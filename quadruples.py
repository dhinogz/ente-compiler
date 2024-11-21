class Quadruple:
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

    def __str__(self) -> str:
        return f"{self.operator} {self.left_operand} {self.right_operand} {self.result}"

    def __repr__(self) -> str:
        return str(self)


class QuadrupleManager:
    def __init__(self) -> None:
        self.quadruples: list[Quadruple] = []
        self.temp_count = 0

    def add(self, operator, left_operand, right_operand, result):
        q = Quadruple(operator, left_operand, right_operand, result)
        self.quadruples.append(q)

    def get_index(self) -> int:
        return len(self.quadruples) - 1

    def fill(self, index, value):
        self.quadruples[index].result = value

    def __str__(self) -> str:
        res = []
        for q in self.quadruples:
            res.append(str(q))
        return "\n".join(res)

