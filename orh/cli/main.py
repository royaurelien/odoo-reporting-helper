import logging
import pathlib

import click

from orh.core.converter import Converter
from orh.core.tools import (
    add_style,
    compile_stylesheets,
    fix_stylesheets,
    fix_stylesheets_url,
    get_base_url,
    get_js_scripts,
    get_stylesheets,
    get_tree,
    remove_div,
    remove_empty_lines,
    remove_html_attrs,
    tree_to_string,
)

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.FileHandler("./orh.log"))

DEFAULT_PAPER_FORMAT = "A4"
WORKDIR = pathlib.Path().absolute()


@click.group()
def cli():
    """Odoo Reporting System"""


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


@click.command()
@click.argument("source")
@click.argument("destination")
@click.option(
    "--format",
    "-f",
    required=False,
    default=DEFAULT_PAPER_FORMAT,
    type=str,
    help="Paper Format: A4, A3, Letter...",
)
@click.option(
    "--landscape",
    "-l",
    is_flag=True,
    default=False,
    type=bool,
    help="Landscape orientation.",
)
@click.option(
    "--ignore-header",
    is_flag=True,
    default=False,
    type=bool,
    help="Ignore header if presents.",
)
@click.option(
    "--ignore-footer",
    is_flag=True,
    default=False,
    type=bool,
    help="Ignore footer if presents.",
)
def convert(source, destination, landscape, **kwargs):
    options = {
        "page-size": kwargs.get("format"),
        "path": WORKDIR,
        "ignore_header": kwargs.get("ignore_header", False),
        "ignore_footer": kwargs.get("ignore_footer", False),
    }

    if landscape:
        options["orientation"] = "Landscape"

    converter = Converter(source, **options)
    converter.run(destination)


@click.command()
@click.argument("source")
@click.argument("destination")
def merge(source, destination, **kwargs):
    """Merge stylesheets into main HTML file."""

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


cli.add_command(clean)
cli.add_command(convert)
cli.add_command(merge)
