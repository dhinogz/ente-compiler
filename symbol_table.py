class Symbol:
    def __init__(
        self,
        name="undeclared",
        data_type="undeclared",
        address=None,
        child=None,
        index=None,
    ):
        self.name = name
        self.data_type = data_type
        self.address = address
        self.child = child
        self.index = index

    def __str__(self):
        return f"[{self.address}] {self.name}: {self.data_type}"

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return self.name != "undeclared"


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, symbol):
        if symbol.name in self.symbols:
            raise Exception(f"Symbol {symbol.name} is already declared.")
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        if name not in self.symbols:
            raise Exception(f"Symbol {name} is undeclared.")
        return self.symbols[name]

    def update(self, symbol):
        if symbol.name not in self.symbols:
            raise Exception(f"Symbol {symbol.name} is undeclared.")
        self.symbols[symbol.name] = symbol

    def remove(self, name):
        if name not in self.symbols:
            raise Exception(f"Symbol {name} is undeclared.")
        del self.symbols[name]

    def __str__(self):
        return "\n" + "\n".join(str(symbol) for symbol in self.symbols.values())
