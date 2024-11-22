from typing_extensions import Annotated
from pathlib import Path
import typer

from lexer import EnteLexer
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
    print(f"counter table {counter_table}\n")
    print(f"constant table {constant_table}\n")
    print(f"quadruples {parser.quadruples}\n")


@cli.command("run")
def run_vm(file: Annotated[Path, typer.Argument()]):
    if not file.is_file():
        print("not a file")
        raise typer.Abort()

    text = file.read_text()

    vm = VirtualMachine()

    quadruples = []
    for line in text.splitlines():
        operator, left_operand, right_operand, result = line.split()
        q = Quadruple(int(operator), int(left_operand), int(right_operand), int(result))
        quadruples.append(q)

    vm.execute(quadruples)


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
