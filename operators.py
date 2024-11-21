from enum import IntEnum

class Operator(IntEnum):
    SUBTRACT = 1
    ADD = 2             
    MULTIPLY = 3        
    DIVIDE = 4          
    LESS_THAN = 5       
    GREATER_THAN = 6    
    LESS_EQUAL = 7      
    GREATER_EQUAL = 8   
    EQUAL = 9           
    NOT_EQUAL = 10     
    PRINT = 11          
    GOTO = 12           
    GOTOF = 13          
    GOTOT = 14          
    GOSUB = 15          
    ERA = 16           
    ENDFUNC = 17        
    PARAM = 18         
    ASSIGN = 19         


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

