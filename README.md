
# Odoo Reporting Helper

_**ORH** Command Line Tool_

![PyPI](https://img.shields.io/pypi/v/odoo-reporting-helper) ![PyPI](https://img.shields.io/pypi/pyversions/odoo-reporting-helper)

## Requirements

Wkhtmltopdf download page: https://wkhtmltopdf.org/downloads.html

Installation script : https://raw.githubusercontent.com/JazzCore/python-pdfkit/master/ci/before-script.sh

See options : https://wkhtmltopdf.org/usage/wkhtmltopdf.txt

## Installation

Install from PyPI:
```bash
pip install odoo-reporting-helper
```

## Quickstart


### Clean and prepare HTML
```bash
orh clean <source> <destination>
```

Options:

```
  -s, --include-stylesheets  Compile and include external stylesheets in HTML
                             report.
  -j, --include-javascripts  Keep JS scripts.
  -c, --cookies TEXT         Cookies
  -l, --limit-memory         Set memory limit.
```

### Merge stylesheets (optional)
```bash
orh merge <source> <destination>

```

### Generate PDF
* PDF Report :
```bash
orh convert <source> <destination> --format A3 --landscape --ignore-header --ignore-footer
```
