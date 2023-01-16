// initialize SP segment to 256
@256
D=A
@SP
M=D
// initialize LCL segment to 300
@300
D=A
@LCL
M=D
// initialize ARG segment to 400
@400
D=A
@ARG
M=D
// initialize THIS segment to 3000
@3000
D=A
@THIS
M=D
// initialize THAT segment to 3010
@3010
D=A
@THAT
M=D
// push argument 1
@ARG
D=M
@1
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@3
D=A
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 0
@THAT
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 1
@THAT
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
@SP
AM=M-1
A=M
AD=A-D
@SP
A=M
M=D
@SP
M=M+1
// pop argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// writeLabel: MAIN_LOOP_START
(MAIN_LOOP_START)
// push argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// writeIf: COMPUTE_ELEMENT
@SP
AM=M-1
D=M
@COMPUTE_ELEMENT
D;JNE
// writeGoto: END_PROGRAM
@END_PROGRAM
0;JMP
// writeLabel: COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
// push that 0
@THAT
D=M
@0
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1
@THAT
D=M
@1
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
@SP
AM=M-1
A=M
D=D+A
@SP
A=M
M=D
@SP
M=M+1
// pop that 2
@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push pointer 1
@3
D=A
@1
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
@SP
AM=M-1
A=M
D=D+A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@3
D=A
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
@SP
AM=M-1
A=M
AD=A-D
@SP
A=M
M=D
@SP
M=M+1
// pop argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// writeGoto: MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP
// writeLabel: END_PROGRAM
(END_PROGRAM)
// end hack program with infinite loop
(END_LOOP)
@END_LOOP
0;JMP
