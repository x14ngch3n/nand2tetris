// writeFunction: SimpleFunction.test 2
// writeLabel: SimpleFunction.test
(SimpleFunction.test)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push local 0
@LCL
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
// push local 1
@LCL
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
// not
@SP
AM=M-1
D=M
D=!D
@SP
A=M
M=D
@SP
M=M+1
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
// writeReturn
// assign LCL to R14 as the temporary variable
@LCL
D=M
@R14
M=D
// save return address in R15
@LCL
D=M
@5
D=D-A
@R13
M=D
@R13
A=M
D=M
@R15
M=D
// reposition the return value for the caller
@SP
AM=M-1
D=M
@ARG
A=M
M=D
D=A
// reposition SP for the caller
@SP
M=D+1
// restore THAT for the caller
@R14
D=M
@1
D=D-A
@R13
M=D
@R13
A=M
D=M
@THAT
M=D
// restore THIS for the caller
@R14
D=M
@2
D=D-A
@R13
M=D
@R13
A=M
D=M
@THIS
M=D
// restore ARG for the caller
@R14
D=M
@3
D=D-A
@R13
M=D
@R13
A=M
D=M
@ARG
M=D
// restore LCL for the caller
@R14
D=M
@4
D=D-A
@R13
M=D
@R13
A=M
D=M
@LCL
M=D
// goto the return address
@R15
A=M
0;JMP
// end hack program with infinite loop
(INF_LOOP)
@INF_LOOP
0;JMP
