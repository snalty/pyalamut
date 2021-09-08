import unittest
from pyalamut.pyalamut import MutationsParser

# These tests don't work yet, sorry!

class TestMutParser(unittest.TestCase):
    def test_from_path(self):
        p = MutationsParser()
        m = p.parse_mut_file_from_path("./PKD1.mut")
        True

    def test_mut_parse_PALB2(self):
        parser = MutationsParser()
        with open("PALB2.mut") as f:
            parsed_mut = parser.parse_mut_file(f)
            True

    def test_mut_parse_PALB2(self):
        parser = MutationsParser()
        with open("PKD1.mut") as f:
            parsed_mut = parser.parse_mut_file(f)
            True
            