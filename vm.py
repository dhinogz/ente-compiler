from memory import MemoryManager
from quadruples import Quadruple
from operators import Operator, perform_operation
from stack import Stack


class VirtualMachine:
    def __init__(self, memory_manager: MemoryManager) -> None:
        self.memory_manager = memory_manager
        self.function_exit = Stack("function_exit")

    def execute(self, quadruples: list[Quadruple]):
        ip = 0

        while ip < len(quadruples):
            curr = quadruples[ip]

            left_operand = (
                self.memory_manager.access(curr.left_operand)
                if curr.left_operand != -1
                else None
            )
            right_operand = (
                self.memory_manager.access(curr.right_operand)
                if curr.right_operand != -1
                else None
            )

            result = curr.result

            # Handling operations
            match curr.operator:
                case Operator.PRINT:
                    print(left_operand)
                case Operator.GOTO:
                    ip = curr.result
                    continue
                case Operator.GOTOF:
                    if not left_operand:
                        ip = curr.result
                        continue
                case Operator.GOTOT:
                    if left_operand:
                        ip = curr.result
                        continue
                case Operator.GOSUB:
                    self.function_exit.append(ip + 1)
                    ip = curr.result
                    continue
                case Operator.ERA:
                    self.memory_manager.allocate_local()
                    print(f"Function memory allocated for {curr.result}")
                case Operator.ENDFUNC:
                    self.memory_manager.deallocate_local()
                    next_func = self.function_exit.pop()
                    if next_func is not None:
                        ip = next_func
                    else:
                        print(f"error in function_exit stack")
                    continue
                case Operator.PARAM:
                    self.memory_manager.param(curr.left_operand)
                    print(f"Parameter {left_operand} added to function memory")
                case Operator.ASSIGN:
                    result = self.memory_manager.access(curr.left_operand)
                case _:
                    try:
                        if left_operand is None or right_operand is None:
                            raise ValueError(
                                f"Invalid operands: {left_operand} {right_operand}"
                            )
                        result = perform_operation(
                            curr.operator, left_operand, right_operand
                        )
                    except ValueError as e:
                        raise ValueError(
                            f"Unsupported operator: {curr.operator}"
                        ) from e

            if result != -1:
                self.memory_manager.assign(curr.result, result)

            ip += 1
