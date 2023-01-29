# This module provides services for building, populating and using symbol tables
# which keep track of the symbol properties: name, type, kind and index for each kind


class SymbolTable:
    # Create a new symbol table
    def __init__(self) -> None:
        pass

    # Empty the symbol table and reset index when starting compile a subroutineDec
    def reset(self) -> None:
        pass

    # Add a new variable to symbol table, update the running index
    def define(self, name: str, type: str, kind: str) -> None:
        pass

    # Return the number of defined variables of given kind
    def varCount(self, kind: str) -> int:
        pass

    # Return the kind of the named variable
    def kindOf(self, name: str) -> str:
        pass

    # Return the type of the named variable
    def typeOf(self, name: str) -> str:
        pass

    # Return the index of the named variable
    def indexOf(self, name: str) -> int:
        pass
