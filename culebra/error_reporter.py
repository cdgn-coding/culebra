class ErrorReporter:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.split('\n')
    
    def report(self, token, message: str):
        """
        Reports an error with source code context, line number, and position indicator.
        
        Example output:
        Error at line 3:
        let x = 1 + ;
                    ^
        Unexpected token ';'
        """
        # Get line number (1-based) and position in line
        line_num = 1
        pos_in_line = token.pos
        
        # Count newlines to find the actual line number and position
        for i in range(token.pos):
            if i < len(self.source_code) and self.source_code[i] == '\n':
                line_num += 1
                pos_in_line = token.pos - (i + 1)
        
        # Get the line of code where the error occurred
        error_line = self.lines[line_num - 1]
        
        # Build the error message
        error = f"Error at line {line_num}:\n"
        error += f"{error_line}\n"
        error += " " * pos_in_line + "^\n"  # Position indicator
        error += message
        
        print(error)
        return error 