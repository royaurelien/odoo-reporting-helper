import logging
import os
import re

import requests
from lxml import etree

import resource


_logger = logging.getLogger(__name__)

__all__ = ["limit_memory", "download_file"]


def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    _logger.info("soft: %s, hard: %s", soft, hard)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))


def download_file(url, filename=None, path=None, params=None):
    """Download file."""

    if not params:
        params = {}

    with requests.get(url, params=params, stream=True, timeout=60) as response:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            _logger.log(error)
            return False

        _logger.log(response.headers)

        content_disposition = response.headers["content-disposition"]
        fname = re.findall("filename=(.+)", content_disposition)[0]

        if not filename:
            filename = f"./{fname}" if fname else "./download"

        filepath = os.path.join(path, filename) if path else filename
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return filepath
