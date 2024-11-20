from sly import Lexer


class EnteLexer(Lexer):
    tokens = {
        # Identifiers and literals
        ID,  # identifier
        NUMBER,  # numeric literal
        STRING,  # string literal
        # Operators
        PLUS,  # +
        MINUS,  # -
        MULTIPLY,  # *
        DIVIDE,  # /
        ASSIGN,  # =
        LESSER,  # <
        GREATER,  # >
        # Delimiters
        LPAREN,  # (
        RPAREN,  # )
        LBRACE,  # {
        RBRACE,  # }
        COLON,  # :
        SEMICOLON,  # ;
        COMMA,  # ,
        # Keywords
        PROGRAM,  # 'program'
        MAIN,  # 'main'
        WRITE,  # 'write'
        INT,  # 'int'
        FLOAT,  # 'float'
        STRING,  # 'string'
        VAR,  # 'var'
        END,  # 'end'
        VOID,  # 'void'
        IF,  # 'if'
        ELSE,  # 'else'
        WHILE,  # 'while'
        DO,  # 'do'
        LET, # 'let'
    }

    # String containing ignored characters between tokens
    ignore = " \t"

    # Identifiers and literals
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    NUMBER = r"\d+"
    # NUMBER = r"\d+(\.\d+)?"

    # Operators
    PLUS = r"\+"
    MINUS = r"-"
    MULTIPLY = r"\*"
    DIVIDE = r"/"
    ASSIGN = r"="

    LESSER = r"<"
    GREATER = r">"

    # Delimiters
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACE = r"\{"
    RBRACE = r"\}"
    COLON = r":"
    SEMICOLON = r";"
    COMMA = r","

    # Keywords
    ID["program"] = PROGRAM
    ID["main"] = MAIN
    ID["write"] = WRITE
    ID["int"] = INT
    ID["float"] = FLOAT

    ID["var"] = VAR
    ID["end"] = END
    ID["void"] = VOID
    ID["if"] = IF
    ID["else"] = ELSE
    ID["while"] = WHILE
    ID["do"] = DO
    ID["let"] = LET

    @_(r'"[^"]*"')
    def STRING(self, t):
        # Strip the quotes from the string
        t.value = t.value[1:-1]
        return t

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print(f"Line {self.lineno-1}: Bad character {t.value[0]}")
        self.index += 1
