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
    def translate(self, bootstrap: bool, endloop: bool) -> None:
        C = CodeWriter(self.outputfile)
        if bootstrap:
            C.writeBootstrap()
        for inputfile in self.inputfiles:
            P = Parser(inputfile)
            C.setFilename(os.path.basename(inputfile).split(".")[0])
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
                elif self.command_type == "C_FUNCTION":
                    C.writeFuntion(self.arg1, self.arg2)
                elif self.command_type == "C_CALL":
                    C.writeCall(self.arg1, self.arg2)
                elif self.command_type == "C_RETURN":
                    C.writeReturn()
        if endloop:
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
        # Arithmetic-Logical commands
        if self.tokens[0] in self.arithmetic_commands + self.comparison_commands + self.logical_commands:
            return "C_ARITHMETIC"
        # Push/Pop commands
        elif self.tokens[0] == "push":
            return "C_PUSH"
        elif self.tokens[0] == "pop":
            return "C_POP"
        # Branch commands
        elif self.tokens[0] == "label":
            return "C_LABEL"
        elif self.tokens[0] == "goto":
            return "C_GOTO"
        elif self.tokens[0] == "if-goto":
            return "C_IF"
        # Function commands
        elif self.tokens[0] == "function":
            return "C_FUNCTION"
        elif self.tokens[0] == "return":
            return "C_RETURN"
        elif self.tokens[0] == "call":
            return "C_CALL"

    # returns the first argument of current command
    def arg1(self, type) -> str:
        if type == "C_ARITHMETIC":
            return self.tokens[0]
        elif type in ["C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION", "C_CALL"]:
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
        self.TrueCnt = 0
        self.afterCnt = 0
        self.returnCnt = 0
        self.comparison_instruction = {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
        }
        self.functionName = ""

    # current file being processed
    def setFilename(self, inputfile: str) -> None:
        self.inputfile = inputfile

    # write one-line hack code to output file
    def writeLine(self, line: str) -> None:
        self.file.write(line + "\n")

    # write to outputfile the hack code that implements the given arithmetic-logical command
    def writeArithmetic(self, command: str) -> None:
        self.writeLine(" ".join(["//", command]))
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
        self.writeLine(" ".join(["//", command, segment, index]))
        if command == "push":
            if segment == "constant":
                self.pushValue(index)
            else:
                self.getAddress(self.segmentMap[segment], index)
                self.getValue()
                self.pushD()
        elif command == "pop":
            self.getAddress(self.segmentMap[segment], index)
            self.popD()
            # retrive destination from R13, avoiding D register's conflict
            self.writeLine("@R13")
            self.writeLine("A=M")
            self.writeLine("M=D")

    # write assembly code that effects the label command
    def writeLabel(self, label: str) -> None:
        mangled_label = f"{self.functionName}${label}" if self.functionName else label
        self.writeLine(" ".join(["//", "writeLabel:", mangled_label]))
        self.writeLine(f"({mangled_label})")

    # write assembly code that effects the goto command
    def writeGoto(self, label: str) -> None:
        mangled_label = f"{self.functionName}${label}" if self.functionName else label
        self.writeLine(" ".join(["//", "writeGoto:", mangled_label]))
        self.writeLine("@" + mangled_label)
        self.writeLine("0;JMP")

    # write assembly code that effects the if-goto command
    def writeIf(self, label: str) -> None:
        mangled_label = f"{self.functionName}${label}" if self.functionName else label
        self.writeLine(" ".join(["//", "writeIf:", mangled_label]))
        # check branch condition
        self.popD()
        self.writeLine("@" + mangled_label)
        self.writeLine("D;JNE")

    # write assembly code that effects the function command
    def writeFuntion(self, functionName: str, nVars: str) -> None:
        self.writeLine(" ".join(["//", "writeFunction:", functionName, nVars]))
        self.writeLine(f"({functionName})")
        self.functionName = functionName  # mangle the label name with functionName
        for _ in range(int(nVars)):
            self.pushValue("0")

    # write assembly code that effects the call command
    def writeCall(self, functionName: str, nArgs: str) -> None:
        self.writeLine(" ".join(["//", "writeCall:", functionName, nArgs]))
        # generate return address label and push it to stack
        self.writeLine("// push return address to stack")
        mangled_label = f"{self.functionName}$ret.{self.returnCnt}"
        self.returnCnt += 1
        self.writeLine("@" + mangled_label)
        self.writeLine("D=A")
        self.pushD()
        # save LCL of the caller
        self.writeLine("// save LCL of the caller")
        self.pushReg("LCL")
        # save ARG of the caller
        self.writeLine("// save ARG of the caller")
        self.pushReg("ARG")
        # save THIS of the caller
        self.writeLine("// save THIS of the caller")
        self.pushReg("THIS")
        # save THAT of the caller
        self.writeLine("// save THAT of the caller")
        self.pushReg("THAT")
        # reposition ARG to SP - 5 - nArgs
        self.writeLine("// reposition ARG to SP - 5 - nArgs")
        self.writeLine("@SP")
        self.writeLine("D=M")
        self.writeLine("@5")
        self.writeLine("D=D-A")
        if int(nArgs):
            self.writeLine("@" + nArgs)
            self.writeLine("D=D-A")
        self.writeLine("@ARG")
        self.writeLine("M=D")
        # reposition LCL to SP
        self.writeLine("// reposition LCL to SP")
        self.move("SP", "LCL")
        # transfer control to the callee
        self.writeLine("// transfer control to the callee")
        self.writeLine("@" + functionName)
        self.writeLine("0;JMP")
        # injects the return address label here
        self.writeLine("// injects the return address label here")
        self.writeLine(f"({mangled_label})")

    # write assembly code that effects the return command
    def writeReturn(self) -> None:
        self.writeLine(" ".join(["//", "writeReturn"]))
        # assign LCL to R14 as the temporary variable
        self.writeLine("// assign LCL to R14 as the temporary variable")
        self.move("LCL", "R14")
        # save return address in R15
        self.writeLine("// save return address in R15")
        self.setReg("LCL", "-5", "R15")
        # reposition the return value for the caller
        self.writeLine("// reposition the return value for the caller")
        self.popD()
        self.writeLine("@ARG")
        self.writeLine("A=M")
        self.writeLine("M=D")
        self.writeLine("D=A")
        # reposition SP for the caller
        self.writeLine("// reposition SP for the caller")
        self.writeLine("@SP")
        self.writeLine("M=D+1")
        # restore THAT, THIS, ARG, LCL for the caller
        self.writeLine("// restore THAT for the caller")
        self.setReg("R14", "-1", "THAT")
        self.writeLine("// restore THIS for the caller")
        self.setReg("R14", "-2", "THIS")
        self.writeLine("// restore ARG for the caller")
        self.setReg("R14", "-3", "ARG")
        self.writeLine("// restore LCL for the caller")
        self.setReg("R14", "-4", "LCL")
        # goto the return address
        self.writeLine("// goto the return address")
        self.writeLine("@R15")
        self.writeLine("A=M")
        self.writeLine("0;JMP")

    # write bootstrap code at the beginning of HACK code
    def writeBootstrap(self):
        # stack initialization
        self.writeLine("// map stack on the host RAM from address 256 onward")
        self.setReg("", "256", "SP")
        # begin execution
        self.writeLine("// start executing with the OS function Sys.init")
        self.writeCall("Sys.init", "0")

    """
    a set of helper using A/M and D register
    serve as elemenary operation for VM code
    """

    def pushD(self) -> None:
        self.writeLine("@SP")
        self.writeLine("A=M")
        self.writeLine("M=D")
        self.writeLine("@SP")
        self.writeLine("M=M+1")

    def popD(self) -> None:
        self.writeLine("@SP")
        self.writeLine("AM=M-1")
        self.writeLine("D=M")

    def popA(self) -> None:
        self.writeLine("@SP")
        self.writeLine("AM=M-1")
        self.writeLine("A=M")

    def pushValue(self, value: str) -> None:
        self.writeLine("@" + value)
        self.writeLine("D=A")
        self.pushD()

    def pushReg(self, register: str) -> None:
        self.writeLine("@" + register)
        self.writeLine("D=M")
        self.pushD()

    def comparison(self, jumpInstruction: str) -> None:
        self.popD()
        self.popA()
        # each comparison command has two unique jump target
        self.TrueTarget = "PUSH_TRUE." + str(self.TrueCnt)
        self.afterTarget = "AFTER." + str(self.afterCnt)
        # mangle the jump target
        if self.functionName:
            self.TrueTarget = f"{self.functionName}${self.TrueTarget}"
            self.afterTarget = f"{self.functionName}${self.afterTarget}"
        self.TrueCnt += 1
        self.afterCnt += 1
        # simple jump hack code to determine whether push True(-1) of False(0)
        self.writeLine("D=A-D")
        self.writeLine("@" + self.TrueTarget)
        self.writeLine("D;" + jumpInstruction)
        self.pushValue("0")
        self.writeLine("@" + self.afterTarget)
        self.writeLine("0;JMP")
        self.writeLine(f"({self.TrueTarget})")
        # hack code can only assign -1 directly to D
        self.writeLine("D=-1")
        self.pushD()
        self.writeLine(f"({self.afterTarget})")

    # compute linear destination address and save it to R13
    def getAddress(self, segment: str, index: str) -> None:
        # translate static variable to assembly symbol, later allocated onward address 16 by assembler
        if segment == "16":
            self.writeLine(f"@{self.inputfile}.{index}")
            self.writeLine("D=A")
            self.writeLine("@R13")
            self.writeLine("M=D")
            return
        self.writeLine("@" + segment)
        if segment.isnumeric():
            # direct addressing: temp(3), pointer(5) -> segment + index
            self.writeLine("D=A")
        else:
            # linear addressing: LCL, ARG, THIS, THAT -> [segment] + index
            self.writeLine("D=M")
        # add/sub index, as HACK assembly do not suport @-1
        if int(index) >= 0:
            self.writeLine("@" + index)
            self.writeLine("D=D+A")
        else:
            self.writeLine("@" + index[1:])
            self.writeLine("D=D-A")
        # save to temporary register
        self.writeLine("@R13")
        self.writeLine("M=D")

    # read value stored at address R13 and store it to D
    def getValue(self) -> None:
        self.writeLine("@R13")
        self.writeLine("A=M")
        self.writeLine("D=M")

    # read value at segment+index and store it to segment register or directly assign index to register
    def setReg(self, segment: str, index: str, register: str) -> None:
        if segment:
            self.getAddress(segment, index)
            self.getValue()
            self.writeLine("@" + register)
            self.writeLine("M=D")
        else:
            self.writeLine("@" + index)
            self.writeLine("D=A")
            self.writeLine("@" + register)
            self.writeLine("M=D")

    # move the value of source register to destination register
    def move(self, src: str, dst: str) -> None:
        self.writeLine("@" + src)
        self.writeLine("D=M")
        self.writeLine("@" + dst)
        self.writeLine("M=D")

    def endLoop(self) -> None:
        self.writeLine("// end hack program with infinite loop")
        self.writeLine("(INF_LOOP)")
        self.writeLine("@INF_LOOP")
        self.writeLine("0;JMP")

    def close(self) -> None:
        self.file.close()
        print("Hack code saved to: ", self.outputfile)


if __name__ == "__main__":
    # parse commandline
    parser = argparse.ArgumentParser(
        description="Jack virtual machine's translator, from VM code to HACK assembly code"
    )
    parser.add_argument("input", help=".vm file or folder contains .vm files")
    parser.add_argument("-b", "--bootstrap", action="store_true", help="add bootstrap code at begins")
    parser.add_argument("-e", "--endloop", action="store_true", help="add infinite loop code at the end")
    input = parser.parse_args().input
    bootstrap = parser.parse_args().bootstrap
    endloop = parser.parse_args().endloop
    # start translation
    VMT = VMTranslator(input)
    VMT.translate(bootstrap, endloop)
