
# Odoo Reporting Helper

_**ORH** Command Line Tool_

![PyPI](https://img.shields.io/pypi/v/odoo-reporting-helper) ![PyPI](https://img.shields.io/pypi/pyversions/odoo-reporting-helper)


## Installation

Install from PyPI:
```bash
pip install odoo-reporting-helper
```

## Quickstart


### Clean and prepare HTML
`path` is the local repository you want to inspect.
```bash
orh clean <source> <destination>
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
