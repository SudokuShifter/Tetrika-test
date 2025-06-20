import unittest
import inspect


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


class TestStrictDecorator(unittest.TestCase):
    def test_sum_correct(self):
        self.assertEqual(sum(1, 2), 3)
        self.assertEqual(sum(1, -2), -1)
        self.assertEqual(sum(5), 5)  # default b
        self.assertEqual(sum(a=3, b=4), 7)
        self.assertEqual(sum(b=4, a=3), 7)
        self.assertEqual(sum(a=3), 3)

    def test_sum_type_error(self):
        with self.assertRaises(TypeError):
            sum(1, 2.15)
        with self.assertRaises(TypeError):
            sum(1, '2.15')
        with self.assertRaises(TypeError):
            sum('1', 2)
        with self.assertRaises(TypeError):
            sum(a=1, b='2')
        with self.assertRaises(TypeError):
            sum(a='1', b=2)
        with self.assertRaises(TypeError):
            sum('1', '2')
        with self.assertRaises(TypeError):
            sum(a=1.5, b=2)
        with self.assertRaises(TypeError):
            sum(a=1, b=2.5)

    def test_sum_missing_argument(self):
        with self.assertRaises(TypeError):
            sum()

    def test_sum_extra_argument(self):
        with self.assertRaises(TypeError):
            sum(1, 2, 3)
        with self.assertRaises(TypeError):
            sum(a=1, b=2, c=3)

    def test_sum_kwargs(self):
        self.assertEqual(sum(**{'a': 2, 'b': 3}), 5)
        self.assertEqual(sum(**{'a': 2}), 2)
        with self.assertRaises(TypeError):
            sum(**{'a': 2, 'b': '3'})

if __name__ == "__main__":
    unittest.main()