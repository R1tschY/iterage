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


@nox.session(python=python_versions)
def doctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install("xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


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
    args = session.posargs or locations
    session.install(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=[default_python_version])
def doc(session: Session) -> None:
    """Build the documentation."""
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "build/docs")
