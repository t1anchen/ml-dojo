from pathlib import Path
from zipfile import ZipFile


def p30():
    """
    >>> p30()
    """
    pos_zip_path = (
        (Path(__file__) / ".." / "data" / "alice.zip").resolve().as_posix()
    )
    pos_zip = ZipFile(pos_zip_path, metadata_encoding="utf-8")
    buf: list[str] = []
    is_selected = False
    with pos_zip:
        for file_in_archive in pos_zip.namelist():
            if file_in_archive.endswith(".conll"):
                with pos_zip.open(file_in_archive) as pos_coll:
                    pos_coll_content = pos_coll.read().decode("utf-8")
                    for line in pos_coll_content.splitlines():
                        print(line)
                        break


if __name__ == "__main__":
    import doctest

    doctest.testmod()
