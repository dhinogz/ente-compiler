from lexer import EnteLexer
from parser import EnteParser
from pathlib import Path
import typer
from typing_extensions import Annotated
from typing import Optional

cli = typer.Typer(no_args_is_help=True)


def read_ente_file(path_file: Path) -> str:
    if path_file is None:
        print("no input given")
        raise typer.Abort()

    if not path_file.is_file():
        print("not a file")
        raise typer.Abort()

    return path_file.read_text()


@cli.command("ast")
def generate_ast(
    file: Annotated[Path, typer.Argument()],
    graphic: bool = False,
):
    from utils.ast_viz import draw_ast, draw_ast_terminal

    text = read_ente_file(file)

    lexer = EnteLexer()
    parser = EnteParser()
    res = parser.parse(lexer.tokenize(text))

    print(draw_ast_terminal(res))

    if graphic:
        graph = draw_ast(res)
        output_filename = "ast_visualization"
        graph.render(output_filename, view=True)


@cli.command("run")
def test_cli(file: Annotated[Path, typer.Argument()]):
    text = read_ente_file(file)

    lexer = EnteLexer()
    parser = EnteParser()
    parser.parse(lexer.tokenize(text))

    print(parser.scope)
    print(parser.directory)
    print(parser.types)


if __name__ == "__main__":
    cli()
    # print(res)
