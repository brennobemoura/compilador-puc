import sys
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Interpreter.Interpreter import Interpreter
from Lexer.LexerHash import LexerHash
from Lexer.LexerQueue import LexerQueue
from Assembler.Assembler import Assembler

from Assembler.ACompiler import ACompiler

for arg in sys.argv:
    if arg == "-asm":
        ACompiler.compile()
        quit()

Lexer.run(sys.argv)
instructions = Parser.run()
Interpreter.run(instructions)

for arg in sys.argv:
    if arg == "-v":
        print("Tabela de variáveis")
        LexerHash.shared().verbose()

        print("\nLista de instruções")
        LexerQueue.shared().verbose()

        print("\nLista de Instruções (Parser)")
        instructions.copy().verbose(showContent=False)

Assembler.run(instructions).toFile(sys.argv)
ACompiler.compile()