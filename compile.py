import os
import template
import utils
import variable

"""
Main script
Run it at the root directory of your project
It uses current working directory as the starting point
"""


def compile_message(path, file):
    """Compile one *.msg file"""
    
    print('Compiling {}'.format(file))
    
    with open(os.path.join(path, file), encoding='utf-8') as src_file:
        lines = src_file.readlines()
    
    name = utils.replace_ending(file, ".msg", "")
    dst_file = os.path.join(path, "{}.cs".format(name))
    package = "NoPackage"
    usings = {
        "NeoSeusCore.Network.Transport"
    }
    variables = []
    reads = []
    writes = []
    
    for line in lines:
        parts = line.split()
        
        if len(parts) < 1:
            continue
        
        key = parts[0]
        
        if key == "package":
            # Message package definition
            package = parts[1]
        elif key == "use":
            # Custom dependencies
            usings.add(parts[1])
        elif key == "//":
            # Just a *.msg comment (will not be compiled to *.cs)
            pass
        elif key == "%":
            # Separator between variables (empty line between them in *.cs)
            if len(parts) >= 2:
                # and optional comment
                space = utils.add_space("", 2)
                variables.append("{}\n{}// {}".format(space, space, " ".join(parts[1:])))
            else:
                variables.append(utils.add_space("", 2))
            
            reads.append(utils.add_space("", 3))
            writes.append(utils.add_space("", 3))
            
            continue
        elif key == "#" or key == "@":
            # Variable of specified type (#) or List<specified type> (@)
            parts_count = len(parts)
            
            if parts_count >= 3:
                # Optional inline comment for variable definition
                comment = ""
                if parts_count >= 4:
                    comment = " ".join(parts[3:])
                
                definition = variable.compile_variable(key, parts[1], parts[2], comment)
                
                if definition is None:
                    print("Warning! Unknown key {} for type {} for variable {}".format(key, parts[1], parts[2]))
                    continue
                
                # Variable can require some usings (e.g. List require System.Collections.Generic)
                for line_using in definition.usings:
                    usings.add(line_using)
                
                for line_variable in definition.variables:
                    variables.append(line_variable)
                
                for line_read in definition.reads:
                    reads.append(line_read)
                
                for line_write in definition.writes:
                    writes.append(line_write)
                
                continue

    result = template.make_template()
    result = result.replace("%variables%", "\n".join(variables))
    result = result.replace("%read%", "\n".join(reads))
    result = result.replace("%write%", "\n".join(writes))
    result = result.replace("%package%", package)
    result = result.replace("%name%", name)
    
    # Our networking library require all messages to inherit NeoSeusCore.Messages.Message
    # so if we not in this namespace, we need to autoimport it
    if not package.startswith("NeoSeusCore.Messages"):
        usings.add("NeoSeusCore.Messages")
    
    usings_new = []
    for using in usings:
        usings_new.append("using {};".format(using))
    result = result.replace("%usings%", "\n".join(usings_new))
    
    with open(dst_file, 'w', encoding='utf-8') as write_to:
        write_to.write(result)


def compile_all():
    exclude = {'.git', '.idea', 'obj', 'bin', 'packages'}
    
    for root, dirs, files in os.walk(os.curdir):
        dirs[:] = [d for d in dirs if d not in exclude]
        
        for file in files:
            if file.endswith('.msg'):
                compile_message(root, file)


compile_all()
