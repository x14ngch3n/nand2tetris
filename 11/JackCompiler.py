#!/usr/bin/env python3

import argparse
import os

from CompilationEngine import CompilationEngine


# main program that sets up and invokes other two modules
class JackCompiler:
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
    def compile(self) -> None:
        for inputfile in self.inputfiles:
            outputfile = inputfile.replace("jack", "xml")
            engine = CompilationEngine(inputfile, outputfile)
            engine.compileClass()
            engine.writeXml()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Jack lang compiler, generating VM code"
    )
    parser.add_argument("input", help=".jack file or folder contains .jack files")
    input = parser.parse_args().input
    JC = JackCompiler(input)
    JC.compile()
