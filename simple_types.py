"""
This is the registry for all data types to know:

- How to use them in type definitions
- How to call them in function declarations / constants
- And how to work with them
"""


class SimpleType:
    """An entity to hold information about simple language type"""
    
    def __init__(self, code: str, title: str, uppercase: str):
        self.code = code
        self.title = title
        self.uppercase = uppercase


_simple_types = {}


def register(entity: SimpleType) -> None:
    _simple_types[entity.code] = entity
    
    
def has_type(code: str) -> bool:
    """Does type with that code was registered?"""
    return code in _simple_types


def get_type(code: str) -> SimpleType:
    """Get type definition by its code"""
    return _simple_types[code]


register(SimpleType("int", "Int", "INT"))
register(SimpleType("string", "String", "STRING"))
register(SimpleType("long", "Long", "LONG"))
register(SimpleType("bool", "Boolean", "BOOL"))
register(SimpleType("byte", "Byte", "BYTE"))
register(SimpleType("float", "Float", "FLOAT"))
