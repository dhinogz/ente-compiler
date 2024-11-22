from sly import Lexer


class EnteLexer(Lexer):
    tokens = {
        # Identifiers and literals
        ID,  # identifier # type: ignore
        NUMBER,  # numeric literal # type: ignore
        FLOAT_NUMBER,  # float literal # type: ignore
        STRING,  # string literal # type: ignore
        # Operators
        PLUS,  # + # type: ignore
        MINUS,  # - # type: ignore
        MULTIPLY,  # * # type: ignore
        DIVIDE,  # / # type: ignore
        ASSIGN,  # = # type: ignore
        LESSER,  # < # type: ignore
        GREATER,  # > # type: ignore
        # Delimiters
        LPAREN,  # ( # type: ignore
        RPAREN,  # ) # type: ignore
        LBRACE,  # { # type: ignore
        RBRACE,  # } # type: ignore
        COLON,  # : # type: ignore
        SEMICOLON,  # ; # type: ignore
        COMMA,  # , # type: ignore
        # Keywords
        PROGRAM,  # 'program' # type: ignore
        MAIN,  # 'main' # type: ignore
        WRITE,  # 'write' # type: ignore
        INT,  # 'int' # type: ignore
        FLOAT,  # 'float' # type: ignore
        STRING,  # 'string' # type: ignore
        VAR,  # 'var' # type: ignore
        END,  # 'end' # type: ignore
        VOID,  # 'void' # type: ignore
        IF,  # 'if' # type: ignore
        ELSE,  # 'else' # type: ignore
        WHILE,  # 'while' # type: ignore
        DO,  # 'do' # type: ignore
    }

    # String containing ignored characters between tokens
    ignore = " \t"

    # Identifiers and literals
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    FLOAT_NUMBER = r"[-+]?[0-9]+\.[0-9]+([eE][-+]?[0-9]+)?"
    NUMBER = r"\d+"

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
    ID["program"] = PROGRAM  # type: ignore
    ID["main"] = MAIN  # type: ignore
    ID["write"] = WRITE  # type: ignore
    ID["int"] = INT  # type: ignore
    ID["float"] = FLOAT  # type: ignore

    ID["var"] = VAR  # type: ignore
    ID["end"] = END  # type: ignore
    ID["void"] = VOID  # type: ignore
    ID["if"] = IF  # type: ignore
    ID["else"] = ELSE  # type: ignore
    ID["while"] = WHILE  # type: ignore
    ID["do"] = DO  # type: ignore

    @_(r'"[^"]*"')  # type: ignore
    def STRING(self, t):
        # Strip the quotes from the string
        t.value = t.value[1:-1]
        return t

    @_(r"\n+")  # type: ignore
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):  # type: ignore
        print(f"Line {self.lineno-1}: Bad character {t.value[0]}")
        self.index += 1
