# This module features a set of simple routines for writing VM commands
# into the output file


class VMWriter:
    # Create a new output .vm stream and prepares for writing
    def __init__(self, outputfile: str) -> None:
        self.outputstream = open(outputfile, "w")

    # Write a VM push command
    def writePush(self, segment: str, index: str) -> None:
        self.outputstream.write(f"push {segment} {index}\n")

    # Write a VM pop command
    def writePop(self, segment: str, index: str) -> None:
        self.outputstream.write(f"pop {segment} {index}\n")

    # Write a VM arithmetic-logical command
    def writeArithmetic(self, command: str) -> None:
        if command == "+":
            self.outputstream.write("add\n")
        elif command == "*":
            self.outputstream.write("call Math.multiply 2\n")

    # Write a VM label command
    def writeLabel(self, label: str) -> None:
        pass

    # Write a VM goto command
    def writeGoto(self, label: str) -> None:
        pass

    # Write a VM if-goto command
    def writeIf(self, label: str) -> None:
        pass

    # Write a VM call command
    def writeCall(self, name: str, nArgs: int) -> None:
        self.outputstream.write(f"call {name} {nArgs}\n")

    # Write a VM function command
    def writeFunction(self, name: str, nVars: int) -> None:
        self.outputstream.write(f"function {name} {str(nVars)}\n")

    # Write a VM return command
    def writeReturn(self) -> None:
        self.outputstream.write("return\n")

    # Close the output stream
    def close(self) -> None:
        pass
