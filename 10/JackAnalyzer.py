#!/usr/bin/env python3

import argparse
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


# main program that sets up and invokes other two modules
class JackAnalyzer:
    # parse the commandline argument
    def __init__(self, input: str) -> None:
        # cmdline argument is a folder
        if os.path.isdir(input):
            self.inputfiles = [
                os.path.join(input, file)
                for file in list(
                    filter(lambda file: file.endswith(".jack"), os.listdir(input))
                )
            ]
        # cmdline argument is a file
        elif input:
            self.inputfiles = [input]

    # drive the syntax analysis process
    def analyze(self) -> None:
        for inputfile in self.inputfiles:
            outputfile = inputfile.replace(".jack", "T.xml.1")
            tokenizer = JackTokenizer(inputfile)
            outputstream = open(outputfile, "w")
            outputstream.write("<tokens>\n")
            while tokenizer.hasMoreTokens():
                tokenizer.advance()
                if tokenizer.tokentype == "KEYWORD":
                    outputstream.write(f"<keyword> {tokenizer.token} </keyword>\n")
                elif tokenizer.tokentype == "SYMBOL":
                    if tokenizer.token == "<":
                        outputstream.write("<symbol> &lt; </symbol>\n")
                    elif tokenizer.token == ">":
                        outputstream.write("<symbol> &gt; </symbol>\n")
                    elif tokenizer.token == '"':
                        outputstream.write("<symbol> &quot; </symbol>\n")
                    elif tokenizer.token == "&":
                        outputstream.write("<symbol> &amp; </symbol>\n")
                    else:
                        outputstream.write(f"<symbol> {tokenizer.token} </symbol>\n")
                elif tokenizer.tokentype == "INT_CONST":
                    outputstream.write(
                        f"<integerConstant> {tokenizer.token} </integerConstant>\n"
                    )
                elif tokenizer.tokentype == "STRING_CONST":
                    outputstream.write(
                        f"<stringConstant> {tokenizer.token} </stringConstant>\n"
                    )
                elif tokenizer.tokentype == "IDENTIFIER":
                    outputstream.write(
                        f"<identifier> {tokenizer.token} </identifier>\n"
                    )
            outputstream.write("</tokens>\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Jack lang syntax analyzer, for tokenizing and parsing Jack code"
    )
    parser.add_argument("input", help=".jack file or folder contains .jack files")
    input = parser.parse_args().input
    JA = JackAnalyzer(input)
    JA.analyze()
