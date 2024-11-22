OFFSETS = {
    "g_void": 500,
    "g_int": 1000,
    "g_float": 2000,
    "t_int": 3000,
    "t_float": 4000,
    "t_bool": 5000,
    "c_int": 6000,
    "c_float": 7000,
    "c_string": 8000,
    "l_int": 9000,
    "l_float": 10000,
}


class MemoryAssigner:
    def __init__(self):
        self.constants = {}
        self.counter = {
            "global": {
                "g_void": OFFSETS["g_void"],
                "g_int": OFFSETS["g_int"],
                "g_float": OFFSETS["g_float"],
                "t_int": OFFSETS["t_int"],
                "t_float": OFFSETS["t_float"],
                "t_bool": OFFSETS["t_bool"],
                "c_int": OFFSETS["c_int"],
                "c_float": OFFSETS["c_float"],
                "c_string": OFFSETS["c_string"],
            },
            "local": {},
        }

    def assign(self, memory_type, value=None):
        if value is not None:
            if value not in self.constants.keys():
                self.constants[value] = self.counter["global"][memory_type]
            else:
                return self.constants[value]

        assigned_address = self.counter["global"][memory_type]
        self.counter["global"][memory_type] += 1

        return assigned_address

    def assign_local(self, function, type):
        if function not in self.counter["local"]:
            self.counter["local"][function] = {
                "l_int": OFFSETS["l_int"],
                "l_float": OFFSETS["l_float"],
            }

        assigned_address = self.counter["local"][function][type]
        self.counter["local"][function][type] += 1

        return assigned_address

    def output(self):
        counter_copy = self.counter

        for key, _ in counter_copy["global"].items():
            counter_copy["global"][key] -= OFFSETS[key]

        for key, value in counter_copy["local"].items():
            for key2, _ in value.items():
                counter_copy["local"][key][key2] -= OFFSETS[key2]

        return self.constants, counter_copy

    def display(self):
        constants, counter = self.output()

        print("Constant Table:")
        for value, address in constants.items():
            print(f"{address}: {value}")

        print("\nGlobal Counter Table:")
        for key, value in counter["global"].items():
            print(f"{key}: {value}")

        print("\nLocal Counter Table:")
        for key, value in counter["local"].items():
            print(f"{key}:")
            for key2, value2 in value.items():
                print(f"  {key2}: {value2}")


class Memory:
    def __init__(self) -> None:
        # Initialize an empty memory dictionary to store values at pointers
        self.memory = {}

    def allocate(self, pointer: int, value: int | float | bool) -> None:
        # Allocate memory for a pointer with a value
        self.memory[pointer] = value

    def deallocate(self, pointer: int) -> None:
        # Deallocate memory for a pointer (remove from memory)
        if pointer in self.memory:
            del self.memory[pointer]

    def access(self, pointer: int) -> int | None:
        # Access a memory location by pointer, returns None if not found
        return self.memory.get(pointer, None)

    def __repr__(self):
        return f"Memory({self.memory})"


class MemoryManager:
    def __init__(self) -> None:
        # Initialize the memory and local memory stack
        self.memory = Memory()
        self.local_memory_stack = []

    def access(self, pointer: int) -> int | None:
        return self.memory.access(pointer)

    def access_operands(
        self, pointer_left: int, pointer_right: int
    ) -> tuple[int | None, int | None]:
        # Access two operands from memory
        return self.access(pointer_left), self.access(pointer_right)

    def allocate_local(self, function_name: str) -> None:
        self.local_memory_stack.append({})  # Start a new scope for local variables

    def deallocate_local(self) -> None:
        if self.local_memory_stack:
            self.local_memory_stack.pop()  # Remove the most recent local scope

    def param(self, param_value: int | float | bool) -> None:
        # Add a parameter to the local memory scope
        if self.local_memory_stack:
            current_scope = self.local_memory_stack[-1]
            param_pointer = len(current_scope)
            current_scope[param_pointer] = param_value
        else:
            raise ValueError("No local memory scope to add a parameter")

    def __repr__(self):
        return f"MemoryManager({self.memory}, local_memory_stack={self.local_memory_stack})"
