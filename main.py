from lexer import EnteLexer
from parser import EnteParser
from pathlib import Path
import typer
from typing_extensions import Annotated

from quadruples import Quadruple
from vm import MemoryManager, VirtualMachine

cli = typer.Typer(no_args_is_help=True)


def read_ente_file(path_file: Path) -> str:
    if not path_file.is_file():
        print("not a file")
        raise typer.Abort()

    return path_file.read_text()


@cli.command("viz")
def generate_ast(
    file: Annotated[Path, typer.Argument()],
):
    from utils.ast_viz import draw_ast

    text = read_ente_file(file)

    lexer = EnteLexer()
    parser = EnteParser()
    res = parser.parse(lexer.tokenize(text))

    constant_table, counter_table = parser.memory_assigner.output()
    print(f"counter table {counter_table}\n")
    print(f"constant table {constant_table}\n")
    print(f"quadruples {parser.quadruples}\n")

    graph = draw_ast(res)
    output_filename = "tmp/ast_visualization"
    graph.render(output_filename, view=True)


@cli.command("run")
def test_cli(file: Annotated[Path, typer.Argument()]):
    text = read_ente_file(file)

    lexer = EnteLexer()
    parser = EnteParser()
    parser.parse(lexer.tokenize(text))

    print(parser.quadruples)

@cli.command("vm")
def run_vm(file: Annotated[Path, typer.Argument()]):
    memory_manager = MemoryManager()
    vm = VirtualMachine(memory_manager)

    quadruples = []

    text = read_ente_file(file)

    for line in text.splitlines():
        operator, left_operand, right_operand, result = line.split()
        q = Quadruple(int(operator), int(left_operand), int(right_operand), int(result))
        quadruples.append(q)

    vm.execute(quadruples)

if __name__ == "__main__":
    cli()
