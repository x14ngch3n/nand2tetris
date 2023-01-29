# This module features a set of simple routines for writing VM commands
# into the output file


class VMWriter:
    # Create a new output .vm stream and prepares for writing
    def __init__(self, outputfile: str) -> None:
        pass

    # Write a VM push command
    def writePush(self, segment: str, index: int) -> None:
        pass

    # Write a VM pop command
    def writePop(self, segment: str, index: int) -> None:
        pass

    # Write a VM arithmetic-logical command
    def writeArithmetic(self, command: str) -> None:
        pass

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
        pass

    # Write a VM function command
    def writeFunction(self, name: str, nVars: int) -> None:
        pass

    # Write a VM return command
    def writeReturn(self) -> None:
        pass

    # Close the output stream
    def close(self) -> None:
        pass
