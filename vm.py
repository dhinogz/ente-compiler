from quadruples import Quadruple
from operators import Operator, perform_operation
from memory import MemoryManager


class VirtualMachine:
    def __init__(self) -> None:
        self.memory_manager = MemoryManager()

    def execute(self, quadruples: list[Quadruple]):
        ip = 0

        while ip < len(quadruples):
            curr = quadruples[ip]
            print(f"Executing: {curr}")

            left_operand = curr.left_operand
            right_operand = curr.right_operand
            result = curr.result

            # Handling operations
            match curr.operator:
                case Operator.PRINT:
                    value_to_print = self.memory_manager.access(left_operand)
                    print(f"PRINT: {value_to_print}")
                case Operator.GOTO:
                    ip = curr.result
                    continue
                case Operator.GOTOF:
                    if not self.memory_manager.access(left_operand):
                        ip = curr.result
                        continue
                case Operator.GOTOT:
                    if self.memory_manager.access(left_operand):
                        ip = curr.result
                        continue
                case Operator.GOSUB:
                    print("Function call not implemented")
                case Operator.ERA:
                    self.memory_manager.allocate_local()
                    print(f"Function memory allocated for {curr.result}")
                case Operator.ENDFUNC:
                    self.memory_manager.deallocate_local()
                    print(f"Function memory deallocated for {curr.result}")
                case Operator.PARAM:
                    self.memory_manager.param(left_operand)
                    print(f"Parameter {left_operand} added to function memory")
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

            if result is not None:
                # TODO: Store the result in memory and update the result pointer in the quadruple
                self.memory_manager.memory.allocate(curr.result, result)
                print(f"Result stored at {curr.result}: {result}")

            ip += 1
