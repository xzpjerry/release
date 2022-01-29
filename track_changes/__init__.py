import os
from typing import Optional

import fire
from jinja2 import Environment, FileSystemLoader
from track_changes.utils import run_system_command

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)


def render_changelog(
    version: Optional[str] = None, previous_version: Optional[str] = None
) -> None:
    """Render Changelog from template

    Args:
        version (Optional[str], optional): render changelog for which version. Defaults to None, meaning the latest git tag veresion.
        previous_version (Optional[str], optional): render changelog since which verision. Defaults to None, meaning the one before the latest git tag version.
    """
    if version is None:
        code, version, _ = run_system_command("git describe --tags --abbrev=0")
        assert code == 0, "Failed to get latest git tag version"
        version = version.strip()
    if previous_version is None:
        code, previous_version, _ = run_system_command(
            f"git describe --abbrev=0 --tags {version}^"
        )
        assert code == 0, "Failed to get previous git tag version"
        previous_version = previous_version.strip()
    code, changes, _ = run_system_command(
        f"git log --pretty=format:%s {previous_version}..{version}"
    )
    assert code == 0, "Failed to get git log"
    changes = changes.splitlines()
    print(
        j2_env.get_template("resources/changelog_template.md").render(
            version=version,
            prev_version=previous_version,
            changes=changes,
            commits=len(changes),
        )
    )


def entrypoint() -> None:
    fire.Fire(render_changelog)
