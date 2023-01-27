# a recursive top-down parser
# serves as the main module that drives the overall compilation process
class CompilationEngine:
    # create a new compilation engine with the given input and output
    # the next routine called by the JackAnalyzer module must be compileClass
    def __init__(self, inputfile: str, outputfile: str) -> None:
        pass

    # compile a complete class
    def compileClass(self) -> None:
        pass

    # compile a static variable or field declaration
    def compileClassVarDec(self) -> None:
        pass

    # compile a complete method, function or constructor
    def compileSubroutine(self) -> None:
        pass

    # compile a possibly empty parameter lists
    # Does not handle the enclosing parentheses tokens: ( and )
    def compileParameterList(self) -> None:
        pass

    # compile a subroutine's body
    def compileSubroutineBody(self) -> None:
        pass

    # compile a var declaration
    def compileVarDec(self) -> None:
        pass

    # compile a sequence of statements
    # Does not handle the enclosing curly bracket tokens: { and }
    def compileStatements(self) -> None:
        pass

    # compile a let statment
    def compileLet(self) -> None:
        pass

    # compile a if statment, possibly with a trailing else clause
    def compileIf(self) -> None:
        pass

    # compile a while statment
    def compileWhile(self) -> None:
        pass

    # compile a do statment
    def compileDo(self) -> None:
        pass

    # compile a return statement
    def compileReturn(self) -> None:
        pass

    # compile an expression
    def compileExpression(self) -> None:
        pass

    # compile a term. If the current token is identifier,
    # the routine must resolve it into a variable / array element / subroutine call
    # single lookahead token is needed to distinguish between the possibilities
    # another token is not part of this term and should not be advanced over
    def compileTerm(self) -> None:
        pass

    # compile a possibly empty comma-seperated list of expressions
    # returns the number of expressions in the list
    # the return value is necessary for generating VM code, thus not used in project 10
    def compileExpressionList(self) -> int:
        pass
