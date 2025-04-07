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
