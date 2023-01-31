# This module features a set of simple routines for writing VM commands
# into the output file


class VMWriter:
    # Create a new output .vm stream and prepares for writing
    def __init__(self, outputfile: str) -> None:
        self.outputstream = open(outputfile, "w")

    # Write a VM push command
    def writePush(self, segment: str, index: str) -> None:
        self.writeLine(f"push {segment} {index}")

    # Write a VM pop command
    def writePop(self, segment: str, index: str) -> None:
        self.writeLine(f"pop {segment} {index}")

    # Write a VM arithmetic-logical command
    def writeArithmetic(self, command: str) -> None:
        if command == "+":
            self.writeLine("add")
        elif command == "-":
            self.writeLine("sub")
        elif command == "*":
            self.writeCall("Math.multiply", 2)
        elif command == ">":
            self.writeLine("gt")
        elif command == "<":
            self.writeLine("lt")
        elif command == "=":
            self.writeLine("eq")
        elif command == "&":
            self.writeLine("and")
        elif command == "|":
            self.writeLine("or")

    # Write a VM label command
    def writeLabel(self, label: str) -> None:
        self.writeLine(f"label {label}")

    # Write a VM goto command
    def writeGoto(self, label: str) -> None:
        self.writeLine(f"goto {label}")

    # Write a VM if-goto command
    def writeIf(self, label: str) -> None:
        self.writeLine(f"if-goto {label}")

    # Write a VM call command
    def writeCall(self, name: str, nArgs: int) -> None:
        self.writeComment(f"call function {name}")
        self.writeLine(f"call {name} {nArgs}")

    # Write a VM function command
    def writeFunction(self, name: str, nVars: int) -> None:
        self.writeComment(f"define function {name}")
        self.writeLine(f"function {name} {str(nVars)}")

    # Write a VM return command
    def writeReturn(self) -> None:
        self.writeLine("return")

    # Close the output stream
    def close(self) -> None:
        self.outputstream.close()

    """ below are helper functions """

    def writeLine(self, code: str = "") -> None:
        self.outputstream.write(code + "\n")

    def writeComment(self, comment: str) -> None:
        self.writeLine()
        self.writeLine(f"// {comment}")
        self.writeLine()
