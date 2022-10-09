# NeoBuf
Metalanguage implementation for networking code in my own game engine (which written in C#)

#### Requirements
* Python 3.5+

#### Setup
* No python packages needed, so just install python 3.5+
* Clone this repo
* Create your own `*.msg` files in your project
* Open terminal, go to the root folder of your project
* Run `python path/to/neobuf/compile.py`

#### Example and how to
Every `*.msg` is a single message entity that will be compiled to respective `*.cs` file near it

Source message consists of lines that starting with a some keyword
* `package` is a package definition for compiled code
* `//` is a comment that will not be in compiled code
* `use` adds a custom dependency
* `#` defines a single variable
* `@` defines a List of specified type
* `!` before variable type means that it is Enum type
* `%` is a line comment that **will** be compiled into `*.cs`

Example:
```text
// Example message for testing NeoBuf

package Test.Foo

use SomeNamespace.SomeClass
use SomeNamespace.SomeEnum

# int Color
# string Name // Some inline comment

% Some comment for Aliases (used only at variable definition and makes empty line at networking code)
@ string Aliases


%
# !SomeEnum MyEnum
# SomeClass MyClass
@ SomeClass ListOfMyClasses
```

If this file is named `Test.msg` then it will be compiled into `Test.cs`:
```cs
// This file was generated via NeoBuf. Please, do not modify manually
// Этот файл был сгенерирован через NeoBuf. Пожалуйста, не редактируйте его вручную
// https://github.com/Mishin870/NeoBuf

using SomeNamespace.SomeClass;
using System.Collections.Generic;
using NeoSeusCore.Network.Transport;
using SomeNamespace.SomeEnum;
using NeoSeusCore.Messages;

namespace Test.Foo {
    public class Test : Message {
        public int Color;
        public string Name;// Some inline comment
        
        // Some comment for Aliases (used only at variable definition and makes empty line at networking code)
        public List<string> Aliases;
        
        public SomeEnum MyEnum;
        public SomeClass MyClass;
        public List<SomeClass> ListOfMyClasses;

        public override void Read(DataStream Data) {
            Color = Data.ReadInt();
            Name = Data.ReadString();
            
            Aliases = Data.ReadList(NetworkHelper.STRING_READER);
            
            MyEnum = (SomeEnum)Data.ReadInt();
            MyClass = SomeClass.READER(Data);
            ListOfMyClasses = Data.ReadList(SomeClass.READER);
        }

        public override void Write(DataStream Data) {
            Data.WriteInt(Color);
            Data.WriteString(Name);
            
            Data.WriteList(Aliases, NetworkHelper.STRING_WRITER);
            
            Data.WriteInt((int) MyEnum);
            SomeClass.WRITER(Data, MyClass);
            Data.WriteList(ListOfMyClasses, SomeClass.WRITER);
        }
    }
} 
```

As you see, all variables from source file has a definition and read / write networking code

It's using my classes such as DataStream and NetworkHelper, but you can define your own or modify this script (also it is possible to migrate it to another language)

#### Tasks
- [X] Compile simple types
- [X] Lists, enums, lists of enums etc.
- [X] `*.msg` comments support
- [X] Comments for compiled C# code
- [X] Inline comments for variables
- [ ] Ability to define path to process (not the working directory)
- [ ] Variables that doesn't need a networking code (only definition)
- [ ] More useful keywords or user friendly stuff