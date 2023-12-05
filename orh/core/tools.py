import logging
import os
import re
import resource

import requests

_logger = logging.getLogger(__name__)

__all__ = ["limit_memory", "download_file"]

DEFAULT_FILENAME = "download"
DEFAULT_MEMORY_LIMIT = 4294967296


def set_memory_limit(maxsize=None):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    _logger.info("Memory limited to: %s soft, %s hard.", soft, hard)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize or DEFAULT_MEMORY_LIMIT, hard))


def download_file(url, filename=None, path=None, params=None, **kwargs):
    """Download file."""

    if not params:
        params = {}

    cookies = kwargs.get("cookie")

    if cookies:
        req = requests.Session()
        name, value = cookies.split("=")
        req.cookies.set(name, value)
    else:
        req = requests

    with req.get(url, params=params, stream=True, timeout=60) as response:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            _logger.log(error)
            return False

        _logger.debug(response.headers)

        if "content-disposition" in response.headers and not filename:
            content_disposition = response.headers["content-disposition"]
            fname = re.findall("filename=(.+)", content_disposition)[0]
            filename = f"./{fname}" if fname else DEFAULT_FILENAME

        if not filename:
            filename = DEFAULT_FILENAME

        filepath = os.path.join(path, filename) if path else filename

        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return filepath
