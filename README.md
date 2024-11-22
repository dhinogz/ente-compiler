# Ente Language

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

## Files 

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

[quadruples](#quadruples.py)

### quadruples.py


### memory.py


### symbol_table.py


### vm.py


### operators.py


### semantics.py


### stack.py


### utils/viz.py

- Parser
    - In charge of semantic analysis, as well
    - Initialize before beginning parsing
        - function directory
        - scope stack
            - function declaration
        - id stack
            - variable declaration
        - jump stack
            - conditions and cycles
        - call stacks
            - functions
            - params
            - param types
        - expressions
            - operator stack
            - operand stack
            - operand type stack
        - Quadruples
        - Memory
    - Parsing certain stuff
        - Program Namespace
            - Variable and functions
            - Main namespace (Body)
                - Statements
                    - Assignment
                    - Functions
                    - Loops
                    - Conditions
        - Expressions
            - End


