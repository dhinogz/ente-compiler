# Ente Compiler

The "Ente" Compiler (German for "pato") is a small, imperative, procedural programming language designed for educational purposes, primarily for educational use in compiler construction. The language follows a traditional procedural paradigm, which means that programs in Ente are structured around functions, variables, and control flow statements. It includes basic features common to many languages, such as arithmetic operations, conditional statements, and loops, while keeping the syntax simple enough.

The design of Ente emphasizes the importance of lexical, syntactic, and semantic analysis in the compilation process. In the first phase, the source code is analyzed lexically, where the language's tokens are identified using regular expressions. After that, we convert the token sequence into a structured representation that follows the language's grammar rules. This stage is crucial for ensuring that the source code follows the correct syntactic structure, setting the stage for further analysis and validation.

Following the parsing stage, Ente performs semantic validation to ensure the program's correctness. This includes type checking, scope resolution, and ensuring that operations are logically valid based on the types of operands involved. Once the semantic checks are complete, Ente generates an intermediate code representation (quadruple) that abstracts away from the original source code. This intermediate code is then executed by a custom virtual machine, which interprets the code, handles the program's memory and carries out operations.

This is the grammar that describes Ente's structure and rules.

![Grammar Diagram](https://github.com/dhinogz/ente-compiler/blob/main/ente-grammar.png)

## Modules 

### main.py
The entrypoint of our program. I used typer, a python library for creating CLIs. 

I have the following commands:

```python
cli = typer.Typer(no_args_is_help=True)

@cli.command("build")
def build(file: Annotated[Path, typer.Argument()]):
    """
    Reads code from file path and builds intermediate code.
    """
    pass

# reads intermediate code generated and runs virtual achine machine
@cli.command("vm")
def run_vm(file: Annotated[Path, typer.Argument()]):
    """reads intermediate code from file path and runs virtual machine."""
    pass

@cli.command("viz")
def generate_ast(
    file: Annotated[Path, typer.Argument()],
):
    """helper command to visualize AST our parser is creating."""
    pass

if __name__ == "__main__":
    cli()
```

### parser.py and lexer.py
I used the [SLY](https://sly.readthedocs.io/) library for my lexer and parser implementation of the "Patito" language. SLY is a Python implementation of the lex & yacc tools and it's parsing is based on the same LALR(1) algorithm.

Tokens are defined using regex and can be used in the parser quite simply.

```python
from sly import Lexer

class MyLexer(Lexer):
    tokens = {
        ID,
        PLUS,
    }

    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    PLUS = r"\+"
```

A grammer rule is defined in the Parser class as a decorator for a method. We can do `some code` once the specific grammer exits, like declaring variables or adding instructions in a quadruple.

It looks something like this.

```python
from sly import Parser


class EnteParser(Parser):
    tokens = MyLexer.tokens

    @_("ID seen_id grammer_rule")
    def grammer_definition(self, p):
        return p

    @_("")
    def seen_id(self, p):
        print(p[-1]) # p[-1] accesses last token in parent grammer (TOKEN)
        
    @_("ANOTHER_TOKEN PLUS grammer_rule", "empty") # we can use empty as a base case
    def grammer_rule(self, p):
        return p

    @_("")
    def empty(self, p):
        return p
```


### quadruples.py
Quadruples are a key part of the intermediate representation in the compilation process of the "Patito" language. They serve as a simplified and structured way to represent operations, making it easier to generate and execute machine-independent code.

A quadruple consists of four elements:

- Operator: The operation to be performed (e.g., +, -, *, /, relational operators, or control flow instructions like GOTO).
- Left Operand: The first input to the operation.
- Right Operand: The second input to the operation (optional, depending on the operator).
- Result: The location where the operation's result will be stored.

We used them in our neuralgic points in our parser module.

### memory.py
The memory.py file handles memory management for the "Patito" language compiler. This includes assigning memory addresses for variables, constants, and temporary values, as well as managing the allocation and deallocation of memory during execution. The file introduces several classes to streamline these operations.

The **Memory Address Offsets** dictionary defines the starting memory address ranges for various types of data, categorized by scope (global/local) and type (integer, float, boolean, etc.). These offsets ensure memory is organized and don't overlapping.

At compile time, the **Memory Assigner** class is responsible for assigning memory addresses during the compilation phase. It handles both global and local memory allocation and maintains a constant table for reuse of values.

At compile time, the **MemoryAssigner** is used to assign memory locations for variables and constants. These assignments are included in quadruples as pointers. 

At runtime, the **Memory** and **MemoryManager** classes simulate the actual execution of the program by reading, writing, and managing values at these memory addresses.


### symbol_table.py
The **Symbol Table** class is a data structure used in the compilation process of the "Patito" language. It maps identifiers (such as variable names, function names, or constants) to their associated metadata, such as types, memory addresses, and scopes.

The SymbolTable class manages a collection of Symbol instances. It supports:

- Declaration: Adds a new symbol to the table.
- Lookup: Retrieves a symbol by name, raising an exception if undeclared.
- Update: Modifies an existing symbol's metadata.
- Remove: Deletes a symbol from the table.

It is present thoughout the compilation process:

1. **Parsing**: During syntax analysis, the symbol table ensures all identifiers are declared before use and stores their types.
2. **Code Generation**: It provides memory addresses for identifiers, linking them to instructions in quadruples.
3. **Scope Management**: Nested or hierarchical symbol tables can represent different scopes (e.g., global, local).


### vm.py
The **VirtualMachine** class is for executing intermediate code represented as quadruples. This handles programming language runtime, memory management and the execution of operations defined by quadruples. It uses an instruction pointer that follows the input quadruple.

### semantics.py
The semantics module validates the compatibility of operations between different data types using a semantic cube, ensuring that operations like arithmetic and comparisons are type-appropriate. The validate_semantics function checks if the operands' types and the operator are valid and returns the resulting type or an "error" if the operation is not supported.

### operators.py
The operators module defines an enumeration of operators that can be used in various operations, such as arithmetic, comparisons, and control flow. The perform_operation function executes the specified operation between two operands based on the given operator and returns the result, supporting operations like addition, subtraction, and comparisons.

## Requirements

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

## Run

Output available commands
```bash
python main.py
```

```bash
python main.py build $filename
```

```bash
python main.py viz $filename
```

