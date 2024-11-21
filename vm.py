from quadruples import Quadruple
from operators import Operator, perform_operation

class MemoryManager:
    def __init__(self) -> None:
        self.memory = {} 

    def access(self, pointer) -> int | None:
        if pointer == -1:
            return None
        if pointer not in self.memory:
            return None
        return self.memory[pointer]

    def access_operands(self, pointer_left, pointer_right) -> tuple[int | None, int | None]:
        return (self.access(pointer_left), self.access(pointer_right))

class VirtualMachine:
    def __init__(self, memory_manager: MemoryManager) -> None:
        self.memory_manager = memory_manager

    def execute(self, quadruples: list[Quadruple]):
        ip = 0

        while ip < len(quadruples):
            curr = quadruples[ip]
            print(curr)

            left_operand = curr.left_operand
            right_operand = curr.right_operand
            # left_operand = self.memory_manager.access(curr.left_operand)
            # right_operand = self.memory_manager.access(curr.right_operand)

            result = None

            match curr.operator:
                # Non-calculation operations
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
                    # TODO: keep track where we left off and go to function call

                    # function_exit_stack.push(ip + 1)
                    # ip = quadruple.result

                    print("not yet implemented")
                    pass 
                case Operator.ERA:
                    # TODO: Allocate memory for function call 

                    # mm.allocate_local()
                    # memory_descriptor = mm.descriptor["local"][quadruple.result]
                    # for type, value in memory_descriptor.items():
                    #     mm.allocate(type, value)

                    print("not yet implemented")
                    pass
                case Operator.ENDFUNC:
                    # TODO: deallocate memory, exit from function call and go back to where we left off

                    # mm.deallocate_local()
                    # ip = function_exit_stack.pop()
                    # continue
                    
                    print("not yet implemented")
                    pass
                case Operator.PARAM:
                    # TODO: add param to memory

                    # mm.param(curr.left_operand)
                    print("not yet implemented")
                    pass
                case _:
                    try:
                        if left_operand is None or right_operand is None:
                            raise ValueError(f"Invalid operands: {left_operand} {right_operand}")
                        result = perform_operation(curr.operator, left_operand, right_operand)
                    except ValueError as e:
                        raise ValueError(f"Unsupported operator: {curr.operator}") from e


            if result is not None:
                quadruples[ip+1].left_operand = result
                # mm.assign(curr.result, result)

            ip += 1
