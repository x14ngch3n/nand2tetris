#!/opt/homebrew/bin/python3

import argparse
import os


# drive the translation process
class VMTranslator:
    def __init__(self, input: str) -> None:
        if os.path.isdir(input):
            self.inputfiles = [
                os.path.join(input, file) for file in list(filter(lambda file: file.endswith(".vm"), os.listdir(input)))
            ]
            self.outputfile = os.path.join(input, os.path.basename(input) + ".asm")
        else:
            self.inputfiles = [input]
            self.outputfile = input.replace("vm", "asm")

    # translate single file
    def translate(self) -> None:
        C = CodeWriter(self.outputfile)
        for inputfile in self.inputfiles:
            P = Parser(inputfile)
            C.setFilename(inputfile)
            C.initMemory()
            while P.hasMoreLines():
                P.advance()
                self.command_type = P.commandType()
                self.arg1, self.arg2 = P.arg1(self.command_type), P.arg2(self.command_type)
                if self.command_type == "C_ARITHMETIC":
                    C.writeArithmetic(self.arg1)
                elif self.command_type == "C_PUSH":
                    C.writePushPop("push", self.arg1, self.arg2)
                elif self.command_type == "C_POP":
                    C.writePushPop("pop", self.arg1, self.arg2)
                elif self.command_type == "C_LABEL":
                    C.writeLabel(self.arg1)
                elif self.command_type == "C_GOTO":
                    C.writeGoto(self.arg1)
                elif self.command_type == "C_IF":
                    C.writeIf(self.arg1)

            C.endLoop()
            C.close()


# understand what the command seek to do
class Parser:
    def __init__(self, inputfile: str) -> None:
        self.file = open(inputfile, "r")
        self.arithmetic_commands = ["add", "sub", "neg"]
        self.comparison_commands = ["eq", "gt", "lt"]
        self.logical_commands = ["and", "or", "not"]

    # check if new line exists in file stream and get it
    def hasMoreLines(self) -> bool:
        # get new line from file stream
        while True:
            # ignore comments and blank lines
            self.curr_line = self.file.readline()
            if self.curr_line.startswith("//") or self.curr_line == "\n":
                continue
            else:
                break
        return not not self.curr_line

    # trim useless blank space and comment
    def advance(self) -> None:
        # trim newline, space and tab
        self.curr_command = self.curr_line.strip()
        # trim inline comment
        dash = self.curr_command.find("//")
        self.curr_command = self.curr_command[:dash] if dash > 0 else self.curr_command

    # get current command's type
    def commandType(self) -> str:
        # C type command
        self.tokens = self.curr_command.split(" ")
        # Arithmetic-Logical Commands
        if self.tokens[0] in self.arithmetic_commands + self.comparison_commands + self.logical_commands:
            return "C_ARITHMETIC"
        # Push/Pop Commands
        elif self.tokens[0] == "push":
            return "C_PUSH"
        elif self.tokens[0] == "pop":
            return "C_POP"
        # Branch Commands
        elif self.tokens[0] == "label":
            return "C_LABEL"
        elif self.tokens[0] == "goto":
            return "C_GOTO"
        elif self.tokens[0] == "if-goto":
            return "C_IF"

    # returns the first argument of current command
    def arg1(self, type) -> str:
        if type == "C_ARITHMETIC":
            return self.tokens[0]
        elif type in ["C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF"]:
            return self.tokens[1]
        else:
            return ""

    # returns the second argument of current command
    def arg2(self, type) -> str:
        if type in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            return self.tokens[2]
        else:
            return ""


