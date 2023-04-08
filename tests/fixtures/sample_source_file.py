"""A file for testing prompt creation."""


def fib(n):
    """Returns the nth fibonacci number."""
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


def fact(n):
    """Returns n factorial."""
    if n <= 1:
        return 1
    return n * fact(n - 1)


def hailstone(n):
    """Returns the hailstone sequence starting with positive integer n."""
    if n <= 0:
        raise ValueError(f"Cannot compute hailstone of negative number {n}")
    if n == 1:
        return [n]
    if n % 2 == 0:
        return [n] + hailstone(n // 2)
    return [n] + hailstone(3 * n + 1)
