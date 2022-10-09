"""
Utility functions for compiling
"""


def add_space(text: str, level: int) -> str:
    space = "    " * level
    return f"{space}{text}"


def replace_ending(sentence, old, new):
    """Replace an end of sentence from old to new"""
    if sentence.endswith(old):
        return sentence[:-len(old)] + new
    return sentence
