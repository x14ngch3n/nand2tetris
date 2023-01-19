// map stack on the host RAM from address 256 onward
@256
D=A
@SP
M=D
// start executing with the OS function Sys.init
// writeCall: Sys.init 0
// push return address to stack
@$ret.0
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
@Sys.init
0;JMP
// injects the return address label here
($ret.0)
// writeFunction: Class1.set 0
(Class1.set)
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
// pop static 0
@Class1.0
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
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
// pop static 1
@Class1.1
D=A
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
// writeFunction: Class1.get 0
(Class1.get)
// push static 0
@Class1.0
D=A
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
// push static 1
@Class1.1
D=A
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
// writeFunction: Sys.init 0
(Sys.init)
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// writeCall: Class1.set 2
// push return address to stack
@Sys.init$ret.1
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
@2
D=D-A
@ARG
M=D
// reposition LCL to SP
@SP
D=M
@LCL
M=D
// transfer control to the callee
@Class1.set
0;JMP
// injects the return address label here
(Sys.init$ret.1)
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
// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// writeCall: Class2.set 2
// push return address to stack
@Sys.init$ret.2
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
@2
D=D-A
@ARG
M=D
// reposition LCL to SP
@SP
D=M
@LCL
M=D
// transfer control to the callee
@Class2.set
0;JMP
// injects the return address label here
(Sys.init$ret.2)
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
// writeCall: Class1.get 0
// push return address to stack
@Sys.init$ret.3
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
@Class1.get
0;JMP
// injects the return address label here
(Sys.init$ret.3)
// writeCall: Class2.get 0
// push return address to stack
@Sys.init$ret.4
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
@Class2.get
0;JMP
// injects the return address label here
(Sys.init$ret.4)
// writeLabel: Sys.init$WHILE
(Sys.init$WHILE)
// writeGoto: Sys.init$WHILE
@Sys.init$WHILE
0;JMP
// writeFunction: Class2.set 0
(Class2.set)
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
// pop static 0
@Class2.0
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
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
// pop static 1
@Class2.1
D=A
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
// writeFunction: Class2.get 0
(Class2.get)
// push static 0
@Class2.0
D=A
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
// push static 1
@Class2.1
D=A
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
