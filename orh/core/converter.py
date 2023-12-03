import os

import pdfkit

# Other engine, weasyprint
# from weasyprint import HTML
# HTML(source).write_pdf(destination)

# WKHTMLTOPDF examples :
# options = {
#     "page-size": "Letter",
#     "margin-top": "0.75in",
#     "margin-right": "0.75in",
#     "margin-bottom": "0.75in",
#     "margin-left": "0.75in",
#     "encoding": "UTF-8",
#     "custom-header": [("Accept-Encoding", "gzip")],
#     "cookie": [
#         ("cookie-empty-value", '""'),
#         ("cookie-name1", "cookie-value1"),
#         ("cookie-name2", "cookie-value2"),
#     ],
#     "no-outline": None,
# }

DEFAULT_OPTIONS = {
    "page-size": "A4",
    "margin-top": "0.75in",
    "margin-right": "0.75in",
    "margin-bottom": "0.75in",
    "margin-left": "0.75in",
    "encoding": "UTF-8",
    "enable-local-file-access": True,
    "footer-font-size": 9,
    "footer-left": "[date]",
    "footer-right": "[page] / [topage]",
}
VERBOSE = True
DEFAULT_ENGINE = "pdfkit"


class Converter:
    def __init__(self, filepath, **kwargs):
        self.filepath = filepath
        self.css = []
        self._engine = kwargs.pop("engine") if "engine" in kwargs else DEFAULT_ENGINE

        path = kwargs.pop("path") if "path" in kwargs else False
        ignore_header = (
            kwargs.pop("ignore_header") if "ignore_header" in kwargs else False
        )
        ignore_footer = (
            kwargs.pop("ignore_footer") if "ignore_footer" in kwargs else False
        )
        self.options = DEFAULT_OPTIONS

        if path and not ignore_header:
            header = os.path.join(path, "header.html")
            if os.path.exists(header):
                self.options["header-html"] = header

        if path and not ignore_footer:
            footer = os.path.join(path, "footer.html")
            if os.path.exists(footer):
                self.options["footer-html"] = footer

        if kwargs:
            self.options.update(kwargs)

    def _get_engine(self):
        if self._engine == "pdfkit":
            return pdfkit.from_file

        raise NotImplementedError(f"'{self._engine}' engine not implemented.")

    def add_css(self, files):
        """Add stylesheets"""
        self.css = files

    def run(self, output):
        """Convert HTML to PDF"""
        func = self._get_engine()
        func(self.filepath, output, options=self.options, verbose=VERBOSE)
