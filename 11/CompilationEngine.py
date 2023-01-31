# a recursive top-down parser
# serves as the main module that drives the overall compilation process

from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationEngine:
    # create a new compilation engine with the given input and output
    # the next routine called by the JackAnalyzer module must be compileClass
    def __init__(self, inputfile: str, outputfile: str) -> None:
        self.tokenizer = JackTokenizer(inputfile)
        self.writer = VMWriter(outputfile)
        self.getTokenStream()

    """
    compilexxx methods: each method is called only if the current token is xxx
    compilexxx should get from input and handle all the tokens that make up xxx,
    advance the tokenizer exactly beyond these tokens
    """

    # compile a complete class. No code is generated
    def compileClass(self) -> None:
        self.advance()
        # initialize symbol tables with className
        self.classname = self.token
        self.classST = SymbolTable(self.classname)
        self.subroutineST = SymbolTable(self.classname)
        self.advance()
        # parse zero or more classVarDec
        self.advance()
        while self.token in ["static", "field"]:
            self.compileClassVarDec()
        # parse zero or more subroutineDec
        while self.token in ["constructor", "function", "method"]:
            self.compileSubroutineDec()
        # parse "}"

    # compile a static variable or field declaration
    def compileClassVarDec(self) -> None:
        kind = self.token
        self.advance()
        type = self.token
        # parse one or more varNames
        self.advance()
        while not self.token == ";":
            name = self.token
            # add variable to class-level symbol table
            self.classST.define(name, type, kind)
            self.advance()
            if self.token == ",":
                self.advance()
        self.advance()

    # compile a complete method, function or constructor
    def compileSubroutineDec(self) -> None:
        # reset subroutine-level symbol table
        self.subroutineST.reset()
        # add this pointer to symbol table
        isMethod = self.token == "method"
        if isMethod:
            self.subroutineST.define("this", self.classname, "arg")
        self.advance(2)
        subroutineName = self.token
        self.advance(2)
        self.compileParameterList()
        # write funtion definition
        self.writer.writeFunction(
            f"{self.classname}.{subroutineName}", self.subroutineST.varCount("arg")
        )
        # parse subroutineBody
        self.advance()
        # align this pointer with the object's base address
        if isMethod:
            self.writer.writePush("argument", 0)
            self.writer.writePop("pointer", 0)
        self.compileSubroutineBody()
        self.advance()

    # compile a possibly empty parameter lists
    # Does not handle the enclosing parentheses tokens: ( and )
    def compileParameterList(self) -> None:
        # parse zero or more arguments
        while self.tokentype in ["KEYWORD", "IDENTIFIER"]:
            type = self.token
            self.advance()
            name = self.token
            # add parameter to symbol table
            self.subroutineST.define(name, type, "arg")
            self.advance()
            if self.token == ",":
                self.advance()

    # compile a subroutine's body
    def compileSubroutineBody(self) -> None:
        # parse zero or more varDec
        self.advance()
        while self.token == "var":
            self.compileVarDec()
        # parse statements
        self.compileStatements()

    # compile a var declaration, possibly with multiple varName
    def compileVarDec(self) -> None:
        self.advance()
        type = self.token
        # parse one or more varNames(using do-while loop)
        while True:
            self.advance()
            name = self.token
            # add local variable to symbol table
            self.subroutineST.define(name, type, "var")
            self.advance()
            if not self.token == ",":
                break
        self.advance()

    # compile a sequence of statements
    # Does not handle the enclosing curly bracket tokens: { and }
    def compileStatements(self) -> None:
        # parse zero or more statements
        while self.token in ["let", "if", "while", "do", "return"]:
            # parse letStatement
            if self.token == "let":
                self.compileLet()
            # parse ifStatement
            elif self.token == "if":
                self.compileIf()
            # parse whileStatement
            elif self.token == "while":
                self.compileWhile()
            # parse doStatement
            elif self.token == "do":
                self.compileDo()
            # parse returnStatement
            elif self.token == "return":
                self.compileReturn()

    # compile a let statment
    def compileLet(self) -> None:
        # parse "let"
        # parse varName
        self.advance()
        # parse possibly "["
        self.advance()
        if self.token == "[":
            # parse expression
            self.advance()
            self.compileExpression()
            # parse "]"
            self.advance()
        # parse "="
        # parse expression
        self.advance()
        self.compileExpression()
        # parse ";"
        self.advance()

    # compile a if statment, possibly with a trailing else clause
    def compileIf(self) -> None:
        # parse "if"
        # parse "("
        self.advance()
        # parse expression
        self.advance()
        self.compileExpression()
        # parse ")"
        # parse "{"
        self.advance()
        # parse statements
        self.advance()
        self.compileStatements()
        # parse "}"
        # parse possibly else clause
        self.advance()
        if self.token == "else":
            # parse "else"
            # parse "{"
            self.advance()
            # parse statements
            self.advance()
            self.compileStatements()
            # parse "}"
            # next token
            self.advance()

    # compile a while statment
    def compileWhile(self) -> None:
        # parse "while"
        # parse "("
        self.advance()
        # parse expression
        self.advance()
        self.compileExpression()
        # parse ")"
        # parse "{"
        self.advance()
        # parse statements
        self.advance()
        self.compileStatements()
        # parse "}"
        self.advance()

    # compile a do statment
    def compileDo(self) -> None:
        self.advance()
        self.compileTerm()
        # discard unused return value
        self.writer.writePop("temp", 0)
        self.advance()

    # compile a return statement
    def compileReturn(self) -> None:
        # parse possibly expression
        self.advance()
        if not self.token == ";":
            self.compileExpression()
            self.writer.writeReturn()
        # return 0 when return type is void
        else:
            self.writer.writePush("constant", 0)
            self.writer.writeReturn()
        self.advance()

    # compile an expression
    def compileExpression(self) -> None:
        # parse one or more terms
        self.compileTerm()
        while self.token in ["+", "-", "*", "/", "&", "|", ">", "<", "="]:
            op = self.token
            self.advance()
            self.compileTerm()
            # add postfix operator
            self.writer.writeArithmetic(op)

    # compile a term. If the current token is identifier,
    # the routine must resolve it into a variable / array element / subroutine call
    # single lookahead token is needed to distinguish between the possibilities
    # another token is not part of this term and should not be advanced over
    def compileTerm(self) -> None:
        # parse integerConstant
        if self.tokentype == "INT_CONST":
            self.writer.writePush("constant", self.token)
        # parse stringConstant
        elif self.tokentype == "STRING_CONST":
            pass
        # parse keywordConstant: "true", "false", "null", "this"
        elif self.tokentype == "KEYWORD":
            pass
        # parse varName, varName[expression], subroutineCall
        elif self.tokentype == "IDENTIFIER":
            # single lookahead
            next_token = self.tokenstream[self.position + 1][0]
            if next_token == "[":
                # parse varName
                # parse "["
                self.advance()
                # parse expression
                self.advance()
                self.compileExpression()
                # parse "]"
            elif next_token == "(":
                self.advance(2)
                nArgs = self.compileExpressionList()
            # parse (className | varName).subroutineName(expressionList)
            elif next_token == ".":
                classNameorvarName = self.token
                self.advance(2)
                subroutineName = self.token
                self.advance(2)
                nArgs = self.compileExpressionList()
                self.writer.writeCall(f"{classNameorvarName}.{subroutineName}", nArgs)
            # parse varName
            else:
                pass
        # parse unaryOp term
        elif self.token in ["-", "~"]:
            self.advance()
            self.compileTerm()
            return
        # parse (pression)
        elif self.token == "(":
            self.advance()
            self.compileExpression()
        self.advance()

    # compile a possibly empty comma-seperated list of expressions
    # returns the number of expressions in the list
    # the return value is necessary for generating VM code, thus not used in project 10
    def compileExpressionList(self) -> int:
        # initialize expression counter
        cnt = 0
        # parse zero or more expression
        while not self.token == ")":
            # parse first expression
            self.compileExpression()
            cnt += 1
            if self.token == ",":
                self.advance()
        return cnt

    """ below are helper functions """

    # get all tokens and their type from tokenizer at once
    def getTokenStream(self) -> None:
        self.tokenstream = []
        self.position = 0
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.tokenstream.append((self.tokenizer.token, self.tokenizer.tokentype))
        # initialize token and tokentype
        (self.token, self.tokentype) = self.tokenstream[0]

    # advance token by one and update current token and tokentype
    def advance(self, step: int = 1) -> None:
        self.position += step
        (self.token, self.tokentype) = self.tokenstream[self.position]
