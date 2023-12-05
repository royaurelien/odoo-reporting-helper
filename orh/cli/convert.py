import logging
import pathlib

import click

from orh.core.converter import Converter
from orh.core.tools import download_file
from orh.core.html import *

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.FileHandler("./orh.log"))

DEFAULT_PAPER_FORMAT = "A4"
WORKDIR = pathlib.Path().absolute()


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
    """Convert an html source file to pdf."""

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
