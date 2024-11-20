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

`````bash
python main.py viz $filename
```

## Architecture

- Lexer
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


