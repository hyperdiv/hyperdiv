#!/usr/bin/env python

import sys
import os
import click
import shutil
from importlib.metadata import version


def get_version():
    # Note: This assumes that hyperdiv is installed in the current
    # virtualenv or distribution. This assumption holds when
    # developing locally with poetry, because `poetry install`
    # installs the local project into the virtualenv, using a `.pth`
    # alias.
    return version("hyperdiv")


@click.group()
@click.version_option(get_version(), prog_name="Hyperdiv")
def cli():
    """Hyperdiv command-line utility."""


@cli.command("docs")
def docs():
    """Open the Hyperdiv documentation."""
    docs_app_location = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "hyperdiv-docs",
            "start.py",
        )
    )

    if not os.path.isfile(docs_app_location):
        print("ERROR: Cannot find the docs app :(")
        sys.exit(1)

    python = shutil.which("python3")
    if not python:
        python = shutil.which("python")

    if not python:
        print("ERROR: Cannot find python3 or python")
        sys.exit(1)

    os.environ["HD_PRODUCTION_LOCAL"] = "1"
    os.execl(python, "python", docs_app_location)


if __name__ == "__main__":
    cli()
