from operators import Operator

class Quadruple:
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

    def __str__(self) -> str:
        return f"{self.operator} {self.left_operand} {self.right_operand} {self.result}"

    def __repr__(self) -> str:
        return self.__str__()


class QuadrupleManager:
    def __init__(self) -> None:
        self.operand_stack: list[str] = []
        self.operand_type_stack: list[str] = []
        self.operator_stack: list[Operator] = []
        self.temp_count = 0
        self.quadruples: list[Quadruple] = []

    def add(self, operator, left_operand, right_operand, result):
        q = Quadruple(operator, left_operand, right_operand, result)
        self.quadruples.append(q)

    def get_index(self) -> int:
        return len(self.quadruples) - 1

    def fill(self, index, value):
        self.quadruples[index].result = value

    def generate_quadruple(self):
        # Pop operator and operands
        operator = self.operator_stack.pop()
        right_operand = self.operand_stack.pop()
        left_operand = self.operand_stack.pop()

        # Perform type checking/coercion
        right_type = self.operand_type_stack.pop()
        left_type = self.operand_type_stack.pop()
        result_type = self.coerce_types(right_type, left_type)

        # Create a new temporary variable for the result
        temp_result = f"t{self.temp_count}"
        self.temp_count += 1

        # Add the quadruple to the list
        self.add(operator, left_operand, right_operand, temp_result)

        # Push the result back to the stacks
        self.operand_stack.append(temp_result)
        self.operand_type_stack.append(result_type)

    def coerce_types(self, type1, type2):
        # Simplified type coercion
        if type1 == type2:
            return type1
        elif "float" in (type1, type2):
            return "float"
        else:
            return "int"

    def __str__(self) -> str:
        res = []
        for q in self.quadruples:
            res.append(str(q))
        return "\n".join(res)

