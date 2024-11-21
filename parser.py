from sly import Parser
from lexer import EnteLexer
from memory import MemoryAssigner
from operators import Operator as Op

# TODO: from symbol_table import SymbolTable, Symbol
from quadruples import QuadrupleManager
from semantics import validate_semantics
from stack import Stack


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

        # Stacks for quadruple building
        self.operands = Stack("operands")
        self.operand_types = Stack("operand_types")
        self.operators = Stack("operators")

        self.memory_assigner: MemoryAssigner = MemoryAssigner()

    ########
    # Root #
    ########
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
        if self.scope:
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
        "LBRACE block RBRACE",
    )
    def statement(self, p):
        return p[0]

    @_("ID ASSIGN in_assign expression")
    def assign(self, p):
        if not self.operators.is_empty() and self.operators.peek() == Op.ASSIGN:
            operator = self.operators.pop()

            right_operand = self.operands.pop()
            right_type = self.operand_types.pop()

            left_operand = self.operands.pop()
            left_type = self.operand_types.pop()

            # validate semantics here
            result_type = validate_semantics(left_type, right_type, operator)
            if result_type == "error":
                raise Exception(
                    f"type mismatch: {left_operand} {operator} {right_type}"
                )

            self.quadruples.add(operator, left_operand, right_operand, -1)

            self.operand_types.append(result_type)

        return p

    @_("")
    def in_assign(self, p):
        self.operands.append(p[-2])
        # TODO: look up symbol in table
        self.operand_types.append("int")
        self.operators.append(Op.ASSIGN)

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

    ################################################par
    # Expression -> Exp -> Term -> Factor -> Const #
    ################################################
    @_("exp", "exp LESSER exp", "exp GREATER exp")
    def expression(self, p):
        return p

    @_("term exp_operator")
    def exp(self, p):
        if not self.operators.is_empty() and self.operators.peek() in [
            Op.ADD,
            Op.SUBTRACT,
        ]:
            operator = self.operators.pop()

            right_operand = self.operands.pop()
            right_type = self.operand_types.pop()

            left_operand = self.operands.pop()
            left_type = self.operand_types.pop()

            # validate semantics here
            result_type = validate_semantics(left_type, right_type, operator)
            if result_type == "error":
                raise Exception(
                    f"type mismatch: {left_operand} {operator} {right_type}"
                )

            result = f"t-{self.quadruples.get_index()+1}"

            self.quadruples.add(operator, left_operand, right_operand, result)

            self.operands.append(result)
            self.operand_types.append(result_type)

        return p

    @_("PLUS seen_operator exp", "MINUS seen_operator exp", "empty")
    def exp_operator(self, p):
        return p

    @_("factor term_operator")
    def term(self, p):
        if not self.operators.is_empty() and self.operators.peek() in [
            Op.MULTIPLY,
            Op.DIVIDE,
        ]:
            operator = self.operators.pop()

            right_operand = self.operands.pop()
            right_type = self.operand_types.pop()

            left_operand = self.operands.pop()
            left_type = self.operand_types.pop()

            # validate semantics here
            result_type = validate_semantics(left_type, right_type, operator)
            if result_type == "error":
                raise Exception(
                    f"type mismatch: {left_operand} {operator} {right_type}"
                )

            result = f"t-{self.quadruples.get_index()+1}"

            self.quadruples.add(operator, left_operand, right_operand, result)

            self.operands.append(result)
            self.operand_types.append(result_type)
        return p

    @_("MULTIPLY seen_operator term", "DIVIDE seen_operator term", "empty")
    def term_operator(self, p):
        return p

    @_("LPAREN expression RPAREN", "const")
    def factor(self, p):
        return p

    @_("")
    def seen_operator(self, p):
        operator = p[-1]

        match operator:
            case "+":
                self.operators.append(Op.ADD)
            case "-":
                self.operators.append(Op.SUBTRACT)
            case "*":
                self.operators.append(Op.MULTIPLY)
            case "/":
                self.operators.append(Op.DIVIDE)
            case _:
                print(f"invalid operator {operator}")

    @_(
        "PLUS seen_operator ID",
        "MINUS seen_operator ID",
        "PLUS seen_operator const_num",
        "MINUS seen_operator const_num",
        "const_num",
        "const_string",
        "const_id",
    )
    def const(self, p):
        return p

    @_("const_int", "const_float")
    def const_num(self, p):
        return p

    @_("NUMBER")
    def const_int(self, p):
        addr = self.memory_assigner.assign("c_int", p[0])
        self.operands.append(addr)
        self.operand_types.append("int")
        return p

    @_("FLOAT_NUMBER")
    def const_float(self, p):
        addr = self.memory_assigner.assign("c_float", p[0])
        self.operands.append(addr)
        self.operand_types.append("float")
        return p

    @_("STRING")
    def const_string(self, p):
        addr = self.memory_assigner.assign("c_string", p[0])
        self.operands.append(addr)
        self.operand_types.append("string")
        return p

    @_("ID")
    def const_id(self, p):
        # look up id in symbol table
        # if not available, id does not exist, throw error
        # symbol table will contain address and type
        # push to stacks

        print("not implemented")
        return p

    #########
    # Empty #
    #########
    @_("")
    def empty(self, p):
        pass
