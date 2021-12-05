import os
from pathlib import Path

import nox
from nox_poetry import Session, session

package = "iterage"
locations = "src", "tests", "noxfile.py"

default_python_version = "3.9"
python_versions = ["3.10", "3.9", "3.8", "3.7"]

nox.needs_version = ">= 2021.6.6"
nox.options.sessions = ("test", "doctest", "lint", "typecheck")


@session(python=python_versions)
def test(session: Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install("coverage[toml]", "pytest", "pygments")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@session(python=default_python_version)
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@nox.session(python=python_versions)
def doctest(session: Session) -> None:
    """Run examples with xdoctest."""
    if session.posargs:
        args = [package, *session.posargs]
    else:
        args = [f"--modname={package}", "--command=all"]
        if "FORCE_COLOR" in os.environ:
            args.append("--colored=1")

    session.install(".")
    session.install("xdoctest[colors]")
    session.run("python", "-m", "xdoctest", *args)


@nox.session(python=[default_python_version])
def fmt(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=[default_python_version])
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-bandit",
        "flake8-bugbear",
        "flake8-import-order",
        "flake8-docstrings",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python=[default_python_version])
def typecheck(session):
    args = session.posargs or ["src"]
    session.install("mypy")
    session.run("mypy", *args)


@nox.session(python=[default_python_version])
def doc(session: Session) -> None:
    """Build the documentation."""
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "build/docs")
