from sly import Parser
from lexer import EnteLexer
from symbol_table import SymbolTable, Symbol
from quadruples import QuadrupleManager


class EnteParser(Parser):
    tokens = EnteLexer.tokens

    precedence = (
        ("left", PLUS, MINUS),
        ("left", MULTIPLY, DIVIDE),
    )
    debugfile = "parser.out"

    def __init__(self):
        super().__init__()
        self.quadruples = QuadrupleManager()
        self.scope = []
        self.directory = {}
        self.types = {}

    @_("PROGRAM prog_init SEMICOLON global_scope seen_global main END SEMICOLON")
    def root(self, p):
        return (f"root {p[1]}", p[3], p[5])

    ########################
    # Initialize a program #
    ########################
    @_("ID")
    def prog_init(self, p):
        # init function symbol table
        # init quadruples
        self.quadruples.add("GOTO", -1, -1, -1)
        # TODO: init jump stack

        scope = "global"
        self.scope.append(scope)
        self.directory[scope] = []
        self.types[scope] = []

        return p[0]

    ##########
    # Global #
    ##########
    @_("vars funcs")
    def global_scope(self, p):
        return p

    @_("")
    def seen_global(self, p):
        print("done with global")
        self.scope.pop()
        return p

    #############
    # Variables #
    #############
    @_(
        "VAR vars_declare",
        "empty",
    )
    def vars(self, p):
        return p

    @_(
        "var_list COLON var_type SEMICOLON",
        "var_list COLON var_type SEMICOLON vars_declare",
    )
    def vars_declare(self, p):
        return p

    @_("ID", "ID COMMA var_list")
    def var_list(self, p):
        curr_scope = self.scope[-1] if self.scope else "global"
        self.directory[curr_scope].append(p[0])

        return p

    @_("INT", "FLOAT")
    def var_type(self, p):
        curr_scope = self.scope[-1] if self.scope else "global"
        self.types[curr_scope].append(p[0])

        return p

    #############
    # Functions #
    #############
    @_("ID COLON var_type", "ID COLON var_type COMMA params")
    def params(self, p):
        curr_scope = self.scope[-1] if self.scope else "global"
        self.directory[curr_scope].append(p[0])

        return p

    @_("")
    def at_params(self, p):
        func = p[-2]
        scope = "params"
        self.scope.append(scope)
        self.directory[scope] = []
        self.types[scope] = []
        return p

    @_("")
    def seen_params(self, p):
        self.scope.pop()

    @_(
        "VOID ID LPAREN at_params params seen_params RPAREN LBRACE at_func block seen_func RBRACE SEMICOLON",
        "empty",
    )
    def funcs(self, p):
        return p

    @_("")
    def at_func(self, p):
        scope = p[-7]
        self.scope.append(scope)
        self.directory[scope] = []
        self.types[scope] = []

    @_("")
    def seen_func(self, p):
        self.scope.pop()

    ########
    # Main #
    ########
    @_("MAIN LBRACE at_main block seen_main RBRACE SEMICOLON", "empty")
    def main(self, p):
        return p

    @_("")
    def at_main(self, p):
        scope = "main"
        self.scope.append(scope)
        self.directory[scope] = []
        self.types[scope] = []

    @_("")
    def seen_main(self, p):
        self.scope.pop()

    #########
    # Block #
    #########
    @_("vars statements")
    def block(self, p):
        return p

    ##############
    # Statements #
    ##############
    @_("statement SEMICOLON statements", "empty")
    def statements(self, p):
        return p

    @_(
        "assign",
        "write",
        "condition",
        "loop",
        "do_while",
        "block",
    )
    def statement(self, p):
        return p[0]

    @_("LET ID ASSIGN expression")
    def assign(self, p):
        return p

    @_("WHILE LPAREN expression RPAREN LBRACE block RBRACE")
    def loop(self, p):
        return p

    @_("WRITE LPAREN expression RPAREN")
    def write(self, p):
        return p

    @_("IF LPAREN expression RPAREN LBRACE block RBRACE else_condition")
    def condition(self, p):
        return p

    @_("ELSE LBRACE block RBRACE", "empty")
    def else_condition(self, p):
        return p

    @_("DO LBRACE block RBRACE WHILE LPAREN expression RPAREN")
    def do_while(self, p):
        return p

    ################################################
    # Expression -> Exp -> Term -> Factor -> Const #
    ################################################
    @_("exp", "exp LESSER exp", "exp GREATER exp")
    def expression(self, p):
        return p

    @_("term exp_operator")
    def exp(self, p):
        return p

    @_("PLUS exp", "MINUS exp", "empty")
    def exp_operator(self, p):
        return p

    @_("factor term_operator")
    def term(self, p):
        return p

    @_("MULTIPLY term", "DIVIDE term", "empty")
    def term_operator(self, p):
        return p

    @_("LPAREN expression RPAREN", "const")
    def factor(self, p):
        return p

    @_("PLUS NUMBER", "MINUS NUMBER", "PLUS ID", "MINUS ID", "NUMBER", "STRING", "ID")
    def const(self, p):
        return p

    #########
    # Empty #
    #########
    @_("")
    def empty(self, p):
        pass
