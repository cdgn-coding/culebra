import sys
import argparse
from typing import NoReturn
from culebra.lexer import Lexer
from culebra.token import TokenType
from culebra.parser import Parser


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
    print("Type 'exit' on a new line or press Ctrl+D to quit")
    print("Enter your code (press Enter twice to execute):")


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

    # Convert tab indentation to 4 spaces for the parser.
    text = text.replace("\t", "    ")

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


def multiline_input(prompt=">>> ") -> str:
    """Allows multi-line input until an empty line is encountered, with auto-indentation.
    
    If a line ends with a ':' character, the next input prompt will be indented with a tab.
    """
    lines = []
    current_indent = ""
    current_prompt = prompt + current_indent  # initial prompt e.g. ">>> "
    while True:
        try:
            line = input(current_prompt)
            if line.strip() == "exit":
                return "exit"
            if line == "":
                break
            # Append the line with the current indentation.
            lines.append(current_indent + line)
            # If the trimmed line ends with ':', increase the indentation (adds one tab).
            if line.rstrip().endswith(':'):
                current_indent += "\t"
            # Update the prompt for the next line to include the current indentation.
            current_prompt = "... " + current_indent
        except EOFError:
            print("\nGoodbye!")
            return "exit"
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received")
            return "exit"
    return "\n".join(lines)


def repl(mode: str) -> NoReturn:
    """Run the REPL (Read-Eval-Print Loop)."""
    print_welcome_message(mode)
    process_func = process_lexer_input if mode == 'lexer' else process_parser_input

    while True:
        text = multiline_input()
        if text == "exit":
            break
        process_func(text)


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
