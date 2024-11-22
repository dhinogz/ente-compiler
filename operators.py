from enum import IntEnum


class Operator(IntEnum):
    GOTO = 1
    ASSIGN = 2
    PRINT = 3
    GOTOF = 4
    GOTOT = 5
    GOSUB = 6
    ERA = 8
    ENDFUNC = 9
    PARAM = 10
    SUBTRACT = 12
    ADD = 13
    MULTIPLY = 14
    DIVIDE = 15
    LESS_THAN = 16
    GREATER_THAN = 17
    LESS_EQUAL = 18
    GREATER_EQUAL = 19
    EQUAL = 20
    NOT_EQUAL = 21


def perform_operation(
    operator: Operator, left_operand: int, right_operand: int
) -> int | float | bool:
    match operator:
        case Operator.SUBTRACT:
            return left_operand - right_operand
        case Operator.ADD:
            return left_operand + right_operand
        case Operator.MULTIPLY:
            return left_operand * right_operand
        case Operator.DIVIDE:
            return left_operand / right_operand
        case Operator.LESS_THAN:
            return left_operand < right_operand
        case Operator.GREATER_THAN:
            return left_operand > right_operand
        case Operator.LESS_EQUAL:
            return left_operand <= right_operand
        case Operator.GREATER_EQUAL:
            return left_operand >= right_operand
        case Operator.EQUAL:
            return left_operand == right_operand
        case Operator.NOT_EQUAL:
            return left_operand != right_operand
        case _:
            raise ValueError(f"Unsupported operator: {operator}")
