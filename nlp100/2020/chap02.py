import re
import subprocess
from pathlib import Path

txt_path: str = (
    (Path(__file__) / ".." / "data" / "popular-names.txt").resolve().as_posix()
)


def p10():
    """
    >>> p10()
    '2780'
    """

    res = subprocess.run(
        f"wc -l {txt_path}", capture_output=True, shell=True, encoding="utf-8"
    )
    if (matched := re.findall(r"\d+", res.stdout)) and len(matched):
        return matched[0]
    else:
        return None
