import re
from random import randint
from typing import Generator


def p00(s: str) -> str:
    """
    >>> s = 'stressed'
    >>> p00(s)
    'desserts'
    """
    return s[::-1]


def p01(s: str) -> str:
    """
    >>> p01('schooled')
    'shoe'
    """
    res: list[str] = []
    for i in [1, 3, 5, 7]:
        res.append(s[i - 1])
    return "".join(res)


def p02(s1: str, s2: str) -> str:
    """
    >>> p02('shoe', 'cold')
    'schooled'
    """
    return "".join(a + b for a, b in zip(s1, s2))


def p03(s: str) -> list[int]:
    """
    >>> s = 'Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics.'
    >>> p03(s)
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]
    """
    res: list[int] = []
    pat = re.compile(r"[^A-Za-z]*")
    for token in s.split():
        res.append(len(pat.sub("", token)))
    return res


def p04(s: str) -> dict[str, int]:
    """
    >>> s = 'Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can.'
    >>> p04(s)
    {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Na': 11, 'Mi': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20}
    """
    res: dict[str, int] = {}
    for i, token in enumerate(s.split()):
        if (i + 1) in [1, 5, 6, 7, 8, 9, 15, 16, 19]:
            key = token[0]
        else:
            key = token[:2]
        res[key] = i + 1
    return res


def p05(s: str) -> dict[str, set[str]]:
    """
    >>> s = 'I am an NLPer'
    >>> sorted(p05(s)['word_level'])
    ['I-am', 'am-an', 'an-NLPer']
    >>> sorted(p05(s)['character_level'])
    [' N', ' a', 'I ', 'LP', 'NL', 'Pe', 'am', 'an', 'er', 'm ', 'n ']
    """
    res: dict[str, set[str]] = {"word_level": set(), "character_level": set()}
    left, right = iter(s.split()), iter(s.split())
    next(right, None)
    for token1, token2 in zip(left, right):
        res["word_level"].add(token1 + "-" + token2)
    left, right = iter(s), iter(s)
    next(right, None)
    for token1, token2 in zip(left, right):
        res["character_level"].add(token1 + token2)
    return res


def p06(X: set[str], Y: set[str]) -> dict[str, list[str] | bool]:
    """
    >>> X = p05('paraparaparadise')['character_level']
    >>> Y = p05('paragraph')['character_level']
    >>> p06(X, Y)
    {'union': ['ad', 'ag', 'ap', 'ar', 'di', 'gr', 'is', 'pa', 'ph', 'ra', 'se'], 'intersection': ['ap', 'ar', 'pa', 'ra'], 'difference': ['ad', 'di', 'is', 'se'], 'has_se': True}
    """
    return {
        "union": sorted(X | Y),
        "intersection": sorted(X & Y),
        "difference": sorted(X - Y),
        "has_se": "se" in X or "se" in Y,
    }


def p07(x: str, y: str, z: str) -> str:
    """
    >>> x = 12
    >>> y = 'temperature'
    >>> z = 22.4
    >>> p07(x, y, z)
    'temperature is 22.4 at 12'
    """
    return f"{y} is {z} at {x}"


def p08(plain: str) -> str:
    """
    >>> p08('Hello')
    'Hvool'
    >>> p08(p08('Hello'))
    'Hello'
    """

    def cipher(c: str) -> str:
        if c.islower():
            return chr(219 - ord(c))
        else:
            return c

    return "".join(cipher(c) for c in plain)


def p09(s: str) -> Generator[str, None, None]:
    """
    >>> s = 'I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind.'
    >>> res = [*p09(s)]
    >>> res[3]
    'that'
    >>> res[1][0], res[1][-1]
    ('c', 't')
    """

    def uniform_shuffle(s: str) -> str:
        chars = [*s]
        N = len(s)
        if N > 2:
            for i in range(1, N - 1):
                j = randint(1, N - 2)
                chars[i], chars[j] = chars[j], chars[i]
        return "".join(chars)

    for word in s.split():
        if len(word) > 4:
            yield uniform_shuffle(word)
        else:
            yield word
