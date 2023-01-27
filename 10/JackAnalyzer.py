#!/usr/bin/env python3

import argparse
import os
import xml.etree.ElementTree as ET

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
            xmldata = ET.Element("tokens")
            while tokenizer.hasMoreTokens():
                tokenizer.advance()
                if tokenizer.tokentype == "KEYWORD":
                    token = ET.SubElement(xmldata, "keyword")
                    token.text = tokenizer.token
                elif tokenizer.tokentype == "SYMBOL":
                    token = ET.SubElement(xmldata, "symbol")
                    token.text = tokenizer.token
                elif tokenizer.tokentype == "INT_CONST":
                    token = ET.SubElement(xmldata, "integerConstant")
                    token.text = tokenizer.token
                elif tokenizer.tokentype == "STRING_CONST":
                    token = ET.SubElement(xmldata, "stringConstant")
                    token.text = tokenizer.token
                elif tokenizer.tokentype == "IDENTIFIER":
                    token = ET.SubElement(xmldata, "identifier")
                    token.text = tokenizer.token
            ET.indent(xmldata)
            with open(outputfile, "w") as f:
                f.writelines(ET.tostringlist(xmldata, encoding="unicode"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Jack lang syntax analyzer, for tokenizing and parsing Jack code"
    )
    parser.add_argument("input", help=".jack file or folder contains .jack files")
    input = parser.parse_args().input
    JA = JackAnalyzer(input)
    JA.analyze()
