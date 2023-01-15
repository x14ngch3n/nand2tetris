@24575
D = A
@R0
M = D

(LOOP)
    @R0
    D = M
    @SCREEN
    D = D - A
    @END
    D;JLT
    @R0
    A = M
    M = -1
    @R0
    M = M - 1
    @LOOP
    0;JMP

(END)
@END
0;JMP
