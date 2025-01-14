from unittest import TestCase

class TestLexer(TestCase):
    def test_lexer(self):
        lexer = Lexer()
        self.assertEqual(lexer.next_token("1 + 2"), Token(TokenType.NUMBER, "1"))
