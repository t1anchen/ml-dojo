import re
from string import ascii_letters
from typing import Dict, List


def p00_patatokukashiii(s1: str, s2: str) -> str:
    """
    >>> s1 = 'パトカー'
    >>> s2 = 'タクシー'
    >>> p00_patatokukashiii(s1, s2)
    'パタトクカシーー'
    """
    return "".join(c1 + c2 for c1, c2 in zip(s1, s2))


def p01_takushii(s: str) -> str:
    """
    >>> s = 'パタトクカシーー'
    >>> p01_takushii(s)
    'タクシー'
    """
    return s[1::2]


def p02_reverse(s: str) -> str:
    """
    >>> s = 'stressed'
    >>> p02_reverse(s)
    'desserts'
    """
    return s[::-1]


def p03(s: str) -> List[int]:
    """
    >>> s = 'Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics.'
    >>> p03(s)
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]
    """
    res: List[int] = []
    for word in s.split():
        c_count = sum(1 for c in word if c in ascii_letters)
        if c_count:
            res.append(c_count)
    return res


def p04(s: str):
    """
    >>> s = 'Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can.'
    >>> p04(s)
    {'H': 0, 'He': 1, 'Li': 2, 'Be': 3, 'B': 4, 'C': 5, 'N': 6, 'O': 7, 'F': 8, 'Ne': 9, 'Na': 10, 'Mi': 11, 'Al': 12, 'Si': 13, 'P': 14, 'S': 15, 'Cl': 16, 'Ar': 17, 'K': 18, 'Ca': 19}
    """
    mapping: Dict[str, int] = {}
    words = [re.sub(r"[^A-Za-z]", "", token) for token in s.split()]
    for i, word in enumerate(words):
        selected = ""
        if (i + 1) in [1, 5, 6, 7, 8, 9, 15, 16, 19]:
            selected = word[0]
        else:
            selected = word[:2]
        mapping[selected] = i
    return mapping
