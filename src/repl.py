import sys
import argparse
from typing import NoReturn
from src.lexer import Lexer
from src.token import TokenType
from src.parser import Parser

def print_welcome_message(mode: str) -> None:
    """Print the initial welcome message and instructions."""
    print(r"""
      /^\/^\
    _|__|  O|
\/     /~   \_/ \
 \____|__________/  \
        \_______      \
                `\     \                 \
                  |     |                  \
                 /      /                    \
                /     /                       \\
              /      /                         \ \
             /     /                            \  \
           /     /             _----_            \   \
          /     /           _-~      ~-_         |   |
         (      (        _-~    _--_    ~-_     _/   |
          \      ~-____-~    _-~    ~-_    ~-_-~    /
            ~-_           _-~          ~-_       _-~
               ~--______-~                ~-___-~
    """)
    print(f"Welcome to the Culebra {mode.capitalize()} REPL!")
    print("Type 'exit' or press Ctrl+D to quit")
    print("Enter your code:")

def process_lexer_input(text: str) -> bool:
    """Process input in lexer mode."""
    if text.lower().strip() == 'exit':
        print("Goodbye!")
        return False

    lexer = Lexer()
    tokens = lexer.tokenize(text)

    for token in tokens:
        if token.type != TokenType.EOF:
            print(token)

    return True

def process_parser_input(text: str) -> bool:
    """Process input in parser mode."""
    if text.lower().strip() == 'exit':
        print("Goodbye!")
        return False

    lexer = Lexer()
    parser = Parser(lexer.tokenize(text))
    program = parser.parse()
    
    if parser.errors:
        print("Parser Errors:")
        for error in parser.errors:
            print(f"\t{error}")
    else:
        print(program.pretty())

    return True

def repl(mode: str) -> NoReturn:
    """Run the REPL (Read-Eval-Print Loop)."""
    print_welcome_message(mode)
    process_func = process_lexer_input if mode == 'lexer' else process_parser_input

    while True:
        try:
            text = input(">>> ")
            if not process_func(text):
                break

        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received")
            continue
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)

def setup_argparse() -> argparse.ArgumentParser:
    """Setup command line argument parser."""
    parser = argparse.ArgumentParser(
        description='Culebra Language REPL',
        formatter_class=argparse.RawTextHelpFormatter
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('-l', '--lexer', action='store_true',
                          help='Run in lexer mode (shows tokens)')
    mode_group.add_argument('-p', '--parser', action='store_true',
                          help='Run in parser mode (shows AST)')
    return parser

def main() -> int:
    """Main entry point for the script."""
    try:
        arg_parser = setup_argparse()
        args = arg_parser.parse_args()

        if not (args.lexer or args.parser):
            arg_parser.print_help()
            return 0

        mode = 'lexer' if args.lexer else 'parser'
        repl(mode)
        return 0
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())