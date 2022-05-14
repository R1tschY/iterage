import os
import shutil
from pathlib import Path

import nox
from nox_poetry import Session, session

package = "iterage"
locations = "src", "tests", "noxfile.py"

default_python_version = "3.10"
python_versions = ["3.10", "3.9", "3.8", "3.7"]

nox.needs_version = ">= 2021.6.6"
nox.options.sessions = ("tests", "xdoctest", "lint", "mypy", "docs-build")


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install("coverage[toml]", "pytest", "pygments", "typeguard")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", f"--typeguard-packages={package}", *session.posargs)
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
def xdoctest(session: Session) -> None:
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
def mypy(session):
    args = session.posargs or ["src"]
    session.install("mypy")
    session.run("mypy", *args)


@session(name="docs-build", python=python_versions[0])
def docs_build(session: Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    if not session.posargs and "FORCE_COLOR" in os.environ:
        args.insert(0, "--color")

    session.install(".")
    session.install("sphinx", "sphinx-click", "furo", "myst-parser")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@session(python=python_versions[0])
def docs(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.install(".")
    session.install("sphinx", "sphinx-autobuild", "sphinx-click", "furo", "myst-parser")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
