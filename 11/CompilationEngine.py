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
        # record while and if statements label
        self.whileBegin = "whileBegin.0"
        self.whileEnd = "whileEnd.0"
        self.ifFalse = "ifFalse.0"
        self.ifEnd = "ifEnd.0"

    # update label counter each time
    def __getattribute__(self, name: str) -> str:
        if name in ["whileBegin", "whileEnd", "ifFalse", "ifEnd"]:
            label = super().__getattribute__(name)
            newlabel = ".".join(
                [label.split(".")[0], str(int(label.split(".")[1]) + 1)]
            )
            super().__setattr__(name, newlabel)
            return label
        else:
            return super().__getattribute__(name)

    """
    compilexxx methods: each method is called only if the current token is xxx
    compilexxx should get from input and handle all the tokens that make up xxx,
    advance the tokenizer exactly beyond these tokens
    """

    # compile a complete class. No code is generated
    def compileClass(self) -> None:
        self.advance()
        # initialize symbol tables with className
        self.className = self.token
        self.classST = SymbolTable(self.className)
        self.subroutineST = SymbolTable(self.className)
        self.advance()
        # parse zero or more classVarDec
        self.advance()
        while self.token in ["static", "field"]:
            self.compileClassVarDec()
        # parse zero or more subroutineDec
        while self.token in ["constructor", "function", "method"]:
            self.subroutineType = self.token
            self.compileSubroutineDec()

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
        self.advance(2)
        self.subroutineName = self.token
        self.advance(2)
        self.compileParameterList()
        # parse subroutineBody
        self.advance()
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
        # write funtion definition
        self.writer.writeFunction(
            f"{self.className}.{self.subroutineName}", self.subroutineST.varCount("var")
        )
        # add subroutine specific prelogue code
        if self.subroutineType == "constructor":
            # allocate dynamic memory for field varailes
            self.writer.writePush("constant", self.classST.varCount("field"))
            self.writer.writeCall("Memory.alloc", 1)
            self.writer.writePop("pointer", 0)
        elif self.subroutineType == "method":
            self.subroutineST.define("this", self.className, "arg")
            # assign argument 0 to this pointer
            self.writer.writePush("argument", 0)
            self.writer.writePop("pointer", 0)
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

    # compile a let statement
    def compileLet(self) -> None:
        self.advance()
        name = self.token
        self.advance()
        segment, index = self.mapVariable(name)
        # parse array access
        if self.token == "[":
            # push array
            self.writer.writePush(segment, index)
            self.advance()
            self.compileExpression()
            # add array and expression
            self.writer.writeArithmetic("+")
            self.advance(2)
            self.compileExpression()
            # save right value to temp 0
            self.writer.writePop("temp", 0)
            # assign that pointer
            self.writer.writePop("pointer", 1)
            # push right value
            self.writer.writePush("temp", 0)
            # store right value to the element
            self.writer.writePop("that", 0)
        # parse simple let statement
        else:
            self.advance()
            self.compileExpression()
            # assign expression result to varName
            self.writer.writePop(segment, index)
        self.advance()

    # compile a if statement, possibly with a trailing else clause
    def compileIf(self) -> None:
        # fetch label
        ifFalse = self.ifFalse
        ifEnd = self.ifEnd
        self.advance(2)
        self.compileExpression()
        # check if condition
        self.writer.writeLine("not")
        self.writer.writeIf(ifFalse)
        self.advance(2)
        self.compileStatements()
        # finish if True expression
        self.writer.writeGoto(ifEnd)
        # parse possibly else clause
        self.advance()
        if self.token == "else":
            self.advance(2)
            self.writer.writeLabel(ifFalse)
            self.compileStatements()
            self.advance()
        else:
            # insert a fake ifFalse label
            self.writer.writeLabel(ifFalse)
        self.writer.writeLabel(ifEnd)

    # compile a while statement
    def compileWhile(self) -> None:
        # fetch label
        whileBegin = self.whileBegin
        whileEnd = self.whileEnd
        # write begin label
        self.writer.writeLabel(whileBegin)
        self.advance(2)
        self.compileExpression()
        # check while condition
        self.writer.writeLine("not")
        self.writer.writeIf(whileEnd)
        self.advance(2)
        self.compileStatements()
        self.writer.writeGoto(whileBegin)
        # write end label
        self.writer.writeLabel(whileEnd)
        self.advance()

    # compile a do statement
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
            # create string object
            string = self.token
            self.writer.writePush("constant", len(string))
            self.writer.writeCall("String.new", 1)
            # append characters
            for char in string:
                self.writer.writePush("constant", ord(char))
                self.writer.writeCall("String.appendChar", 2)
        # parse keywordConstant
        elif self.tokentype == "KEYWORD":
            if self.token == "true":
                self.writer.writePush("constant", 1)
                self.writer.writeLine("neg")
            elif self.token in ["false", "null"]:
                self.writer.writePush("constant", 0)
            elif self.token == "this":
                self.writer.writePush("pointer", 0)
        # parse varName, varName[expression], subroutineCall
        elif self.tokentype == "IDENTIFIER":
            # single lookahead
            next_token = self.tokenstream[self.position + 1][0]
            # parse array access
            if next_token == "[":
                # push array
                segment, index = self.mapVariable(self.token)
                self.writer.writePush(segment, index)
                self.advance(2)
                self.compileExpression()
                # add array and expression
                self.writer.writeArithmetic("+")
                # assign that pointer
                self.writer.writePop("pointer", 1)
                # de-reference that pointer
                self.writer.writePush("that", 0)
            # parse subroutineName(expressionList)
            elif next_token == "(":
                subroutineName = self.token
                self.advance(2)
                nArgs = self.compileExpressionList()
                self.writer.writePush("pointer", 0)
                self.writer.writeCall(f"{self.className}.{subroutineName}", nArgs + 1)
            # parse (className | varName).subroutineName(expressionList)
            elif next_token == ".":
                classNameorvarName = self.token
                self.advance(2)
                subroutineName = self.token
                self.advance(2)
                segment, index = self.mapVariable(classNameorvarName)
                # method call: varName.subroutineName(expressionList)
                if segment:
                    self.writer.writePush(segment, index)
                    nArgs = self.compileExpressionList()
                    # get className of varName
                    className = self.subroutineST.typeOf(
                        classNameorvarName
                    ) or self.classST.typeOf(classNameorvarName)
                    self.writer.writeCall(f"{className}.{subroutineName}", nArgs + 1)
                # do function call: className.subroutineName(expressionList)
                else:
                    nArgs = self.compileExpressionList()
                    self.writer.writeCall(
                        f"{classNameorvarName}.{subroutineName}", nArgs
                    )
            # parse varName
            else:
                name = self.token
                segment, index = self.mapVariable(name)
                self.writer.writePush(segment, index)
        # parse unaryOp term
        elif self.token in ["-", "~"]:
            unaryOp = self.token
            self.advance()
            self.compileTerm()
            self.writer.writeLine("neg" if unaryOp == "-" else "not")
            return
        # parse (expression)
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

    # map variable in symbol table to VM segment format
    def mapVariable(self, name: str):
        if self.subroutineST.hasSymbol(name):
            if self.subroutineST.kindOf(name) == "var":
                return "local", self.subroutineST.indexOf(name)
            elif self.subroutineST.kindOf(name) == "arg":
                return "argument", self.subroutineST.indexOf(name)
        elif self.classST.hasSymbol(name):
            if self.classST.kindOf(name) == "static":
                return "static", self.classST.indexOf(name)
            elif self.classST.kindOf(name) == "field":
                return "this", self.classST.indexOf(name)
        else:
            return None, None
