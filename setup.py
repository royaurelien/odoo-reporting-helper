from setuptools import find_packages, setup

setup(
    name="orh",
    version="0.0.1",
    description="Odoo Reporting Helper",
    url="https://github.com/royaurelien/odoo-reporting-helper",
    author="Aurelien ROY",
    author_email="roy.aurelien@gmail.com",
    license="BSD 2-clause",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "lxml",
        "pdfkit",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "orh = orh.cli.main:cli",
        ],
    },
)
