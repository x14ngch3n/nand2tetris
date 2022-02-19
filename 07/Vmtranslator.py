#!/opt/homebrew/bin/python3

import sys


# drive the translation process
class VMTranslator():

    def __init__(self, inputfile) -> None:
        self.inputfile = inputfile
        self.outputfile = self.inputfile.replace('vm', 'asm')

    def translate(self):
        P = Parser(self.inputfile)
        C = CodeWriter(self.outputfile)
        # C.initMemory()
        while P.hasMoreLines():
            P.advance()
            self.command_type = P.commandType()
            self.arg1, self.arg2 = P.arg1(self.command_type), P.arg2(
                self.command_type)
            if self.command_type == 'C_ARITHMETIC':
                C.writeArithmetic(self.arg1)
            elif self.command_type == 'C_PUSH':
                C.writePushPop('push', self.arg1, self.arg2)
            elif self.command_type == 'C_POP':
                C.writePushPop('pop', self.arg1, self.arg2)

        C.endLoop()
        C.close()


# understand what the command seek to do
class Parser():

    def __init__(self, inputfile) -> None:
        self.file = open(inputfile, 'r')
        self.arithmetic_commands = ['add', 'sub', 'neg']
        self.comparison_commands = ['eq', 'gt', 'lt']
        self.logical_commands = ['and', 'or', 'not']

    # check if new line exists in file stream and get it
    def hasMoreLines(self) -> bool:
        # get new line from file stream
        self.curr_line = self.file.readline()
        return True if self.curr_line else False

    # trim useless blank space and comment
    def advance(self):
        # trim newline, space and tab
        self.curr_command = self.curr_line.strip()
        # trim inline comment
        dash = self.curr_command.find('//')
        self.curr_command = self.curr_command[:dash] if dash > 0 else self.curr_command

    # get current command's type
    def commandType(self) -> str:
        # comment
        if self.curr_command.startswith('//'):
            return 'COMMENT'
        # blank
        elif self.curr_command == '':
            return 'BLANK'
        # C type command
        self.tokens = self.curr_command.split(' ')
        # Arithmetic-Logical Commands
        if self.tokens[0] in self.arithmetic_commands or self.tokens[
                0] in self.comparison_commands or self.tokens[
                    0] in self.logical_commands:
            return 'C_ARITHMETIC'
        # Push/Pop Commands
        elif self.tokens[0] == 'push':
            return 'C_PUSH'
        elif self.tokens[0] == 'pop':
            return 'C_POP'

    # returns the first argument of current command
    def arg1(self, type) -> str:
        if type == 'C_ARITHMETIC':
            return self.tokens[0]
        elif type in ['C_PUSH', 'C_POP']:
            return self.tokens[1]

    # returns the second argument of current command
    def arg2(self, type) -> str:
        if type in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
            return self.tokens[2]


