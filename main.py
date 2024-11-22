from typing_extensions import Annotated
from pathlib import Path
import typer

from lexer import EnteLexer
from memory import MemoryManager
from parser import EnteParser

from quadruples import Quadruple
from vm import VirtualMachine

cli = typer.Typer(no_args_is_help=True)


@cli.command("build")
def build(file: Annotated[Path, typer.Argument()]):
    if not file.is_file():
        print("not a file")
        raise typer.Abort()

    text = file.read_text()

    lexer = EnteLexer()
    parser = EnteParser()
    parser.parse(lexer.tokenize(text))

    constant_table, counter_table = parser.memory_assigner.output()
    print(f"\ncounter table {counter_table}\n")
    print(f"constant table {constant_table}\n")
    print(f"quadruples {parser.quadruples}\n")

    output = (counter_table, constant_table, parser.quadruples)

    with open(f"out/test.en", "w") as bytecode:
        for _, table in output[0].items():
            for t, c in table.items():
                if type(c) == dict:
                    bytecode.write("~\n")
                    bytecode.write(f"{t}\n")
                    for t2, c2 in c.items():
                        bytecode.write(f"{t2}|{c2}\n")  # Updated separator to '|'
                else:
                    bytecode.write(f"{t}|{c}\n")  # Updated separator to '|'

        # Write constants section
        bytecode.write(":\n")
        for value, address in output[1].items():
            bytecode.write(f"{address}|{value}\n")  # Updated separator to '|'

        # Write quadruples section
        bytecode.write(":\n")
        bytecode.write(str(output[2]))


@cli.command("exec")
def run_vm(file: Annotated[Path, typer.Argument()]):
    if not file.is_file():
        print("not a file")
        raise typer.Abort()

    text = file.read_text()

    memory_manager = MemoryManager()
    vm = VirtualMachine(memory_manager)

    # Read and process the file
    line = text.splitlines()

    # Allocate memory segments
    idx = 0
    while line[idx] != "~" and line[idx] != ":":
        mem_type, size = line[idx].split("|")
        memory_manager.describe(mem_type=mem_type, size=int(size))
        idx += 1

    while line[idx] != ":":
        idx += 1
        function = line[idx]
        idx += 1
        while not (line[idx] == "~" or line[idx] == ":"):
            mem_type, size = line[idx].split("|")
            memory_manager.describe(
                mem_type=mem_type, size=int(size), function=function
            )
            idx += 1
    idx += 1

    # Allocate global memory
    for key, value in memory_manager.descriptor["global"].items():
        memory_manager.allocate(key, value)

    while line[idx] != ":":
        address, value = line[idx].split("|")
        memory_manager.assign(int(address), value)
        idx += 1

    idx += 1

    quads = []
    while idx < len(line):
        operator, left_operand, right_operand, result = line[idx].split(" ")
        q = Quadruple(int(operator), int(left_operand), int(right_operand), int(result))
        quads.append(q)
        idx += 1

    vm.execute(quads)


@cli.command("viz")
def generate_ast(
    file: Annotated[Path, typer.Argument()],
):
    from utils.ast_viz import draw_ast

    if not file.is_file():
        print("not a file")
        raise typer.Abort()

    text = file.read_text()

    lexer = EnteLexer()
    parser = EnteParser()
    res = parser.parse(lexer.tokenize(text))

    graph = draw_ast(res)
    output_filename = "tmp/ast_visualization"
    graph.render(output_filename, view=True)


if __name__ == "__main__":
    cli()
