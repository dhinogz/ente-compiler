from enum import IntEnum

class Operator(IntEnum):
    SUBTRACT = 1        # 1
    ADD = 2             # 2
    MULTIPLY = 3        # 3
    DIVIDE = 4          # 4
    LESS_THAN = 5       # 5
    GREATER_THAN = 6    # 6
    LESS_EQUAL = 7      # 7
    GREATER_EQUAL = 8   # 8
    EQUAL = 9           # 9
    NOT_EQUAL = 10      # 10
    ASSIGN = 11         # 11
    PRINT = 12          # 12
    GOTO = 13           # 13
    GOTOF = 14          # 14
    GOTOT = 15          # 15
    GOSUB = 16          # 16
    ERA = 17            # 17
    ENDFUNC = 18        # 18
    PARAM = 19          # 19


def perform_operation(operator: Operator, left_operand: int, right_operand: int) -> int | float | bool:
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
            return (left_operand < right_operand)
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

