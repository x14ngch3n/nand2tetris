#!/opt/homebrew/bin/python3

import sys


class Code:

    def __init__(self) -> None:
        # initialize translate dictionary, mind that the code is read from right to left, AKA big endian
        self.dest_dict = {
            'M': 2,
            'D': 1,
            'A': 0,
        }
        self.comp_dict = {
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            'M': '1110000',
            '!D': '0001101',
            '!A': '0110001',
            '!M': '1110001',
            '-D': '0001111',
            '-A': '0110011',
            '-M': '1110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'M+1': '1110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'M-1': '1110010',
            'D+A': '0000010',
            'D+M': '1000010',
            'D-A': '0010011',
            'D-M': '1010011',
            'A-D': '0000111',
            'M-D': '1000111',
            'D&A': '0000000',
            'D&M': '1000000',
            'D|A': '0010101',
            'D|M': '1010101',
        }
        self.jump_dict = {
            'null': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }

    # convert comp field to binary code
    def comp(self, symbol):
        return self.comp_dict[symbol]

    # convert dest field to binary code
    def dest(self, symbol):
        code = ['0', '0', '0']
        if symbol == 'null':
            return ''.join(code)
        for d, i in self.dest_dict.items():
            if d in symbol:
                code[i] = '1'
        return ''.join(code)

    # convert jump field to binary code
    def jump(self, symbol):
        return self.jump_dict[symbol]


class Parser:

    def __init__(self, inputfile) -> None:
        self.file = open(inputfile, 'r')
        self.curr_line = ''
        self.curr_instruction = ''
        self.curr_instructionType = ''

    # check if new line exists in file stream and get it
    def hasMoreLines(self):
        # get new line from file stream
        self.curr_line = self.file.readline()
        return True if self.curr_line else False

    # trim useless blank space and comment
    def advance(self):
        # trim newline, space and tab
        self.curr_instruction = self.curr_line.strip()
        # trim inline comment
        dash = self.curr_instruction.find('//')
        self.curr_instruction = self.curr_instruction[:
                                                      dash] if dash > 0 else self.curr_instruction
        print(self.curr_instruction)

    # get the instruction's type
    def instructionType(self):
        # comment
        if self.curr_instruction.startswith('//'):
            self.curr_instructionType = 'COMMENT'
        # blank line
        elif self.curr_instruction == '':
            self.curr_instructionType = 'BLANK'
        # A_INSTRUCTION
        elif self.curr_instruction.startswith('@'):
            self.curr_instructionType = 'A_INSTRUCTION'
        # C_INSTRUCTION
        elif '=' in self.curr_instruction or ';' in self.curr_instruction:
            self.curr_instructionType = 'C_INSTRUCTION'
        # L_INSTRUCTION
        elif self.curr_instruction.startswith(
                '(') and self.curr_instruction.endswith(')'):
            self.curr_instructionType = 'L_INSTRUCTION'
        # other cases
        else:
            self.curr_instructionType = ''
        print('type:', self.curr_instructionType)

    # get symbol in instruction
    def symbol(self):
        # @xxx
        if self.curr_instructionType == 'A_INSTRUCTION':
            return self.curr_instruction[1:]
        # (xxx)
        elif self.curr_instructionType == 'L_INSTRUCTION':
            return self.curr_instruction[1:-1]
        # instrcution not contains symbol
        else:
            pass

    # distract comp fields from current instruction
    def comp(self):
        equal = self.curr_instruction.find('=')
        column = self.curr_instruction.find(';')
        return self.curr_instruction[
            equal + 1:] if column == -1 else self.curr_instruction[equal +
                                                                   1:column]

    # distract dest fields from current instruction
    def dest(self):
        if '=' not in self.curr_instruction:
            return 'null'
        return self.curr_instruction[:self.curr_instruction.find('=')]

    # distract jump fields from current instruction
    def jump(self):
        if ';' not in self.curr_instruction:
            return 'null'
        return self.curr_instruction[self.curr_instruction.find(';') + 1:]


class Assembler:

    def __init__(self, inputfile) -> None:
        # file operation
        self.inputfile = inputfile
        self.outputfile = self.inputfile.replace('asm', 'hack')
        # initial symbol table with predefined symbol
        self.symbol_table = {
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'SCREEN': 16384,
            'KBD': 24576,
        }
        # address track
        self.rom_addr = 0
        self.ram_addr = 16

    # assemble .asm to .hack
    def assemble(self):
        self.file = open(self.outputfile, 'w')
        self.first_pass()
        self.second_pass()
        self.file.close()
        print('binary code saved to: ', self.outputfile)

    # parse L_INSTRUCTION symbol
    def L_pass(self):
        P = Parser(self.inputfile)
        while P.hasMoreLines():
            P.advance()
            P.instructionType()
            symbol = P.symbol()
            if P.curr_instructionType == 'L_INSTRUCTION':
                # bind label symbol to next rom address
                self.addEntry(symbol, self.rom_addr)
            elif P.curr_instructionType == 'A_INSTRUCTION' or P.curr_instructionType == 'C_INSTRUCTION':
                self.rom_addr += 1

    # parse A_INSTRUCTION symbol
    def A_pass(self):
        P = Parser(self.inputfile)
        while P.hasMoreLines():
            P.advance()
            P.instructionType()
            symbol = P.symbol()
            if P.curr_instructionType == 'A_INSTRUCTION':
                # bind variable symbol to next ram address for first appearence
                if not symbol.isdigit() and not self.contains(symbol):
                    self.addEntry(symbol, self.ram_addr)
                    self.ram_addr += 1

    # first pass of assemble, aim to construct symbol table
    def first_pass(self):
        self.L_pass()
        self.A_pass()
        # dump symbol table
        self.symbolfile = self.inputfile.replace('asm', 'sym')
        with open(self.symbolfile, 'w') as f:
            for i in self.symbol_table.items():
                f.write(str(i) + '\n')

    # second pass of assemble, aim to parse each line
    def second_pass(self):
        P = Parser(self.inputfile)
        while P.hasMoreLines():
            P.advance()
            P.instructionType()
            if P.curr_instructionType == 'A_INSTRUCTION':
                symbol = P.symbol()
                # get symbol address
                if not symbol.isdigit():
                    number = self.getAddress(symbol)
                else:
                    number = int(symbol)
                # convert to binary format
                code = bin(number)[2:].rjust(16, '0') + '\n'
                self.file.write(code)
            elif P.curr_instructionType == 'C_INSTRUCTION':
                # construct code by fields
                code = '111'
                C = Code()
                code += C.comp(P.comp())
                code += C.dest(P.dest())
                code += C.jump(P.jump())
                code += '\n'
                self.file.write(code)
            # skip L_INSTRUCTION, comment and blank for second pass
            else:
                assert P.curr_instructionType, 'not valid instruction type'

    def addEntry(self, symbol, address):
        self.symbol_table.update({symbol: address})

    def contains(self, symbol):
        return symbol in self.symbol_table.keys()

    def getAddress(self, symbol):
        return self.symbol_table[symbol]


if __name__ == '__main__':
    assert sys.argv[1].endswith(
        '.asm'), 'input filename must contain .asm extension'
    A = Assembler(sys.argv[1])
    A.assemble()
