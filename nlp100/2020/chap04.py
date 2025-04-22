from io import StringIO
from pathlib import Path
from typing import Generator
from zipfile import ZipFile

import pandas as pd


def p30() -> Generator[pd.DataFrame, None, None]:
    """
    >>> sum(1 for df in p30())
    1716
    """
    pos_zip_path = (
        (Path(__file__) / ".." / "data" / "alice.zip").resolve().as_posix()
    )
    pos_zip = ZipFile(pos_zip_path, metadata_encoding="utf-8")
    buf: list[str] = []
    with pos_zip:
        for file_in_archive in pos_zip.namelist():
            if file_in_archive.endswith(".conll"):
                with pos_zip.open(file_in_archive) as pos_coll:
                    pos_coll_content = pos_coll.read().decode("utf-8")
                    for line in pos_coll_content.splitlines():
                        if line == "\n" or line == "":
                            df = pd.read_csv(
                                StringIO("\n".join(buf)), sep="\t", header=None
                            )
                            yield df
                            buf.clear()
                        else:
                            buf.append(line)


def p31() -> Generator[pd.DataFrame, None, None]:
    for df in p30():
        pass


if __name__ == "__main__":
    import doctest

    doctest.testmod()
