# a recursive top-down parser
# serves as the main module that drives the overall compilation process

import xml.etree.ElementTree as ET
from JackTokenizer import JackTokenizer


class CompilationEngine:
    # create a new compilation engine with the given input and output
    # the next routine called by the JackAnalyzer module must be compileClass
    def __init__(self, inputfile: str, outputfile: str) -> None:
        self.tokenizer = JackTokenizer(inputfile)
        self.outputfile = outputfile
        self.getTokenStream()

    """
    compilexxx methods: each method is called only if the current token is xxx
    compilexxx should get from input and handle all the tokens that make up xxx,
    advance the tokenizer exactly beyond these tokens
    """

    # compile a complete class, compile unit of CompilationEngine
    def compileClass(self) -> None:
        # initialize the xml root element
        xmlclass = ET.Element("class")
        self.xmlclass = xmlclass
        # parse "class"
        self.addXmlElement(xmlclass, "keyword")
        # parse className
        self.advance()
        self.addXmlElement(xmlclass, "identifier")
        # parse "{"
        self.advance()
        self.addXmlElement(xmlclass, "symbol")
        # parse zero or more classVarDec
        self.advance()
        while self.token in ["static", "field"]:
            self.compileClassVarDec(xmlclass)
        # parse zero or more subroutineDec
        while self.token in ["constructor", "function", "method"]:
            self.compileSubroutineDec(xmlclass)
        # parse "}"
        self.addXmlElement(xmlclass, "symbol")

    # compile a static variable or field declaration
    def compileClassVarDec(self, xmlclass: ET.Element) -> None:
        # create new xml element
        xmlclassVarDec = ET.SubElement(xmlclass, "classVarDec")
        # parse "static" or "field"
        self.addXmlElement(xmlclassVarDec, "keyword")
        # parse type
        self.advance()
        self.addXmlElement(xmlclassVarDec, self.tokentype.lower())
        # parse one or more varNames
        self.advance()
        while not self.token == ";":
            # parse varName
            self.addXmlElement(xmlclassVarDec, "identifier")
            self.advance()
            # parse possibly ","
            if self.token == ",":
                self.addXmlElement(xmlclassVarDec, "symbol")
                self.advance()
        # parse ";"
        self.addXmlElement(xmlclassVarDec, "symbol")
        # next token
        self.advance()

    # compile a complete method, function or constructor
    def compileSubroutineDec(self, xmlclass: ET.Element) -> None:
        # create new xml element
        xmlsubroutineDec = ET.SubElement(xmlclass, "subroutineDec")
        # parse "constructor", "function" or "method"
        self.addXmlElement(xmlsubroutineDec, "keyword")
        # parse "void" or type
        self.advance()
        self.addXmlElement(xmlsubroutineDec, self.tokentype.lower())
        # parse subroutineName
        self.advance()
        self.addXmlElement(xmlsubroutineDec, "identifier")
        # parse "("
        self.advance()
        self.addXmlElement(xmlsubroutineDec, "symbol")
        # parse parameterList
        self.advance()
        self.compileParameterList(xmlsubroutineDec)
        # parse ")"
        self.addXmlElement(xmlsubroutineDec, "symbol")
        # parse subroutineBody
        self.advance()
        self.compileSubroutineBody(xmlsubroutineDec)
        # next token
        self.advance()

    # compile a possibly empty parameter lists
    # Does not handle the enclosing parentheses tokens: ( and )
    def compileParameterList(self, xmlsubroutine: ET.Element) -> None:
        # create new xml element
        xmlparameterList = ET.SubElement(xmlsubroutine, "parameterList")
        xmlparameterList.text = "\n"
        # parse zero or more arguments
        while self.tokentype in ["KEYWORD", "IDENTIFIER"]:
            # parse type
            self.addXmlElement(xmlparameterList, "keyword")
            # parse varName
            self.advance()
            self.addXmlElement(xmlparameterList, "identifier")
            self.advance()
            # parse possibly ","
            if self.token == ",":
                self.addXmlElement(xmlparameterList, "symbol")
                self.advance()

    # compile a subroutine's body
    def compileSubroutineBody(self, xmlsubroutine: ET.Element) -> None:
        # create new xml element
        xmlsubroutineBody = ET.SubElement(xmlsubroutine, "subroutineBody")
        # parse "{"
        self.addXmlElement(xmlsubroutineBody, "symbol")
        # parse zero or more varDec
        self.advance()
        while self.token == "var":
            self.compileVarDec(xmlsubroutineBody)
        # parse statements
        self.compileStatements(xmlsubroutineBody)
        # parse "}"
        self.addXmlElement(xmlsubroutineBody, "symbol")

    # compile a var declaration
    def compileVarDec(self, xmlsubroutineBody: ET.Element) -> None:
        # create new xml element
        xmlvarDec = ET.SubElement(xmlsubroutineBody, "varDec")
        # parse "var"
        self.addXmlElement(xmlvarDec, "keyword")
        # parse type
        self.advance()
        self.addXmlElement(xmlvarDec, self.tokentype.lower())
        # parse one or more varNames(using do-while loop)
        while True:
            # parse varName
            self.advance()
            self.addXmlElement(xmlvarDec, "identifier")
            # parse possibly ","
            self.advance()
            if self.token == ",":
                self.addXmlElement(xmlvarDec, "symbol")
            else:
                break
        # parse ";"
        self.addXmlElement(xmlvarDec, "symbol")
        # next token
        self.advance()

    # compile a sequence of statements
    # Does not handle the enclosing curly bracket tokens: { and }
    def compileStatements(self, xmlparent: ET.Element) -> None:
        # create new xml element
        xmlstatements = ET.SubElement(xmlparent, "statements")
        xmlstatements.text = "\n"
        # parse zero or more statements
        while self.token in ["let", "if", "while", "do", "return"]:
            # parse letStatement
            if self.token == "let":
                self.compileLet(xmlstatements)
            # parse ifStatement
            elif self.token == "if":
                self.compileIf(xmlstatements)
            # parse whileStatement
            elif self.token == "while":
                self.compileWhile(xmlstatements)
            # parse doStatement
            elif self.token == "do":
                self.compileDo(xmlstatements)
            # parse returnStatement
            elif self.token == "return":
                self.compileReturn(xmlstatements)

    # compile a let statment
    def compileLet(self, xmlstatements: ET.Element) -> None:
        # create new xml element
        xmlletStatement = ET.SubElement(xmlstatements, "letStatement")
        # parse "let"
        self.addXmlElement(xmlletStatement, "keyword")
        # parse varName
        self.advance()
        self.addXmlElement(xmlletStatement, "identifier")
        # parse possibly "["
        self.advance()
        if self.token == "[":
            self.addXmlElement(xmlletStatement, "symbol")
            # parse expression
            self.advance()
            self.compileExpression(xmlletStatement)
            # parse "]"
            self.addXmlElement(xmlletStatement, "symbol")
            self.advance()
        # parse "="
        self.addXmlElement(xmlletStatement, "symbol")
        # parse expression
        self.advance()
        self.compileExpression(xmlletStatement)
        # parse ";"
        self.addXmlElement(xmlletStatement, "symbol")
        # next token
        self.advance()

    # compile a if statment, possibly with a trailing else clause
    def compileIf(self, xmlstatements: ET.Element) -> None:
        # create new xml element
        xmlifStatement = ET.SubElement(xmlstatements, "ifStatement")
        # parse "if"
        self.addXmlElement(xmlifStatement, "keyword")
        # parse "("
        self.advance()
        self.addXmlElement(xmlifStatement, "symbol")
        # parse expression
        self.advance()
        self.compileExpression(xmlifStatement)
        # parse ")"
        self.addXmlElement(xmlifStatement, "symbol")
        # parse "{"
        self.advance()
        self.addXmlElement(xmlifStatement, "symbol")
        # parse statements
        self.advance()
        self.compileStatements(xmlifStatement)
        # parse "}"
        self.addXmlElement(xmlifStatement, "symbol")
        # parse possibly else clause
        self.advance()
        if self.token == "else":
            # parse "else"
            self.addXmlElement(xmlifStatement, "keyword")
            # parse "{"
            self.advance()
            self.addXmlElement(xmlifStatement, "symbol")
            # parse statements
            self.advance()
            self.compileStatements(xmlifStatement)
            # parse "}"
            self.addXmlElement(xmlifStatement, "symbol")
            # next token
            self.advance()

    # compile a while statment
    def compileWhile(self, xmlstatements: ET.Element) -> None:
        # create new xml element
        xmlwhileStatement = ET.SubElement(xmlstatements, "whileStatement")
        # parse "while"
        self.addXmlElement(xmlwhileStatement, "keyword")
        # parse "("
        self.advance()
        self.addXmlElement(xmlwhileStatement, "symbol")
        # parse expression
        self.advance()
        self.compileExpression(xmlwhileStatement)
        # parse ")"
        self.addXmlElement(xmlwhileStatement, "symbol")
        # parse "{"
        self.advance()
        self.addXmlElement(xmlwhileStatement, "symbol")
        # parse statements
        self.advance()
        self.compileStatements(xmlwhileStatement)
        # parse "}"
        self.addXmlElement(xmlwhileStatement, "symbol")
        # next token
        self.advance()

    # compile a do statment
    def compileDo(self, xmlstatements: ET.Element) -> None:
        # create new xml element
        xmldoStatement = ET.SubElement(xmlstatements, "doStatement")
        # parse "do"
        self.addXmlElement(xmldoStatement, "keyword")
        # parse subroutineCall
        self.advance()
        self.compileTerm(xmldoStatement, True)
        # parse ";"
        self.addXmlElement(xmldoStatement, "symbol")
        # next token
        self.advance()

    # compile a return statement
    def compileReturn(self, xmlstatements: ET.Element) -> None:
        # create new xml element
        xmlreturnStatement = ET.SubElement(xmlstatements, "returnStatement")
        # parse "return"
        self.addXmlElement(xmlreturnStatement, "keyword")
        # parse possibly expression
        self.advance()
        if not self.token == ";":
            self.compileExpression(xmlreturnStatement)
        # parse ";"
        self.addXmlElement(xmlreturnStatement, "symbol")
        # next token
        self.advance()

    # compile an expression
    def compileExpression(self, xmlparent: ET.Element) -> None:
        # create new xml element
        xmlexpression = ET.SubElement(xmlparent, "expression")
        # parse one or more terms
        while True:
            self.compileTerm(xmlexpression, False)
            if self.token in ["+", "-", "*", "/", "&", "|", ">", "<", "="]:
                # parse op
                self.addXmlElement(xmlexpression, "symbol")
                self.advance()
            else:
                break

    # compile a term. If the current token is identifier,
    # the routine must resolve it into a variable / array element / subroutine call
    # single lookahead token is needed to distinguish between the possibilities
    # another token is not part of this term and should not be advanced over
    def compileTerm(self, xmlparent: ET.Element, isfromdoStatement: bool) -> None:
        # create new xml element
        if not isfromdoStatement:
            xmlterm = ET.SubElement(xmlparent, "term")
        # parse integerConstant
        if self.tokentype == "INT_CONST":
            self.addXmlElement(xmlterm, "integerConstant")
        # parse stringConstant
        elif self.tokentype == "STRING_CONST":
            self.addXmlElement(xmlterm, "stringConstant")
        # parse keywordConstant: "true", "false", "null", "this"
        elif self.tokentype == "KEYWORD":
            self.addXmlElement(xmlterm, "keyword")
        # parse varName, varName[expression], subroutineCall
        elif self.tokentype == "IDENTIFIER":
            xmlparent = xmlparent if isfromdoStatement else xmlterm
            # single lookahead
            next_token = self.tokenstream[self.position + 1][0]
            if next_token == "[":
                # parse varName
                self.addXmlElement(xmlparent, "identifier")
                # parse "["
                self.advance()
                self.addXmlElement(xmlparent, "symbol")
                # parse expression
                self.advance()
                self.compileExpression(xmlparent)
                # parse "]"
                self.addXmlElement(xmlparent, "symbol")
            elif next_token == "(":
                # parse subroutineName
                self.addXmlElement(xmlparent, "identifier")
                # parse "("
                self.advance()
                self.addXmlElement(xmlparent, "symbol")
                # parse expressionList
                self.advance()
                self.compileExpressionList(xmlparent)
                # parse ")"
                self.addXmlElement(xmlparent, "symbol")
            # parse subroutineCall
            elif next_token == ".":
                # parse className or varName
                self.addXmlElement(xmlparent, "identifier")
                # parse "."
                self.advance()
                self.addXmlElement(xmlparent, "symbol")
                # parse subroutineName
                self.advance()
                self.addXmlElement(xmlparent, "identifier")
                # parse "("
                self.advance()
                self.addXmlElement(xmlparent, "symbol")
                # parse expressionList
                self.advance()
                self.compileExpressionList(xmlparent)
                # parse ")"
                self.addXmlElement(xmlparent, "symbol")
            # parse varName
            else:
                self.addXmlElement(xmlterm, "identifier")
        # parse unaryOp term
        elif self.token in ["-", "~"]:
            self.addXmlElement(xmlterm, "symbol")
            self.advance()
            self.compileTerm(xmlterm, False)
            return
        # parse (pression)
        elif self.token == "(":
            # parse "("
            self.addXmlElement(xmlterm, "symbol")
            # parse expression
            self.advance()
            self.compileExpression(xmlterm)
            # parse "("
            self.addXmlElement(xmlterm, "symbol")
        # next token
        self.advance()

    # compile a possibly empty comma-seperated list of expressions
    # returns the number of expressions in the list
    # the return value is necessary for generating VM code, thus not used in project 10
    def compileExpressionList(self, xmlsubroutineCall: ET.Element) -> int:
        # create new xml element
        xmlexpressionList = ET.SubElement(xmlsubroutineCall, "expressionList")
        xmlexpressionList.text = "\n"
        # initialize expression counter
        cnt = 0
        # parse zero or more expression
        while not self.token == ")":
            # parse first expression
            self.compileExpression(xmlexpressionList)
            cnt += 1
            if self.token == ",":
                # parse ","
                self.addXmlElement(xmlexpressionList, "symbol")
                self.advance()
        return cnt

    """ below are helper functions """

    # parse the current token to xml element
    def addXmlElement(self, parent: ET.Element, type: str) -> None:
        element = ET.SubElement(parent, type)
        element.text = self.token

    # write the formatted xml data to file
    def writeXml(self) -> None:
        ET.indent(self.xmlclass)
        with open(self.outputfile, "w") as f:
            f.write(
                ET.tostring(
                    self.xmlclass, encoding="unicode", short_empty_elements=False
                )
            )

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
    def advance(self) -> None:
        self.position += 1
        (self.token, self.tokentype) = self.tokenstream[self.position]
