"""
Simple date calculations and formatting for TimeCapture.
"""

from typing import List, Tuple, Callable, Union, Optional


def vec_op(vec1: Tuple[int, ...], vec2: Tuple[int, ...], op: Callable[[int, int], int]) -> List[int]:
    """
    Applies an element-wise operation to two vectors.

    :param vec1: First vector.
    :param vec2: Second vector.
    :param op: Operation function (e.g., sum_op, sub_op).
    :return: List of results.
    """
    return list(map(op, vec1, vec2))


DATE_VEC_NORM = (None, 12, 31, 24, 60, 60)
"""Normalization factors for date vectors (Year, Month, Day, Hour, Minute, Second)."""


def sum_op(a: int, b: int) -> int:
    """Sum operation."""
    return a + b


def sub_op(a: int, b: int) -> int:
    """Subtraction operation."""
    return a - b


def vec_std_form(vec: Tuple[int, ...], norm: Tuple[Optional[int], ...]) -> Tuple[int, ...]:
    """
    Normalizes a vector based on given normalization factors.

    :param vec: Vector to normalize.
    :param norm: Normalization factors.
    :return: Normalized vector.
    """
    def _n(x: int, m: Optional[int]) -> Tuple[int, int]:
        if m is None:
            return x, 0
        return x % m, x // m

    while True:
        res = list(map(_n, vec, norm))
        new_vec, rest = zip(*res)
        if not any(rest):
            return new_vec
        rest_shifted = rest[1:] + (0,)
        vec = tuple(vec_op(new_vec, rest_shifted, sum_op))


def vec_abs(vec: Union[List[int], Tuple[int, ...]], norm: Tuple[Optional[int], ...]) -> int:
    """
    Calculates an absolute value (e.g., total seconds) for a given vector and normalization.

    :param vec: Vector.
    :param norm: Normalization factors.
    :return: Absolute value.
    """
    x = 0
    m = 1
    for i in reversed(range(len(vec))):
        x += vec[i] * m
        if norm[i] is None:
            break
        m *= norm[i]
    return x


def vectorize(num: int, norm: Tuple[Optional[int], ...]) -> Tuple[int, ...]:
    """
    Decomposes an absolute value into a vector based on normalization factors.

    :param num: Absolute value.
    :param norm: Normalization factors.
    :return: Vector.
    """
    vec: Tuple[int, ...] = ()
    i = len(norm) - 1
    while num != 0:
        m = norm[i]
        if m is not None:
            x = num % m
            num //= m
        else:
            x = num
            num = 0
        vec = (x,) + vec
        i -= 1
        if i < 0:
            break
    return vec


def date_abs_diff(vec1: Tuple[int, ...], vec2: Tuple[int, ...]) -> int:
    """
    Calculates the absolute difference in seconds between two date vectors.

    :param vec1: First date vector.
    :param vec2: Second date vector.
    :return: Difference in seconds.
    """
    return vec_abs(vec_op(vec1, vec2, sub_op), DATE_VEC_NORM)


def date_vectorize(secs: int) -> Tuple[int, ...]:
    """
    Converts seconds into a date-like vector.

    :param secs: Seconds.
    :return: Vector.
    """
    return vectorize(secs, DATE_VEC_NORM)


def date_str(vec: Tuple[int, ...]) -> str:
    """
    Formats a time vector into a human-readable string.

    :param vec: Time vector.
    :return: Formatted string.
    """
    if len(vec) == 0:
        return "0 sec"
    if len(vec) == 1:
        return "%d sec" % vec
    if len(vec) == 2:
        return "%d:%02d min" % vec
    if len(vec) >= 3:
        return "%d:%02d:%02d" % vec[-3:]
    return str(vec)
