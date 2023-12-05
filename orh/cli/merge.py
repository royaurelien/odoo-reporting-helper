import logging
import pathlib

import click

from orh.core.converter import Converter
from orh.core.html import *


@click.command()
@click.argument("source")
@click.argument("destination")
def merge(source, destination):
    """Merge stylesheets into a single HTML file."""

    with open(source, encoding="utf-8") as file:
        tree = get_tree(file.read())

    remove_stylesheets = True
    stylesheets, tree = get_stylesheets(tree, remove_stylesheets)

    content = compile_stylesheets(stylesheets)
    tree = add_style(tree, content)

    html = tree_to_string(tree)
    html = remove_empty_lines(html)

    with open(destination, "w", encoding="utf-8") as file:
        file.write(html)
