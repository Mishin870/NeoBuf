from typing import List

import simple_types
import utils

"""
Module for compiling variables from raw keywords
"""


class Variable:
    """
    Variable information that holds information about:
    - Required usings
    - Variable definition
    - Networking code (reading and writing this variable to the network stream)
    """
    
    def __init__(self, usings: List[str], variables: List[str], reads: List[str], writes: List[str]):
        self.usings = usings
        self.variables = variables
        self.reads = reads
        self.writes = writes


def _compile_simple(variable: str, read: str, write: str) -> Variable:
    """Helper function to create single variable"""
    return Variable([], [utils.add_space(variable, 2)], [utils.add_space(read, 3)], [utils.add_space(write, 3)])


def _compile_list(variable: str, read: str, write: str) -> Variable:
    """Helper function to create variable of list type with dependency on System.Collections.Generic"""
    return Variable(["System.Collections.Generic"], [utils.add_space(variable, 2)],
                    [utils.add_space(read, 3)], [utils.add_space(write, 3)])


def compile_variable(key: str, type: str, name: str, comment: str) -> Variable:
    """Compile parsed keywords to variable definition"""
    
    formatted_comment = ""
    if comment != "":
        formatted_comment = " // {}".format(comment)
    
    if key == "#":
        # If this is a single variable (#)
        
        if simple_types.has_type(type):
            simple = simple_types.get_type(type)
            
            return _compile_simple("public {} {};{}".format(simple.code, name, comment),
                                   "{} = Data.Read{}();".format(name, simple.title),
                                   "Data.Write{}({});".format(simple.title, name))
        elif type.startswith("!"):
            # Specified type is an enum
            type = type[1:]
            
            return _compile_simple("public {} {};{}".format(type, name, formatted_comment),
                                   "{} = ({})Data.ReadInt();".format(name, type),
                                   "Data.WriteInt((int) {});".format(name))
        else:
            # Specified type is not simple
            # We assume that this type has READER and WRITER constants
            
            return _compile_simple("public {} {};{}".format(type, name, formatted_comment),
                                   "{} = {}.READER(Data);".format(name, type),
                                   "{}.WRITER(Data, {});".format(type, name))
    elif key == "@":
        # If this is a list of specified type (@)
        
        if simple_types.has_type(type):
            simple = simple_types.get_type(type)
            
            return _compile_simple("public List<{}> {};{}".format(simple.code, name, formatted_comment),
                                   "{} = Data.ReadList(NetworkHelper.{}_READER);".format(name, simple.uppercase),
                                   "Data.WriteList({}, NetworkHelper.{}_WRITER);".format(name, simple.uppercase))
        elif type.startswith("!"):
            # Specified type is an enum
            type = type[1:]
            
            return _compile_list("public List<{}> {};{}".format(type, name, formatted_comment),
                                 "{} = Data.ReadList(NetworkHelper.MakeEnumReader<{}>());".format(name, type),
                                 "Data.WriteList({}, NetworkHelper.MakeEnumWriter<{}>());".format(name, type))
        else:
            # Specified type is not simple
            # We assume that this type has READER and WRITER constants
            
            return _compile_list("public List<{}> {};{}".format(type, name, formatted_comment),
                                 "{} = Data.ReadList({}.READER);".format(name, type),
                                 "Data.WriteList({}, {}.WRITER);".format(name, type))
    
    return None
