import logging
import pathlib

import click

from orh.core.converter import Converter
from orh.core.tools import download_file
from orh.core.html import *

# from orh.core.tools import (
#     add_style,
#     compile_stylesheets,
#     fix_stylesheets,
#     fix_stylesheets_url,
#     get_base_url,
#     get_js_scripts,
#     get_stylesheets,
#     get_tree,
#     remove_div,
#     remove_empty_lines,
#     remove_html_attrs,
#     tree_to_string,
# )


WORKDIR = pathlib.Path().absolute()


@click.command()
@click.argument("source")
@click.argument("destination")
@click.option(
    "--include-stylesheets",
    "-s",
    is_flag=True,
    default=False,
    type=bool,
    help="Compile and include external stylesheets in HTML report.",
)
@click.option(
    "--include-javascripts",
    "-j",
    is_flag=True,
    default=False,
    type=bool,
    help="Keep JS scripts.",
)
def clean(source, destination, **kwargs):
    """Clean and prepare html sources."""

    # limit_memory(4294967296)
    remove_stylesheets = kwargs.get("include_stylesheets", False)
    remove_js = not kwargs.get("include_javascripts", False)
    # download_stylesheets = False
    local_stylesheets = True

    with open(source, encoding="utf-8") as r, open(
        destination, "w", encoding="utf-8"
    ) as o:
        for line in r:
            if line.strip():
                o.write(line)

    with open(destination, encoding="utf-8") as file:
        tree = get_tree(file.read())

    base_url, tree = get_base_url(tree)
    print("base url: %s", base_url)
    _, tree = get_js_scripts(tree, remove_js)
    stylesheets, tree = get_stylesheets(tree, remove_stylesheets)
    to_fix = None

    if stylesheets:
        print(stylesheets)
        new_stylesheets = []

        if local_stylesheets:
            new_stylesheets = fix_stylesheets(stylesheets, WORKDIR)
            to_fix = zip(stylesheets, new_stylesheets)

        # if download_stylesheets:
        #     for url, filename in [
        #         stylesheet_to_url(base_url, file) for file in stylesheets
        #     ]:
        #         filepath = download_file(url, filename, WORKDIR)
        #         new_stylesheets.append(filepath)

        if new_stylesheets:
            stylesheets = new_stylesheets

        print(stylesheets)

        if remove_stylesheets:
            content = compile_stylesheets(stylesheets, base_url, WORKDIR)
            tree = add_style(tree, content)
        else:
            fix_stylesheets_url(stylesheets, base_url, WORKDIR)

    tree = remove_html_attrs(tree)
    html = tree_to_string(tree)

    if to_fix:
        for old_file, new_file in to_fix:
            html = html.replace(old_file, new_file)

    html = remove_empty_lines(remove_div(html))

    with open(destination, "w", encoding="utf-8") as file:
        file.write(html)