# translate understood command to desired operation in hack lang
class CodeWriter():

    def __init__(self, outputfile) -> None:
        self.outputfile = outputfile
        self.file = open(self.outputfile, 'w')
        self.segmentMap = {
            # segmantation register, support index
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            # pointer 0 -> THIS, pointer 1 -> THAT
            'pointer': '3',
            'temp': '5',
            # reserve for temporary variables
            'R13': '13',
            'R14': '14',
            'R15': '15',
            # static i for i in range(240)
            'static': '16',
        }
        self.pushTrueCnt = 0
        self.afterCnt = 0
        self.comparison_dict = {
            'eq': 'JEQ',
            'gt': 'JGT',
            'lt': 'JLT',
        }

    # write one-line hack code to output file
    def writeLine(self, line):
        self.file.write(line)
        self.file.write('\n')

    # write to outputfile the hack code that implements the given arithmetic-logical command
    def writeArithmetic(self, command):
        comment = ' '.join(['//', command])
        self.writeLine(comment)
        if command == 'add':
            self.popD()
            self.popA()
            self.writeLine('D=D+A')
            self.pushD()
        elif command == 'sub':
            self.popD()
            self.popA()
            self.writeLine('AD=A-D')
            self.pushD()
        elif command == 'neg':
            self.popD()
            self.writeLine('D=-D')
            self.pushD()
        elif command in ['eq', 'gt', 'lt']:
            self.comparison(self.comparison_dict[command])
        elif command == 'and':
            self.popD()
            self.popA()
            self.writeLine('D=D&A')
            self.pushD()
        elif command == 'or':
            self.popD()
            self.popA()
            self.writeLine('D=D|A')
            self.pushD()
        elif command == 'not':
            self.popD()
            self.writeLine('D=!D')
            self.pushD()

    # write to outputfile the hack code that implements the given push/pop command
    def writePushPop(self, command, segment, index):
        comment = ' '.join(['//', command, segment, index])
        self.writeLine(comment)
        if command == 'push':
            if segment == 'constant':
                self.pushValue(index)
            else:
                self.argParse(segment, index)
                self.writeLine('@R13')
                self.writeLine('A=M')
                self.writeLine('D=M')
                self.pushD()
        elif command == 'pop':
            self.argParse(segment, index)
            self.popD()
            # retrive dest from @R13, avoiding D register's conflict
            self.writeLine('@R13')
            self.writeLine('A=M')
            self.writeLine('M=D')

    '''
    a set of helper methods using A/M and D register
    '''

    def initMemory(self):
        self.initSegment('SP', 256)
        self.initSegment('LCL', 300)
        self.initSegment('ARG', 400)
        self.initSegment('THIS', 3000)
        self.initSegment('THAT', 3010)

    def initSegment(self, name, value):
        self.writeLine('// initialize ' + name + ' segment to ' + str(value))
        self.writeLine('@' + str(value))
        self.writeLine('D=A')
        self.writeLine('@' + name)
        self.writeLine('M=D')

    def pushD(self):
        self.writeLine('@SP')
        self.writeLine('A=M')
        self.writeLine('M=D')
        self.writeLine('@SP')
        self.writeLine('M=M+1')

    def popD(self):
        self.writeLine('@SP')
        self.writeLine('AM=M-1')
        self.writeLine('D=M')

    def popA(self):
        self.writeLine('@SP')
        self.writeLine('AM=M-1')
        self.writeLine('A=M')

    def pushValue(self, value):
        self.writeLine('@' + str(value))
        self.writeLine('D=A')
        self.pushD()

    def comparison(self, jumpType):
        self.popD()
        self.popA()
        # unique label for each comparison command
        self.pushTrueName = 'PUSH_TRUE.' + str(self.pushTrueCnt)
        self.afterName = 'AFTER.' + str(self.afterCnt)
        self.pushTrueCnt += 1
        self.afterCnt += 1
        # simple jump hack code to determine whether push True(-1) of False(0)
        self.writeLine('D=A-D')
        self.writeLine('@' + self.pushTrueName)
        self.writeLine('D;' + jumpType)
        self.pushValue(0)
        self.writeLine('@' + self.afterName)
        self.writeLine('0;JMP')
        self.writeLine('(' + self.pushTrueName + ')')
        # hack code don't support @-1
        self.writeLine('D=-1')
        self.pushD()
        self.writeLine('(' + self.afterName + ')')

    # save computed dest addr to D and R13
    def argParse(self, segment, index):
        self.writeLine('@' + self.segmentMap[segment])
        # direct addressing: temp, pointer
        # indirect addressing: local,argument,this,that
        self.writeLine('D=A') if segment in ['temp', 'pointer', 'static'
                                             ] else self.writeLine('D=M')
        self.writeLine('@' + index)
        self.writeLine('D=D+A')
        # save to temporary regisƒter
        self.writeLine('@R13')
        self.writeLine('M=D')

    def endLoop(self):
        self.writeLine('// end hack program with infinite loop')
        self.writeLine('(END_LOOP)')
        self.writeLine('@END_LOOP')
        self.writeLine('0;JMP')

    def close(self):
        self.file.close()
        print('Hack code saved to: ', self.outputfile)


if __name__ == '__main__':
    assert sys.argv[1].endswith(
        '.vm'), 'input filename must contain .vm extension'
    assert sys.argv[1][0].isupper(
    ), 'input filename must begin with UPPERCASE letter'
    VMT = VMTranslator(sys.argv[1])
    VMT.translate()
