# This module provides services for building, populating and using symbol tables
# which keep track of the symbol properties: name, type, kind and index for each kind


class SymbolTable:
    # Create a new symbol table
    def __init__(self, classname: str) -> None:
        # record the running index in a four-key dictionary
        self.index = {
            "static": 0,
            "field": 0,
            "arg": 0,
            "var": 0,
        }
        # initialze symbol table as an empty list
        self.symboltable = []
        self.classname = classname

    # Empty the symbol table and reset index when starting compile a new subroutineDec
    def reset(self) -> None:
        for key in self.index.keys():
            self.index[key] = 0
        self.symboltable = []

    # Add a new variable to symbol table, update the running index
    def define(self, name: str, type: str, kind: str) -> None:
        # store to symbol table as a four-element tuple
        self.symboltable.append((name, type, kind, self.index[kind]))
        # update the running index
        self.index[kind] += 1

    # Return the number of defined variables of given kind
    def varCount(self, kind: str) -> int:
        return self.index[kind]

    # Return the type of the named variable
    # possible return value: ineteger, boolean, char or class name
    def typeOf(self, name: str) -> str:
        for symbol in self.symboltable:
            if symbol[0] == name:
                return symbol[1]
        return None

    # Return the kind of the named variable
    # possible return value: static, field, arg, var
    def kindOf(self, name: str) -> str:
        for symbol in self.symboltable:
            if symbol[0] == name:
                return symbol[2]
        return None

    # Return the index of the named variable
    def indexOf(self, name: str) -> int:
        for symbol in self.symboltable:
            if symbol[0] == name:
                return symbol[3]
        return None

    # Return true if given symbol in the table
    def hasSymbol(self, name: str) -> bool:
        for symbol in self.symboltable:
            if symbol[0] == name:
                return True
        return False
