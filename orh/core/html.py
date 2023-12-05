import os
import re

from lxml import etree


DEFAULT_ATTRIBUTES_TO_CLEAN = [
    # "class",
    # "style",
    "data-domain",
    "data-oe-type",
    "data-res-model",
    "data-oe-expression",
    "data-active-id",
]

__all__ = [
    "get_tree",
    "get_base_url",
    "extract_tag",
    "get_stylesheets",
    "get_js_scripts",
    "fix_url",
    "fix_stylesheets",
    "compile_stylesheets",
    "fix_stylesheets_url",
    "add_style",
    "remove_html_attrs",
    "tree_to_string",
    "remove_empty_lines",
    "remove_div",
]


def get_tree(text):
    """Helper: return etree"""
    parser = etree.HTMLParser()
    tree = etree.fromstring(text, parser)

    return tree


def get_base_url(tree, remove=True):
    """Extract and remove base url."""

    attr = "web-base-url"
    html = tree.xpath("//html")[0]

    try:
        # <html web-base-url="xxx">
        base_url = html.get(attr)
        if remove:
            html.attrib.pop(attr)
    except KeyError:
        # <base href=xxx>
        tag = tree.xpath("//base")[0]
        base_url = tag.get("href")
        if remove:
            tag.getparent().remove(tag)

    return base_url, tree


def extract_tag(tree, name, attrib, **kwargs):
    """Extract and remove HTML attribute."""

    remove = kwargs.get("remove", False)
    res = []
    for tag in tree.iter(name):
        data = tag.attrib.get(attrib)
        res.append(data)

        if remove:
            tag.getparent().remove(tag)

    return res, tree


def get_stylesheets(tree, remove=False):
    """Return the url list of stylesheets."""

    return extract_tag(tree, "link", "href", remove=remove)


def get_js_scripts(tree, remove=False):
    """Return the url list of JS scripts."""

    return extract_tag(tree, "script", "src", remove=remove)


# def stylesheet_to_url(url, filepath):
#     filename = os.path.basename(filepath)
#     url = f"{url}{filepath}"

#     return url, filename


def fix_url(text, url):
    """Fix url in string (relative to absolute)."""

    res = text.replace("url('/web/", f"url('{url}/web/")
    res = res.replace("url(/web/", f"url({url}/web/")
    res = res.replace('url("/web', f'url("{url}/web/')

    return res


def fix_stylesheets(files, path=None):
    """Fix stylesheets filepath."""

    def fix(file):
        filename = os.path.basename(file)
        return os.path.join(path, filename) if path else filename

    return list(map(fix, files))


def compile_stylesheets(files, url=None, path=None):
    """Merging external style sheets into the main HTML document."""
    res = []
    if path:
        files = [os.path.join(path, filename) for filename in files]

    for filepath in files:
        with open(filepath, encoding="utf-8") as f:
            if url:
                res.append(fix_url(f.read(), url))
            else:
                res.append(f.read())

    return r"\n".join(res)


def fix_stylesheets_url(files, url, path=None):
    """Help: fix stylesheets urls;"""

    if path:
        files = [os.path.join(path, filename) for filename in files]

    for filepath in files:
        with open(filepath, encoding="utf-8") as f:
            content = fix_url(f.read(), url)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


def add_style(tree, content):
    """Helper: add style tag with content."""

    head = tree.find("head")
    tag = etree.SubElement(head, "style")

    tag.set("type", "text/css")
    tag.text = content

    return tree


def remove_html_attrs(tree, attributes=None):
    """Filter and remove HTML attributes."""

    if not attributes:
        attributes = DEFAULT_ATTRIBUTES_TO_CLEAN

    for attr in attributes:
        for tag in tree.xpath(f"//*[@{attr}]"):
            tag.attrib.pop(attr)

    return tree


def tree_to_string(tree):
    """Generate HTML from etree."""

    # Use method as HTML to prevent self-closing tag

    return etree.tostring(tree, encoding="unicode", pretty_print=True, method="html")


def remove_empty_lines(text):
    """Helper: remove empty lines."""
    text = re.sub(r"\n+", "\n", text).strip("\n")
    res = os.linesep.join([line for line in text.splitlines() if line.strip() != ""])

    return res


def remove_div(text):
    """Helper: remove dirty DIV."""
    return re.sub(r"\<div\/\>", "", text).strip("\n")
