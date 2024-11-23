import logging
from sly import Parser
from lexer import EnteLexer
from memory import MemoryAssigner
from operators import Operator as Op

from symbol_table import SymbolTable, Symbol
from quadruples import QuadrupleManager
from semantics import validate_semantics
from stack import Stack


class EnteParser(Parser):
    tokens = EnteLexer.tokens

    precedence = (
        ("left", PLUS, MINUS),  # type: ignore
        ("left", MULTIPLY, DIVIDE),  # type: ignore
    )

    debugfile = "parser.out"
    log = logging.getLogger()
    log.setLevel(logging.ERROR)

    def __init__(self):
        super().__init__()

        self.scope_table = SymbolTable()
        self.memory_assigner = MemoryAssigner()

        # Stacks for symbol table building
        self.scope = Stack("scope")
        self.variables = Stack("variables")

        self.quadruples = QuadrupleManager()

        # Stacks for quadruple building
        self.operands = Stack("operands")
        self.operand_types = Stack("operand_types")
        self.operators = Stack("operators")
        self.jumps = Stack("jumps")

    ########
    # Root #
    ########
    @_("PROGRAM prog_init SEMICOLON global_scope main END SEMICOLON")  # type: ignore
    def root(self, p):
        return (f"root {p[1]}", p[3], p[4])

    ########################
    # Initialize a program #
    ########################
    @_("ID")  # type: ignore
    def prog_init(self, p):
        # we initialize our GOTO line in our quadruples
        # we'll later fill in where it has to jump to start main
        self.quadruples.add(Op.GOTO, -1, -1, -1)

        # global scope symbol table contains a child symbol table for storing it's functions and variables
        self.scope_table.declare(
            Symbol(data_type="table.global", name=p[0], child=SymbolTable())
        )
        self.scope.append(p[0])
        self.jumps.append(self.quadruples.current_index())

        return p[0]

    ##########
    # Global #
    ##########
    @_("vars funcs")  # type: ignore
    def global_scope(self, p):
        return p

    #############
    # Variables #
    #############
    @_(  # type: ignore
        "VAR in_vars vars_declare",
        "empty",
    )
    def vars(self, p):
        return p

    @_("")  # type: ignore
    def in_vars(self, _):
        curr_scope = self.scope.peek() if not self.scope.is_empty() else "global"
        curr_scope_table = self.scope_table.lookup(curr_scope)
        if not curr_scope_table.child:
            # init symbol table for scope
            curr_scope_table.child = SymbolTable()
            self.scope_table.update(curr_scope_table)

    @_(  # type: ignore
        "var_list COLON var_type SEMICOLON",
        "var_list COLON var_type SEMICOLON vars",
    )
    def vars_declare(self, p):
        return p

    @_("ID", "ID COMMA var_list")  # type: ignore
    def var_list(self, p):
        self.variables.append(p[0])

        return p

    @_("INT", "FLOAT", "STRING")  # type: ignore
    def var_type(self, p):
        curr_scope = self.scope.peek()
        curr_scope_table = self.scope_table.lookup(curr_scope)

        for var in self.variables:
            if len(self.scope) > 1:
                # if not global scope
                mem_addr = self.memory_assigner.assign_local(
                    curr_scope_table.address, f"l_{p[0]}"
                )
            else:
                mem_addr = self.memory_assigner.assign(f"g_{p[0]}")

            var_symbol = Symbol(name=var, data_type=f"var.{p[0]}", address=mem_addr)
            curr_scope_table.child.declare(var_symbol)
            self.scope_table.update(curr_scope_table)

        self.variables.clear()

        return p

    #############
    # Functions #
    #############
    @_(  # type: ignore
        "VOID ID seen_func_id LPAREN params RPAREN LBRACE block RBRACE seen_func SEMICOLON",
        "empty",
    )
    def funcs(self, p):
        return p

    @_("")  # type: ignore
    def seen_func(self, _):
        self.quadruples.add(Op.ENDFUNC, -1, -1, -1)
        self.scope.pop()

    @_("")  # type: ignore
    def seen_func_id(self, p):
        mem_addr = self.memory_assigner.assign("g_void")
        self.scope_table.declare(
            Symbol(
                data_type="table.local",
                name=p[-1],
                child=SymbolTable(),
                address=mem_addr,
            )
        )
        self.scope.append(p[-1])

    @_("ID COLON param_type", "ID COLON param_type COMMA params")  # type: ignore
    def params(self, p):
        curr_scope = self.scope.peek()
        mem_addr = self.memory_assigner.assign_local(curr_scope, f"l_{p[2]}")

        param_symbol = Symbol(name=p[0], data_type=f"param.{p[2]}", address=mem_addr)

        curr_scope_table = self.scope_table.lookup(curr_scope)
        curr_scope_table.child.declare(param_symbol)

        self.scope_table.update(curr_scope_table)

        return p

    @_("INT", "FLOAT", "STRING")  # type: ignore
    def param_type(self, p):
        return p[0]

    ########
    # Main #
    ########
    @_("MAIN LBRACE at_main block RBRACE SEMICOLON", "empty")  # type: ignore
    def main(self, p):
        return p

    @_("")  # type: ignore
    def at_main(self, _):
        main_quadruple_idx = self.jumps.pop()
        self.quadruples.fill(main_quadruple_idx, self.quadruples.current_index() + 1)

    #########
    # Block #
    #########
    @_("vars statements")  # type: ignore
    def block(self, p):
        return p

    ##############
    # Statements #
    ##############
    @_("statement SEMICOLON statements", "empty")  # type: ignore
    def statements(self, p):
        return p

    @_(  # type: ignore
        "assign",
        "write",
        "condition",
        "loop",
        "do_while",
        "LBRACE block RBRACE",
    )
    def statement(self, p):
        return p[0]

    @_("ID ASSIGN in_assign expression")  # type: ignore
    def assign(self, p):
        if not self.operators.is_empty() and self.operators.peek() == Op.ASSIGN:
            operator = self.operators.pop()

            operand = self.operands.pop()
            operand_type = self.operand_types.pop()

            assignee = self.operands.pop()
            assignee_type = self.operand_types.pop()

            result_type = validate_semantics(assignee_type, operand_type, operator)
            if result_type == "error":
                raise Exception(f"type mismatch: {assignee} {operator} {operand_type}")

            self.quadruples.add(operator, operand, -1, assignee)

            self.operands.append(assignee)
            self.operand_types.append(result_type)

        return p

    @_("")  # type: ignore
    def in_assign(self, p):
        id_symbol = Symbol()
        for scope in reversed(self.scope):
            scope_symbols = self.scope_table.lookup(scope).child
            if scope_symbols.lookup(p[-2]):
                id_symbol = scope_symbols.lookup(p[-2])
                break

        if not id_symbol:
            raise Exception(f"Symbol {p[-2]} is undeclared")

        self.operators.append(Op.ASSIGN)
        self.operands.append(id_symbol.address)
        self.operand_types.append(id_symbol.data_type)

    @_("WHILE LPAREN in_loop expression seen_condition RPAREN LBRACE block RBRACE")  # type: ignore
    def loop(self, p):
        false = self.jumps.pop()
        start = self.jumps.pop()
        self.quadruples.add(Op.GOTO, -1, -1, start)
        self.quadruples.fill(false, self.quadruples.current_index() + 1)
        return p

    @_("")  # type: ignore
    def in_loop(self, _):
        self.jumps.append(self.quadruples.current_index() + 1)

    @_("")  # type: ignore
    def seen_condition(self, _):
        expression_type = self.operand_types.pop()

        if expression_type != "bool":
            raise Exception("Cycle expression must be of type bool")
        expression_result = self.operands.pop()
        self.quadruples.add(Op.GOTOF, expression_result, -1, -1)
        self.jumps.append(self.quadruples.current_index())

    @_("WRITE LPAREN expression RPAREN")  # type: ignore
    def write(self, p):
        self.quadruples.add(Op.PRINT, self.operands.pop(), -1, -1)
        self.operand_types.pop()
        return p

    @_("IF LPAREN expression RPAREN seen_condition LBRACE block RBRACE optional_else")  # type: ignore
    def condition(self, p):
        end = self.jumps.pop()
        self.quadruples.fill(end, self.quadruples.current_index())
        if self.jumps:
            final_jump = self.jumps.pop()
            self.quadruples.fill(final_jump, self.quadruples.current_index())
        return p

    @_("ELSE seen_else LBRACE block RBRACE", "empty")  # type: ignore
    def optional_else(self, p):
        return p

    @_("")  # type: ignore
    def seen_else(self, p):
        self.quadruples.add(Op.GOTO, -1, -1, -1)
        false = self.jumps.pop()
        self.jumps.append(self.quadruples.current_index())
        self.quadruples.fill(false, self.quadruples.current_index() + 1)
        return p

    @_("DO LBRACE block RBRACE WHILE LPAREN expression RPAREN")  # type: ignore
    def do_while(self, p):
        return p

    ################################################
    # Expression -> Exp -> Term -> Factor -> Const #
    ################################################
    @_("exp", "exp LESSER seen_operator exp", "exp GREATER seen_operator exp")  # type: ignore
    def expression(self, p):
        if not self.operators.is_empty() and self.operators.peek() in [
            Op.LESS_THAN,
            Op.GREATER_THAN,
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

            result_addr = self.memory_assigner.assign(f"t_{result_type}")

            self.quadruples.add(operator, left_operand, right_operand, result_addr)

            self.operands.append(result_addr)
            self.operand_types.append(result_type)
        return p

    @_("term exp_operator")  # type: ignore
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

            result_addr = self.memory_assigner.assign(f"t_{result_type}")

            self.quadruples.add(operator, left_operand, right_operand, result_addr)

            self.operands.append(result_addr)
            self.operand_types.append(result_type)
        return p

    @_("PLUS seen_operator exp", "MINUS seen_operator exp", "empty")  # type: ignore
    def exp_operator(self, p):
        return p

    @_("factor term_operator")  # type: ignore
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

            result_addr = self.memory_assigner.assign(f"t_{result_type}")

            self.quadruples.add(operator, left_operand, right_operand, result_addr)

            self.operands.append(result_addr)
            self.operand_types.append(result_type)
        return p

    @_("MULTIPLY seen_operator term", "DIVIDE seen_operator term", "empty")  # type: ignore
    def term_operator(self, p):
        return p

    @_("LPAREN expression RPAREN", "const")  # type: ignore
    def factor(self, p):
        return p

    @_("")  # type: ignore
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
            case ">":
                self.operators.append(Op.GREATER_THAN)
            case "<":
                self.operators.append(Op.LESS_THAN)
            case _:
                print(f"invalid operator {operator}")

    @_(  # type: ignore
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

    @_("const_int", "const_float")  # type: ignore
    def const_num(self, p):
        return p

    @_("NUMBER")  # type: ignore
    def const_int(self, p):
        addr = self.memory_assigner.assign("c_int", p[0])
        self.operands.append(addr)
        self.operand_types.append("int")
        return p

    @_("FLOAT_NUMBER")  # type: ignore
    def const_float(self, p):
        addr = self.memory_assigner.assign("c_float", p[0])
        self.operands.append(addr)
        self.operand_types.append("float")
        return p

    @_("STRING_CONSTANT")  # type: ignore
    def const_string(self, p):
        addr = self.memory_assigner.assign("c_string", p[0])
        self.operands.append(addr)
        self.operand_types.append("string")
        return p

    @_("ID")  # type: ignore
    def const_id(self, p):
        id_symbol = Symbol()
        for scope in reversed(self.scope):
            scope_symbols = self.scope_table.lookup(scope).child
            if scope_symbols.lookup(p[0]):
                id_symbol = scope_symbols.lookup(p[0])
                break

        if not id_symbol:
            raise Exception(f"Symbol {p[0]} is undeclared")

        self.operands.append(id_symbol.address)
        self.operand_types.append(id_symbol.data_type)

        return p

    #########
    # Empty #
    #########
    @_("")  # type: ignore
    def empty(self, _):
        pass
