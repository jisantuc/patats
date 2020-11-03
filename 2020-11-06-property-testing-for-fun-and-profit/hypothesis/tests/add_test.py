from hypothesis import given
from hypothesis.strategies import integers, text


@given(integers())
def test_left_identity(n: int):
    assert 0 + n == n


@given(integers())
def test_right_identity(n: int):
    assert n + 0 == n


@given(integers(), integers(), integers())
def test_associativity(a: int, b: int, c: int):
    assert (a + b) + c == a + (b + c)


@given(integers())
def test_bad_identity(n: int):
    assert n + 1 == n


@given(text())
def test_reverse_reverse(s: str):
    assert reverse(reverse(s)) == s


def reverse(s: str) -> str:
    if len(s) > 20:
        return "too many letters come on"
    else:
        return "".join(s[::-1])
