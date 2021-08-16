import unittest
from pyalamut import MutationsParser

class TestMutParser(unittest.TestCase):
    def test_mut_parse(self):
        parser = MutationsParser()
        with open("PALB2.mut") as f:
            parsed_mut = parser.parse_mut_file(f)
            True
            