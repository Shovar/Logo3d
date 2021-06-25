import sys
from antlr4 import *
from logo3dLexer import logo3dLexer
from logo3dParser import logo3dParser
from visitor import EvalVisitor


input_stream = FileStream(sys.argv[1])
lexer = logo3dLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = logo3dParser(token_stream)

tree = parser.root()

if len(sys.argv) == 2:
    vis = EvalVisitor([])
else:
    tam = len(sys.argv)
    vis = EvalVisitor(sys.argv[2:tam])
vis.visit(tree)
