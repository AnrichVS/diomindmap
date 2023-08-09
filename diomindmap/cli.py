"""This module provides the DioMindmap CLI."""

from typing import Optional
from pathlib import Path

import typer
from typing_extensions import Annotated

from diomindmap import __app_name__, __version__
from diomindmap.mindmap import MindMap

app = typer.Typer()


@app.command()
def generate(
        input: Annotated[Path, typer.Option(
            ...,
            "--input", "-i",
            help="The source text file to read from.",
        )],
        output: Annotated[Path, typer.Option(
            ...,
            "--output", "-o",
            help="The destination file to write to.",
        )],
        max_brightness_offset: Annotated[Optional[int], typer.Option(
            ...,
            "--max-brightness-offset", "-b",
            help="The maximum brightness offset between the base color and leaf nodes",
        )] = 10,
        colors: Annotated[Optional[list[str]], typer.Option(
            ...,
            "--colors", "-c",
            help="Base colors for children of the diagram root node. The default is based on 95% "
                 "accessibility contrast ratio: https://sashamaps.net/docs/resources/20-colors/",
        )] = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6',
              '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3',
              '#808000', '#ffd8b1', '#000075'],
) -> None:
    """
    Generate a Draw.io diagram from a text file.
    """
    file_content = open(input, 'r').read()

    mindmap = MindMap(file_content, colors=colors, max_brightness_offset=max_brightness_offset)
    diagram = mindmap.diagram

    with open(output, 'w') as file:
        file.write(diagram.dump_xml())


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Annotated[bool, typer.Option(
            ...,
            "--version", "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )] = False,
) -> None:
    return
