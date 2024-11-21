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

