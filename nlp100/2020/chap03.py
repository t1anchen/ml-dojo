from __future__ import annotations

import gzip
import json
import re
from pathlib import Path
from typing import Generator, Iterable, Match, Optional, TypeVar
from urllib.parse import unquote

T = TypeVar("T")


def p20(multipline: bool = True) -> Generator[str, None, None]:
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


def select_inside_parenthese(
    paragraph: str, parentheses: str, auxilary_pattern: re.Pattern[str]
) -> Generator[str, None, None]:
    left, right = parentheses.split(",")
    level: list[str] = []
    is_selected = False
    for line in paragraph.split("\n"):
        if left in line:
            if auxilary_pattern.match(line):
                is_selected = True
            level.append(left)
        if right in line:
            if len(level):
                level.pop()
            if is_selected and len(level) == 0:
                is_selected = False
                yield line
                break
        if is_selected:
            yield line


def first(stream: Iterable[T]) -> Generator[T, None, None]:
    first_elem = None
    for x in stream:
        first_elem = x
        break
    if first_elem is not None:
        yield first_elem


def last(stream: Iterable[T]) -> Generator[T, None, None]:
    last_elem = None
    for x in stream:
        last_elem = x
    if last_elem is not None:
        yield last_elem


def double_ends(stream: Iterable[T]) -> tuple[Optional[T], Optional[T]]:
    first_elem, last_elem = None, None
    for x in stream:
        first_elem = x
        last_elem = x
        break
    for x in stream:
        last_elem = x
    return first_elem, last_elem


def p21():
    """
    >>> first_elem, last_elem = double_ends(p21())
    >>> first_elem
    '[[Category:United Kingdom| ]]'
    >>> last_elem
    '[[Category:Western European countries]]'
    """
    for line in p20():
        if line.strip().startswith("[[Category"):
            yield line


def p22():
    """
    >>> first_elem, last_elem = double_ends(p22())
    >>> first_elem
    'United Kingdom|'
    >>> last_elem
    'Western European countries'
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
    >>> first_elem, last_elem = double_ends(p24())
    >>> first_elem
    'Royal Coat of Arms of the United Kingdom.svg'
    >>> last_elem
    'Britannia-Statue.jpg'
    """
    pat = re.compile(r"\[\[File:(.*?)\|")
    for line in p20():
        for matched in pat.finditer(line):
            yield matched.group(1)


class Block:
    def __init__(self, name: str, lines: list[str], block_type: str):
        self.content = lines
        self.block_type = block_type
        self.name = name

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self)

    def to_dict(self) -> dict[str, str]:
        return {
            "content": "\n".join(self.content),
            "block_type": self.block_type,
            "name": self.name,
        }

    @staticmethod
    def from_stream(stream: Iterable[str]) -> Generator[Block, None, None]:
        collected: list[str] = []
        name = "Unknown"
        block_type = "Unknown"
        block_start, block_end = "{{,}}".split(",")
        is_selected = False
        block_name_pat = re.compile(r"\|\s*(\w+)\s*=\s*\{\{(\w+)\s*(.*)")
        for line in stream:
            if block_start in line and block_end in line:
                block_pos_start, block_pos_end = line.find(
                    block_start
                ), line.find(block_end)
                collected.append(line[block_pos_start + 2 : block_pos_end])
                is_selected = False
                if matched := block_name_pat.match(line):
                    name = matched.group(1)
                    block_type = matched.group(2)
                    content_first_line = matched.group(3)
            elif block_start in line:
                block_pos_start = line.find(block_start)
                is_selected = True
                if matched := block_name_pat.match(line):
                    name = matched.group(1)
                    block_type = matched.group(2)
                    content_first_line = matched.group(3)
                    if content_first_line:
                        collected.append(content_first_line)
            elif block_end in line:
                block_pos_end = line.find(block_end)
                collected.append(line[:block_pos_end])
                yield Block(name, collected, block_type)
                collected = []
                is_selected = False
            else:
                if is_selected and line:
                    collected.append(line)


def p25() -> dict[str, str | Block]:
    """
    >>> res = p25()
    >>> res.get('common_name', None)
    'United Kingdom'
    """
    text = "\n".join(p20(True))
    parentheses = "{{,}}"
    auxilary_pattern = re.compile(r".*Infobox.*")
    pat_fields = re.compile(r"\|(.*?) = (.*)")
    res: dict[str, str | Block] = {}

    for line in select_inside_parenthese(text, parentheses, auxilary_pattern):
        if fields := pat_fields.search(line):
            key = fields.group(1).strip()
            val = fields.group(2).strip()
            res[key] = val

    for block in Block.from_stream(
        select_inside_parenthese(text, parentheses, auxilary_pattern)
    ):
        key = block.name
        res[key] = block

    return res


def p26():
    """
    >>> for k, v in p26().items():
    ...     if isinstance(v, str):
    ...         assert "''" not in v
    ...
    """
    pat = re.compile(r"(\'+)(.*?)(\'+)")
    res: dict[str, str | Block] = {}
    for key, val in p25().items():
        if isinstance(val, str):
            val_new = pat.sub(lambda x: x.group(2), val)
            if val != val_new:
                res[key] = val_new
            else:
                res[key] = val
        if isinstance(val, Block):
            if len(val.content):
                for i, line_val in enumerate(val.content):
                    line_val_new = pat.sub(lambda x: x.group(2), line_val)
                    if line_val != line_val_new:
                        val.content[i] = line_val_new
            res[key] = val

    return res


def p27():
    pat = re.compile(r"\[\[([^\|]*)\|?(.*)\]\]")

    def is_internal_link(val: str) -> Optional[Match[str]]:
        return pat.search(val)

    def remove_internal_link(matched: Match[str]) -> str:
        link, _ = matched.groups()
        return link

    res: dict[str, str | Block] = {}
    for key, val in p26().items():
        if isinstance(val, str):
            if matched := is_internal_link(val):
                val_new = remove_internal_link(matched)
                res[key] = val_new
            else:
                res[key] = val
        else:
            res[key] = val
    return res


if __name__ == "__main__":
    import doctest

    doctest.testmod()
