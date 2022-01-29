import os
from contextlib import contextmanager
from typing import Optional

import fire
from jinja2 import Environment, FileSystemLoader
from release.utils import run_system_command

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def render_changelog(
    version: Optional[str] = None, previous_version: Optional[str] = None
):
    """Render Changelog from template

    Args:
        version (Optional[str], optional): render changelog for which version. Defaults to None, meaning the latest git tag veresion.
        previous_version (Optional[str], optional): render changelog since which verision. Defaults to None, meaning the one before the latest git tag version.
    """
    if version is None:
        

    res = j2_env.get_template("resources/changelog_template.md").render(
        version="0.0.1",
        prev_version="0.0.0",
        changes="test",
        commits=1,
    )


def entrypoint():
    fire.Fire(render_changelog)
