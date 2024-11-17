import unittest

from src.formators import JsonFormater


class TestJsonFormater(unittest.TestCase):
    def test_format_data(self):
        data = {"a": {"b": 0.5, "c": 0.3},
                "b": {"a": 0.5, "c": 0.8},
                "c": {"a": 0.3, "b": 0.8}}
        formater = JsonFormater()
        jsondata = formater.format(data)
        self.assertEqual(jsondata, '''{
    "a": {
        "b": 0.5,
        "c": 0.3
    },
    "b": {
        "a": 0.5,
        "c": 0.8
    },
    "c": {
        "a": 0.3,
        "b": 0.8
    }
}''')


