# LL(1) Jack lang tokenizer, enable accessing one token at a time, parse and provides the type of each token
class JackTokenizer:
    # opens the input .jack file stream and gets ready to tokenize it
    def __init__(self, inputfile: str) -> None:
        pass

    # return true if there are more tokens in the input
    def hasMoreTokens(self) -> None:
        pass

    # gets the next token from the input and makes it the current token
    # this method should be called only if hasMoreToken returns true
    # initially there is no current token
    def advance(self) -> None:
        pass

    # returns the type of the current token as a constant string
    def tokenType(self) -> str:
        pass

    # returns the keyword which is the current token as a constant
    # this method should be called only if tokenType returns KEYWORD
    def keyWord(self) -> str:
        pass

    # returns the character which is the current token
    # this method should be called only if tokenType returns SYMBOL
    def symbol(self) -> str:
        pass

    # returns the string which is the current token
    # this method should be called only if tokenType returns IDENTIFIER
    def identifier(self) -> str:
        pass

    # returns the integer value which is the current token
    # this method should be called only if tokenType returns INT_CONST
    def intVal(self) -> int:
        pass

    # returns the string value which is the current token without the opening and closing double quotes
    # this method should be called only if tokenType returns STRING_CONST
    def stringVal(self) -> str:
        pass
