// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// R0 holds the current SCREEN register's address, from 16384(@SCREEN) to 24575

(LISTEN)
    // initial R0
    @24575
    D = A
    @R0
    M = D
    // listen to keyboard
    @KBD
    D = M
    @BLACK
    D;JNE
    @WHITE
    0;JMP

(BLACK)
    // interrupt by keyboard unpress
    @KBD
    D = M
    @LISTEN
    D;JEQ
    // check R0
    @R0
    D = M
    @SCREEN
    D = D - A
    @LISTEN
    D;JLT
    // write to screen
    @R0
    A = M
    M = -1
    @R0
    M = M - 1
    @BLACK
    0;JMP

(WHITE)
    // interrupt by keyboard press
    @KBD
    D = M
    @LISTEN
    D;JNE
    // check R0
    @R0
    D = M
    @SCREEN
    D = D - A
    @LISTEN
    D;JLT
    // write to screen
    @R0
    A = M
    M = 0
    @R0
    M = M - 1
    @WHITE
    0;JMP