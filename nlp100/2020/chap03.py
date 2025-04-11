import gzip
import json
from pathlib import Path
from typing import Optional


def p20() -> Optional[dict[str, str]]:
    """
    >>> p20()
    """
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
                print(obj["text"])
                with open("./article.txt", "w", encoding="utf-8") as article:
                    json.dump(
                        obj["text"], article, ensure_ascii=False, indent=2
                    )
                return obj
    return None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
