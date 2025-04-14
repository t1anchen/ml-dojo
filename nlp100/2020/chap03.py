import gzip
import json
import re
from pathlib import Path
from typing import Generator
from urllib.parse import unquote


def p20(multipline=True) -> Generator[str, None, None]:
    json_path = (
        (Path(__file__) / ".." / "data" / "enwiki-country.json.gz")
        .resolve()
        .as_posix()
    )
    with gzip.open(json_path) as gf:
        content = gf.read().decode()
        for record in content.splitlines():
            obj = json.loads(record)
            if "United Kingdom" in obj["title"]:
                content: str = obj["text"]
                if multipline:
                    for line in content.split("\n"):
                        yield unquote(line)
                else:
                    yield unquote(content)

def select_inside_parenthese(paragraph: str, parentheses: str) -> str:
    left, right = parentheses.split(",")
    selected = []
    level = []
    is_inside_parentheses = False
    for line in paragraph.split():
        if line.startswith(left):
            is_inside_parentheses
            selected.append(line)


def p21():
    """
    >>> for line in p21():
    ...     print(line)
    ...
    [[Category:United Kingdom| ]]
    ...
    [[Category:Western European countries]]
    """
    for line in p20():
        if line.strip().startswith("[[Category"):
            yield line


def p22():
    """
    >>> for line in p22():
    ...     print(line)
    ...
    United Kingdom|
    ...
    Western European countries
    """
    pat = re.compile(r"\[\[Category:(.+)\]\]")
    for line in p21():
        yield re.sub(pat, r"\1", line).strip()


def p23():
    """
    >>> {'level': 1, 'name': 'History'} in p23()
    True
    """
    pat = re.compile(r"([=]+)([^=]+)([=]+)")
    for line in p20():
        if matched := pat.match(line):
            prefix, title, _ = matched.groups()
            yield {"level": len(prefix) - 1, "name": title.strip()}


def p24():
    """
    >>> for media_file in p24():
    ...     print(media_file)
    ...
    Royal Coat of Arms of the United Kingdom.svg
    ...
    Britannia-Statue.jpg
    """
    pat = re.compile(r"\[\[File:(.*?)\|")
    for line in p20():
        for matched in pat.finditer(line):
            yield matched.group(1)


def p25() -> dict[str, str]:
    """
    >>> res = p25()
    >>> res.get('common_name', None)
    'United Kingdom'
    """
    pat_infobox = re.compile(r"{{Infobox country(.*?}})", re.DOTALL)
    pat_fields = re.compile(r"\|(.*?) = (.*)")
    text = "\n".join(line for line in p20())
    matched = pat_infobox.search(text)
    res: dict[str, str] = {}
    if matched:
        infobox_lines = matched.group(0).split("\n")
        for line in infobox_lines:
            if (
                line.startswith("|")
                and (fields := pat_fields.search(line)) is not None
            ):
                key = fields.group(1).strip()
                val = fields.group(2).strip()
                res[key] = val
    return res


def p26():
    """
    >>> p26()
    """
    res: dict[str, str] = {}
    pat = re.compile(r"(\'+)(.*?)(\'+)")
    res: dict[str, str] = {}
    for key, val in p25().items():
        val_new = pat.sub(lambda x: x.group(2), val)
        if val != val_new:
            print(val_new)
        res[key] = val_new
    return res


if __name__ == "__main__":
    import doctest

    doctest.testmod()
