import inspect
import pytest


def strict(func):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        for name, value in bound_args.arguments.items():
            expected_type = func.__annotations__.get(name)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(f'{name} must be {expected_type}')
        return func(*args, **kwargs)
    return wrapper


@strict
def sum(a: int, b: int = 0):
    return a + b


def test_sum_correct():
    assert sum(1, 2) == 3
    assert sum(1, -2) == -1
    assert sum(5) == 5  # default b
    assert sum(a=3, b=4) == 7
    assert sum(b=4, a=3) == 7
    assert sum(a=3) == 3

def test_sum_type_error():
    with pytest.raises(TypeError):
        sum(1, 2.15)
    with pytest.raises(TypeError):
        sum(1, '2.15')
    with pytest.raises(TypeError):
        sum('1', 2)
    with pytest.raises(TypeError):
        sum(a=1, b='2')
    with pytest.raises(TypeError):
        sum(a='1', b=2)
    with pytest.raises(TypeError):
        sum('1', '2')
    with pytest.raises(TypeError):
        sum(a=1.5, b=2)
    with pytest.raises(TypeError):
        sum(a=1, b=2.5)

def test_sum_missing_argument():
    with pytest.raises(TypeError):
        sum()

def test_sum_extra_argument():
    with pytest.raises(TypeError):
        sum(1, 2, 3)
    with pytest.raises(TypeError):
        sum(a=1, b=2, c=3)

def test_sum_kwargs():
    assert sum(**{'a': 2, 'b': 3}) == 5
    assert sum(**{'a': 2}) == 2
    with pytest.raises(TypeError):
        sum(**{'a': 2, 'b': '3'})