# translate understood command to desired operation in hack lang
class CodeWriter:
    def __init__(self, outputfile: str) -> None:
        self.outputfile = outputfile
        self.file = open(self.outputfile, "w")
        self.segmentMap = {
            # segmantation register, support index
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            # pointer 0 -> THIS, pointer 1 -> THAT
            "pointer": "3",
            "temp": "5",
            # reserve for temporary variables
            "R13": "13",
            "R14": "14",
            "R15": "15",
            # static i for i in range(240)
            "static": "16",
        }
        self.pushTrueCnt = 0
        self.afterCnt = 0
        self.comparison_instruction = {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
        }

    # current file being processed
    def setFilename(self, inputfile: str) -> None:
        self.inputfile = inputfile

    # write one-line hack code to output file
    def writeLine(self, line: str) -> None:
        self.file.write(line + "\n")

    # write to outputfile the hack code that implements the given arithmetic-logical command
    def writeArithmetic(self, command: str) -> None:
        comment = " ".join(["//", command])
        self.writeLine(comment)
        if command == "add":
            self.popD()
            self.popA()
            self.writeLine("D=D+A")
            self.pushD()
        elif command == "sub":
            self.popD()
            self.popA()
            self.writeLine("AD=A-D")
            self.pushD()
        elif command == "neg":
            self.popD()
            self.writeLine("D=-D")
            self.pushD()
        elif command in ["eq", "gt", "lt"]:
            self.comparison(self.comparison_instruction[command])
        elif command == "and":
            self.popD()
            self.popA()
            self.writeLine("D=D&A")
            self.pushD()
        elif command == "or":
            self.popD()
            self.popA()
            self.writeLine("D=D|A")
            self.pushD()
        elif command == "not":
            self.popD()
            self.writeLine("D=!D")
            self.pushD()

    # write to outputfile the hack code that implements the given push/pop command
    def writePushPop(self, command: str, segment: str, index: str) -> None:
        comment = " ".join(["//", command, segment, index])
        self.writeLine(comment)
        if command == "push":
            if segment == "constant":
                self.pushValue(index)
            else:
                self.argParse(segment, index)
                self.writeLine("@R13")
                self.writeLine("A=M")
                self.writeLine("D=M")
                self.pushD()
        elif command == "pop":
            self.argParse(segment, index)
            self.popD()
            # retrive dest from @R13, avoiding D register's conflict
            self.writeLine("@R13")
            self.writeLine("A=M")
            self.writeLine("M=D")

    # write assembly code that effects the label command
    def writeLabel(self, label: str) -> None:
        comment = " ".join(["//", "writeLabel:", label])
        self.writeLine(comment)
        self.writeLine(f"({label})")

    # write assembly code that effects the goto command
    def writeGoto(self, label: str) -> None:
        comment = " ".join(["//", "writeGoto:", label])
        self.writeLine(comment)
        self.writeLine(f"@{label}")
        self.writeLine("0;JMP")

    # write assembly code that effects the if-goto command
    def writeIf(self, label: str) -> None:
        comment = " ".join(["//", "writeIf:", label])
        self.writeLine(comment)
        # check branch condition
        self.popD()
        self.writeLine(f"@{label}")
        self.writeLine("D;JNE")

    """
    a set of helper using A/M and D register
    serve as elemenary operation for VM code
    """

    def initMemory(self):
        self.initSegment("SP", 256)
        self.initSegment("LCL", 300)
        self.initSegment("ARG", 400)
        self.initSegment("THIS", 3000)
        self.initSegment("THAT", 3010)

    def initSegment(self, name, value):
        self.writeLine("// initialize " + name + " segment to " + str(value))
        self.writeLine("@" + str(value))
        self.writeLine("D=A")
        self.writeLine("@" + name)
        self.writeLine("M=D")

    def pushD(self):
        self.writeLine("@SP")
        self.writeLine("A=M")
        self.writeLine("M=D")
        self.writeLine("@SP")
        self.writeLine("M=M+1")

    def popD(self):
        self.writeLine("@SP")
        self.writeLine("AM=M-1")
        self.writeLine("D=M")

    def popA(self):
        self.writeLine("@SP")
        self.writeLine("AM=M-1")
        self.writeLine("A=M")

    def pushValue(self, value):
        self.writeLine("@" + str(value))
        self.writeLine("D=A")
        self.pushD()

    def comparison(self, jumpInstruction):
        self.popD()
        self.popA()
        # unique jump target label for each comparison command
        self.pushTrueName = "PUSH_TRUE." + str(self.pushTrueCnt)
        self.afterName = "AFTER." + str(self.afterCnt)
        self.pushTrueCnt += 1
        self.afterCnt += 1
        # simple jump hack code to determine whether push True(-1) of False(0)
        self.writeLine("D=A-D")
        self.writeLine("@" + self.pushTrueName)
        self.writeLine("D;" + jumpInstruction)
        self.pushValue(0)
        self.writeLine("@" + self.afterName)
        self.writeLine("0;JMP")
        self.writeLabel(self.pushTrueName)
        # hack code don't support @-1
        self.writeLine("D=-1")
        self.pushD()
        self.writeLabel(self.afterName)

    # save computed dest addr to D and R13
    def argParse(self, segment, index):
        self.writeLine("@" + self.segmentMap[segment])
        # direct addressing: temp, pointer
        # indirect addressing: local,argument,this,that
        self.writeLine("D=A") if segment in ["temp", "pointer", "static"] else self.writeLine("D=M")
        self.writeLine("@" + index)
        self.writeLine("D=D+A")
        # save to temporary regisƒter
        self.writeLine("@R13")
        self.writeLine("M=D")

    def endLoop(self):
        self.writeLine("// end hack program with infinite loop")
        self.writeLine("(END_LOOP)")
        self.writeLine("@END_LOOP")
        self.writeLine("0;JMP")

    def close(self):
        self.file.close()
        print("Hack code saved to: ", self.outputfile)


if __name__ == "__main__":
    # parse commandline
    parser = argparse.ArgumentParser(
        description="Jack virtual machine's translator, from VM code to HACK assembly code"
    )
    parser.add_argument("input", help=".vm file or folder contains .vm files")
    input = parser.parse_args().input
    # start translation
    VMT = VMTranslator(input)
    VMT.translate()
