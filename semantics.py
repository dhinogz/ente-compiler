from operators import Operator


SEMANTIC_CUBE = {
    "int": {
        "int": {
            "<": "bool",
            ">": "bool",
            "<=": "bool",
            ">=": "bool",
            "==": "bool",
            "!=": "bool",
            "=": "int",
            "*": "int",
            "/": "float",
            "+": "int",
            "-": "int",
        },
        "float": {
            "<": "bool",
            ">": "bool",
            "<=": "bool",
            ">=": "bool",
            "==": "bool",
            "!=": "bool",
            "=": "error",
            "*": "float",
            "/": "float",
            "+": "float",
            "-": "float",
        },
        "bool": {
            "<": "bool",
            ">": "bool",
            "<=": "bool",
            ">=": "bool",
            "==": "bool",
            "!=": "bool",
            "=": "error",
            "*": "int",
            "/": "int",
            "+": "int",
            "-": "int",
        },
    },
    "float": {
        "int": {
            "<": "bool",
            ">": "bool",
            "<=": "bool",
            ">=": "bool",
            "==": "bool",
            "!=": "bool",
            "=": "error",
            "*": "float",
            "/": "float",
            "+": "float",
            "-": "float",
        },
        "float": {
            "<": "bool",
            ">": "bool",
            "<=": "bool",
            ">=": "bool",
            "==": "bool",
            "!=": "bool",
            "=": "float",
            "*": "float",
            "/": "float",
            "+": "float",
            "-": "float",
        },
        "bool": {
            "<": "bool",
            ">": "bool",
            "<=": "bool",
            ">=": "bool",
            "==": "bool",
            "!=": "bool",
            "=": "error",
            "*": "float",
            "/": "float",
            "+": "float",
            "-": "float",
        },
    },
    "bool": {
        "int": {
            "<": "bool",
            ">": "bool",
            "<=": "bool",
            ">=": "bool",
            "==": "bool",
            "!=": "bool",
            "=": "error",
            "*": "int",
            "/": "int",
            "+": "int",
            "-": "int",
        },
        "float": {
            "<": "bool",
            ">": "bool",
            "<=": "bool",
            ">=": "bool",
            "==": "bool",
            "!=": "bool",
            "=": "error",
            "*": "float",
            "/": "float",
            "+": "float",
            "-": "float",
        },
        "bool": {
            "<": "bool",
            ">": "bool",
            "<=": "bool",
            ">=": "bool",
            "==": "bool",
            "!=": "bool",
            "=": "error",
            "*": "int",
            "/": "int",
            "+": "int",
            "-": "int",
        },
    },
}
OPERATOR_MAPPING = {
    Operator.SUBTRACT: "-",
    Operator.ADD: "+",
    Operator.MULTIPLY: "*",
    Operator.DIVIDE: "/",
    Operator.LESS_THAN: "<",
    Operator.GREATER_THAN: ">",
    Operator.LESS_EQUAL: "<=",
    Operator.GREATER_EQUAL: ">=",
    Operator.EQUAL: "==",
    Operator.NOT_EQUAL: "!=",
    Operator.ASSIGN: "=",
}


def validate_semantics(left_operand_type, right_operand_type, operator) -> str:
    operator_symbol = OPERATOR_MAPPING.get(operator)
    if not operator_symbol:
        return "error"

    try:
        result_type = SEMANTIC_CUBE[left_operand_type][right_operand_type][
            operator_symbol
        ]
        print(
            f"{left_operand_type} {operator_symbol} {right_operand_type} -> {result_type}"
        )
        return result_type
    except KeyError:
        print(
            f"Error: Invalid operation {left_operand_type} {operator_symbol} {right_operand_type}"
        )
        return "error"
