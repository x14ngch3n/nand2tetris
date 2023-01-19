// writeFunction: Sys.init 0
(Sys.init)
// push constant 4000	
@4000	
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@3
D=A
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
// push constant 5000
@5000
D=A
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
// writeCall: Sys.main 0
// push return address to stack
@Sys.init$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
// save LCL of the caller
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// save ARG of the caller
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// save THIS of the caller
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// save THAT of the caller
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reposition ARG to SP - 5 - nArgs
@SP
D=M
@5
D=D-A
@ARG
M=D
// reposition LCL to SP
@SP
D=M
@LCL
M=D
// transfer control to the callee
@Sys.main
0;JMP
// injects the return address label here
(Sys.init$ret.0)
// pop temp 1
@5
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
// writeLabel: Sys.init$LOOP
(Sys.init$LOOP)
// writeGoto: Sys.init$LOOP
@Sys.init$LOOP
0;JMP
// writeFunction: Sys.main 5
(Sys.main)
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
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@3
D=A
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
// push constant 5001
@5001
D=A
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
// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 1
@LCL
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
// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 2
@LCL
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
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 3
@LCL
D=M
@3
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// writeCall: Sys.add12 1
// push return address to stack
@Sys.main$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
// save LCL of the caller
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// save ARG of the caller
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// save THIS of the caller
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// save THAT of the caller
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reposition ARG to SP - 5 - nArgs
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// reposition LCL to SP
@SP
D=M
@LCL
M=D
// transfer control to the callee
@Sys.add12
0;JMP
// injects the return address label here
(Sys.main$ret.1)
// pop temp 0
@5
D=A
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
// push local 2
@LCL
D=M
@2
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
// push local 3
@LCL
D=M
@3
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
// push local 4
@LCL
D=M
@4
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
// writeFunction: Sys.add12 0
(Sys.add12)
// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@3
D=A
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
// push constant 5002
@5002
D=A
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
// push constant 12
@12
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
