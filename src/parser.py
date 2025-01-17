from src.lexer import Lexer
from src.ast import Program

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def parse(self, text: str) -> Program:
        program = Program([])
        return program
