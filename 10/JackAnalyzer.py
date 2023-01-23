#!/usr/bin/env python3

import argparse
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


# main program that sets up and invokes other two modules
class JackAnalyzer:
    # parse the commandline argument
    def __init__(self) -> None:
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

    # drive the syntax analysis process, using the services of a JackTokenizer and a CompilationEngine
    def analyze(self) -> None:
        for inputfile in self.inputfiles:
            outputfile = inputfile.replace("jack", "xml")
            tokenizer = JackTokenizer(inputfile)
            engine = CompilationEngine(inputfile, outputfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Jack lang syntax analyzer, performs tokenizing and parsing for error-free Jack code"
    )
    parser.add_argument("input", help=".jack file or folder contains .jack files")
