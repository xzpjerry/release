import os
import re
from typing import List, Optional, Tuple

import fire
from jinja2 import Environment, FileSystemLoader

from track_changes.utils import run_system_command

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
j2_env = Environment(trim_blocks=True)

default_template = os.path.join(THIS_DIR, r"resources\changelog_template.md")


def render_changelog(
    version: Optional[str] = None,
    previous_version: Optional[str] = None,
    out: Optional[str] = None,
    template: Optional[str] = default_template,
    regexps: Tuple[str] = ("^feat:|^fix:", "^ref:"),
) -> None:
    """Render Changelog from template

    Args:
        version (Optional[str], optional): render changelog for which version. Defaults to None, meaning the latest git tag veresion.
        previous_version (Optional[str], optional): render changelog since which verision. Defaults to None, meaning the one before the latest git tag version.
        out (Optional[str]): the output destination file location. Defaults to None, meaning the stdout.
        template (Optional[str]): output template. Defaults to package's changelog_template.md
        regexps (List[str]): Regular for filtering git records. if send None will grabbing all records.
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

    # record filtering
    if regexps:
        p = re.compile('(' + '|'.join(regexps) + ')')
        for change in changes.copy():
            if not re.match(p, change):
                changes.remove(change)

    assert os.path.exists(template), "template not found :{}".format(os.path.abspath(template))
    j2_env.loader = FileSystemLoader(os.path.dirname(template))
    res = j2_env.get_template(os.path.basename(template)).render(
        version=version,
        prev_version=previous_version,
        changes=changes,
        commits=len(changes),
    )

    if out is None:
        print(res)
    else:
        with open(out, "w", encoding="utf-8") as f:
            f.write(res)


def entrypoint() -> None:
    fire.Fire(render_changelog)
