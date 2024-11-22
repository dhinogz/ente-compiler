from stack import Stack


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
    "g_string": 11000,
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
                "g_string": OFFSETS["g_string"],
            },
            "local": {},
        }

    def assign(self, mem_type, value=None):
        if value is not None:
            if value not in self.constants.keys():
                self.constants[value] = self.counter["global"][mem_type]
            else:
                return self.constants[value]

        assigned_address = self.counter["global"][mem_type]
        self.counter["global"][mem_type] += 1

        return assigned_address

    def assign_local(self, scope_name, data_type):
        if scope_name not in self.counter["local"]:
            self.counter["local"][scope_name] = {
                "l_int": OFFSETS["l_int"],
                "l_float": OFFSETS["l_float"],
            }

        assigned_address = self.counter["local"][scope_name][data_type]
        self.counter["local"][scope_name][data_type] += 1

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


class MemorySegment:
    def __init__(self, mem_type, size=0):
        if mem_type not in OFFSETS.keys():
            raise ValueError(f"Invalid memory segment type: {mem_type}")

        self.memory = [None] * size
        self.mem_type = mem_type

    def access(self, address):
        index = address - OFFSETS[self.mem_type]
        return self.memory[index] if index < len(self.memory) else None

    def assign(self, address, value):
        index = address - OFFSETS[self.mem_type]
        self.memory[index] = value

    def __str__(self):
        return f"{self.memory}"

    def __repr__(self):
        return str(self)


class MemoryManager:
    def __init__(self):
        self.descriptor = {
            "global": {
                "g_void": 0,
                "g_int": 0,
                "g_float": 0,
                "t_int": 0,
                "t_float": 0,
                "t_bool": 0,
                "c_int": 0,
                "c_float": 0,
                "c_string": 0,
                "g_string": 0,
            },
            "local": {},
        }
        self.memory = Stack("memory")

    def allocate(self, mem_type, size=0):
        if not mem_type.startswith("l"):
            if len(self.memory) == 0:
                self.memory.append({})
            self.memory.items()[0][mem_type] = MemorySegment(mem_type, size)
        else:
            self.memory.items()[-1][mem_type] = MemorySegment(mem_type, size)

    def allocate_local(self):
        self.memory.append({})

    def deallocate_local(self):
        self.memory.pop()

    def describe(self, mem_type, size=0, function=None):
        if function is not None:
            if function not in self.descriptor["local"]:
                self.descriptor["local"][function] = {}
            self.descriptor["local"][function][mem_type] = size
        else:
            self.descriptor["global"][mem_type] = size

    def access(self, address):
        mem_type = self._get_type(address)

        if mem_type.startswith("l"):
            value = (
                self.memory.peek()[mem_type].access(address)
                if self.memory.peek()[mem_type].access(address) is not None
                else self.memory.peek(2)[mem_type].access(address)
            )
        else:
            value = self.memory.first()[mem_type].access(address)

        if mem_type.endswith("void"):
            return None
        if mem_type.endswith("int"):
            return int(value)
        if mem_type.endswith("float"):
            return float(value)
        if mem_type.endswith("bool"):
            return bool(value)
        if mem_type.endswith("string"):
            return str(value)

        return value

    def assign(self, address, value):
        mem_type = self._get_type(address)

        if mem_type.startswith("l"):
            memory_to_access = self.memory.items()[-1]
        else:
            memory_to_access = self.memory.items()[0]

        if mem_type.endswith("int"):
            value = int(value)
        if mem_type.endswith("float"):
            value = float(value)
        if mem_type.endswith("bool"):
            value = bool(value)
        if mem_type.endswith("string"):
            value = str(value)

        memory_to_access[mem_type].assign(address, value)

    def param(self, address):
        mem_type = self._get_type(address)

        if mem_type.startswith("l"):
            access_memory = self.memory.items()[-2]
        else:
            access_memory = self.memory.items()[0]

        value = access_memory[mem_type].access(address)

        index = 0
        target_memory = self.memory.peek()

        if mem_type.endswith("int"):
            target_type = "l_int"
        if mem_type.endswith("float"):
            target_type = "l_float"

        while (
            target_memory[target_type].access(OFFSETS[target_type] + index) is not None
        ):
            index += 1

        target_memory[target_type].assign(OFFSETS[target_type] + index, value)

    def _get_type(self, address):
        if address < OFFSETS["g_int"]:
            return "g_void"
        elif address < OFFSETS["g_float"]:
            return "g_int"
        elif address < OFFSETS["t_int"]:
            return "g_float"
        elif address < OFFSETS["t_float"]:
            return "t_int"
        elif address < OFFSETS["t_bool"]:
            return "t_float"
        elif address < OFFSETS["c_int"]:
            return "t_bool"
        elif address < OFFSETS["c_float"]:
            return "c_int"
        elif address < OFFSETS["c_string"]:
            return "c_float"
        elif address < OFFSETS["l_int"]:
            return "c_string"
        elif address < OFFSETS["l_float"]:
            return "l_int"
        elif address < OFFSETS["g_string"]:
            return "l_float"
        else:
            return "g_string"

    def __str__(self):
        return str(self.memory)
