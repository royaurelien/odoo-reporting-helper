from setuptools import find_packages, setup

setup(
    name="odoo-reporting-helper",
    version="0.0.2",
    description="Odoo Reporting Helper",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/royaurelien/odoo-reporting-helper",
    author="Aurelien ROY",
    author_email="roy.aurelien@gmail.com",
    license="BSD 2-clause",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "lxml",
        "pdfkit",
        "requests",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "orh = orh.main:cli",
        ],
    },
)
