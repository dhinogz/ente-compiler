from sly import Lexer, Parser


# class EnteParser(Parser):
#     pass
#


class EnteLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {
        # Identifiers and literals
        ID,  # identifier
        NUMBER,  # numeric literal
        STRING,  # string literal
        # Operators
        PLUS,  # +
        MINUS,  # -
        TIMES,  # *
        DIVIDE,  # /
        ASSIGN,  # =
        LESSER,  # <
        GREATER,  # >
        # Delimiters
        LPAREN,  # (
        RPAREN,  # )
        LBRACE,  # {
        RBRACE,  # }
        LBRACKET,  # [
        RBRACKET,  # ]
        COLON,  # :
        SEMICOLON,  # ;
        COMMA,  # ,
        # Keywords
        PROGRAM,  # 'program'
        MAIN,  # 'main'
        PRINTF,  # 'printf'
        INT,  # 'int'
        FLOAT,  # 'float'
        VAR,  # 'var'
        END,  # 'end'
        VOID,  # 'void'
        IF,  # 'if'
        ELSE,  # 'else'
    }

    # String containing ignored characters between tokens
    ignore = " \t"

    # Identifiers and literals
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    NUMBER = r"\d+"

    # Operators
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    ASSIGN = r"="
    LESSER = r"<"
    GREATER = r">"

    # Delimiters
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACE = r"\{"
    RBRACE = r"\}"
    LBRACKET = r"\["
    RBRACKET = r"\]"
    COLON = r":"
    SEMICOLON = r";"
    COMMA = r","

    # Keywords
    ID["program"] = PROGRAM
    ID["main"] = MAIN
    ID["printf"] = PRINTF
    ID["int"] = INT
    ID["float"] = FLOAT
    ID["var"] = VAR
    ID["end"] = END
    ID["void"] = VOID
    ID["if"] = IF
    ID["else"] = ELSE

    @_(r'"[^"]*"')
    def STRING(self, t):
        # Strip the quotes from the string
        t.value = t.value[1:-1]
        return t

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print("Line %d: Bad character %r" % (self.lineno, t.value[0]))
        self.index += 1


if __name__ == "__main__":
    data = "x = 3 + 42 * (s - t)"
    lexer = EnteLexer()
    for tok in lexer.tokenize(data):
        print("type=%r, value=%r" % (tok.type, tok.value))
