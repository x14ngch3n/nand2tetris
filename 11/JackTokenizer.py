# LL(1) Jack lang tokenizer, enable accessing one token at a time
# parse and provides the type of each token
class JackTokenizer:
    # opens the input .jack file stream and gets ready to tokenize it
    def __init__(self, inputfile: str) -> None:
        self.inputstream = open(inputfile, "r").read()
        self.inputlength = len(self.inputstream)
        self.position = 0
        self.token = ""  # initially there's no current token
        self.Jacksymbol = [
            "{",
            "}",
            "(",
            ")",
            "[",
            "]",
            ".",
            ",",
            ";",
            "+",
            "-",
            "*",
            "/",
            "&",
            "|",
            "<",
            ">",
            "=",
            "~",
        ]
        self.Jackkeyword = [
            "class",
            "method",
            "function",
            "constructor",
            "int",
            "boolean",
            "char",
            "void",
            "var",
            "static",
            "field",
            "let",
            "do",
            "if",
            "else",
            "while",
            "return",
            "true",
            "false",
            "null",
            "this",
        ]

    # return true if there are more tokens in the input
    def hasMoreTokens(self) -> bool:
        return self.position < self.inputlength

    # gets the next token from the input and makes it the current token
    # this method should be called only if hasMoreToken returns true
    # initially there is no current token
    def advance(self) -> None:
        self.space()
        # store the next token and its type
        self.tokentype = self.tokenType()
        if self.tokentype == "KEYWORD":
            self.token = self.keyWord()
        elif self.tokentype == "SYMBOL":
            self.token = self.symbol()
        elif self.tokentype == "INT_CONST":
            self.token = self.intVal()
        elif self.tokentype == "STRING_CONST":
            self.token = self.stringVal()
        elif self.tokentype == "IDENTIFIER":
            self.token = self.identifier()
        self.space()

    # recursively ignore space until usable character
    def space(self) -> None:
        while True:
            if self.peek().isspace():
                self.whiteSpace()
                continue
            if self.lookAhead(2) == "//":
                self.SLComment()
                continue
            if self.lookAhead(3) == "/**":
                self.MLComment()
                continue
            else:
                break

    # returns the type of the current token as a constant string
    # without changing the file position
    def tokenType(self) -> str:
        if self.isKeyWord():
            return "KEYWORD"
        # look ahead one character
        elif self.peek() in self.Jacksymbol:
            return "SYMBOL"
        elif self.peek().isdigit():
            return "INT_CONST"
        elif self.peek() == '"':
            return "STRING_CONST"
        elif self.peek().isalpha() or self.peek() == "_":
            return "IDENTIFIER"

    # return true if the following token is a keyword
    def isKeyWord(self) -> bool:
        for keyword in self.Jackkeyword:
            if self.lookAhead(len(keyword)) == keyword:
                return True
        return False

    # returns the keyword which is the current token as a constant
    # this method should be called only if tokenType returns KEYWORD
    def keyWord(self) -> str:
        old_position = self.position
        while self.peek().isalpha():
            self.position += 1  # append alphabet character
        return self.inputstream[old_position : self.position]

    # returns the character which is the current token
    # this method should be called only if tokenType returns SYMBOL
    def symbol(self) -> str:
        symbol = self.peek()
        self.position += 1
        return symbol

    # returns the string which is the current token
    # this method should be called only if tokenType returns IDENTIFIER
    def identifier(self) -> str:
        old_position = self.position
        while self.peek().isalnum() or self.peek() == "_":
            self.position += 1  # append alphabet or digit or "_" character
        return self.inputstream[old_position : self.position]

    # returns the integer value which is the current token
    # this method should be called only if tokenType returns INT_CONST
    def intVal(self) -> str:
        old_position = self.position
        while self.peek().isdigit():
            self.position += 1  # append digit
        return self.inputstream[old_position : self.position]

    # returns the string value which is the current token without the double quotes
    # this method should be called only if tokenType returns STRING_CONST
    def stringVal(self) -> str:
        self.position += 1  # skip leading '"'
        old_position = self.position
        while not self.peek() == '"':
            self.position += 1
        self.position += 1  # skip trailing '"'
        return self.inputstream[old_position : self.position - 1]

    # ignore single-line: // any chreacters "\n"
    def SLComment(self) -> None:
        while not self.peek() == "\n":  # advance characters until newline
            self.position += 1
        self.position += 1

    # ignore multi-line comment: /** any chreacters */
    def MLComment(self) -> None:
        while not self.lookAhead(2) == "*/":
            self.position += 1
        self.position += 2  # skip trailing "*/"

    # ignore whitespace characters: "", "\t", "\r", "\n"
    def whiteSpace(self) -> None:
        while self.peek().isspace():  # advance until non-whitespace character
            self.position += 1

    # return n characters ahead from current position without changing position
    # if reach EOF, append null character to the return string
    def lookAhead(self, n: int) -> str:
        return (
            self.inputstream[self.position : self.position + n]
            if self.position + n <= self.inputlength
            else self.inputstream[self.position :].rjust(n, "\0")
        )

    # return the character at current position
    def peek(self) -> str:
        return self.lookAhead(1)
