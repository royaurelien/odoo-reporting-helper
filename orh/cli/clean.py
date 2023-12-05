import pathlib

import click

from orh.core.html import (
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
    stylesheet_to_url,
    tree_to_string,
)
from orh.core.tools import download_file, set_memory_limit

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
@click.option(
    "--cookies",
    "-c",
    is_flag=False,
    type=str,
    help="Cookies",
)
@click.option(
    "--limit-memory",
    "-l",
    is_flag=True,
    default=False,
    type=bool,
    help="Set memory limit.",
)
def clean(source, destination, **kwargs):
    """Clean and prepare html sources."""

    remove_stylesheets = kwargs.get("include_stylesheets", False)
    remove_js = not kwargs.get("include_javascripts", False)
    download_stylesheets = False
    local_stylesheets = True
    cookies = not kwargs.get("cookies", False)
    limit_memory = not kwargs.get("limit_memory", False)

    if limit_memory:
        set_memory_limit()

    with open(source, encoding="utf-8") as r, open(
        destination, "w", encoding="utf-8"
    ) as o:
        for line in r:
            if line.strip():
                o.write(line)

    with open(destination, encoding="utf-8") as file:
        tree = get_tree(file.read())

    base_url, tree = get_base_url(tree)

    _, tree = get_js_scripts(tree, remove_js)
    stylesheets, tree = get_stylesheets(tree, remove_stylesheets)
    to_fix = None

    if stylesheets:
        new_stylesheets = []

        if local_stylesheets:
            new_stylesheets = fix_stylesheets(stylesheets, WORKDIR)
            to_fix = zip(stylesheets, new_stylesheets)

        if download_stylesheets:
            for url, filename in [
                stylesheet_to_url(base_url, file) for file in stylesheets
            ]:
                options = {"cookies": cookies} if cookies else {}
                filepath = download_file(url, filename, WORKDIR, **options)
                new_stylesheets.append(filepath)

        if new_stylesheets:
            stylesheets = new_stylesheets

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
