from sly import Parser
from lexer import EnteLexer
from symbol_table import SymbolTable, Symbol
from quadruples import QuadrupleManager


class EnteParser(Parser):
    tokens = EnteLexer.tokens

    def __init__(self):
        super().__init__()
        self.quadruples = QuadrupleManager()

    @_("PROGRAM ID SEMICOLON var_declarations END")
    def prog(self, p):
        # init function symbol table
        self.func_dir = SymbolTable()
        # init quadruples
        self.quadruples.add("GOTO", -1, -1, -1)
        # TODO: init jump stack

        # init global function table
        self.func_dir.declare(
            Symbol(name=p[1], type="table.global", child=SymbolTable())
        )

    @_(
        "VAR variables COLON var_type SEMICOLON",
        "VAR variables COLON var_type SEMICOLON var_declarations",
        "empty",
    )
    def var_declarations(self, p):
        return p[1]

    @_("ID", "ID COMMA variables")
    def variables(self, p):
        # TODO: init local scope if it doesnt exist
        return p[0]

    @_("INT", "FLOAT")
    def var_type(self, p):
        return p[0]

    @_("")
    def empty(self, p):
        pass
