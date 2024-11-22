class Symbol:
    """
    This class represents a symbol in the symbol table.

    Attributes:
    - name (str): The name of the symbol.
    - type (str): The type of the symbol [var.int, var.float, param.int, param.float, table.global, table.local].
    - address (int): The address of the symbol in memory.
    - child (SymbolTable): The child symbol table (when symbol is a table).
    - index (int): The index of the start quadruple (when symbol is a function table).
    """

    def __init__(self, name, type, address=None, child=None, index=None):
        self.name = name
        self.type = type
        self.address = address
        self.child = child
        self.index = index

    def update_index(self, index):
        """
        Update the index of the symbol.

        Parameters:
        - index (int): The new index of the symbol.
        """
        self.index = index

    def __str__(self):
        return f"[{self.address}] {self.name}: {self.type}"

    def __repr__(self):
        return str(self)


class SymbolTable:
    """
    This class represents a symbol table.

    Attributes:
    - symbols (dict): The dictionary of symbols.
    """

    def __init__(self):
        self.symbols = {}

    def declare(self, symbol):
        """
        Declare a new symbol in the table.

        Parameters:
        - symbol (Symbol): The symbol to be declared.

        Raises:
        - AlreadyDeclaredError: If the symbol is already declared.
        """
        if symbol.name in self.symbols:
            raise Exception(f"Symbol {symbol.name} is already declared.")
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        """
        Look up a symbol in the table.

        Parameters:
        - name (str): The name of the symbol to look up.

        Returns:
        - Symbol: The symbol with the given name.

        Raises:
        - UndeclaredError: If the symbol is undeclared.
        """
        if name not in self.symbols:
            raise Exception(f"Symbol {name} is undeclared.")
        return self.symbols[name]

    def update(self, symbol):
        """
        Update a symbol in the table.

        Parameters:

        Raises:
        - UndeclaredError: If the symbol is undeclared.
        """
        if symbol.name not in self.symbols:
            raise Exception(f"Symbol {symbol.name} is undeclared.")
        self.symbols[symbol.name] = symbol

    def remove(self, name):
        """
        Remove a symbol from the table.

        Parameters:
        - name (str): The name of the symbol to be removed.

        Raises:
        - UndeclaredError: If the symbol is undeclared.
        """
        if name not in self.symbols:
            raise Exception(f"Symbol {name} is undeclared.")
        del self.symbols[name]

    def __str__(self):
        return "\n" + "\n".join(str(symbol) for symbol in self.symbols.values())
