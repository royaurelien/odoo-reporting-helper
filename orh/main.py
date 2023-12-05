import logging
import pathlib
import os
import click

from orh.cli.clean import clean
from orh.cli.convert import convert
from orh.cli.merge import merge

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
LOG_FILENAME = "orh.log"
LOG_FILEPATH = os.path.join(WORKDIR, LOG_FILENAME)

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.FileHandler(LOG_FILEPATH))


@click.group()
def cli():
    """Odoo Reporting Helper"""


cli.add_command(clean)
cli.add_command(convert)
cli.add_command(merge)
