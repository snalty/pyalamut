from lxml import etree
from typing import IO
from os import PathLike

class MutParser():
    def parse_mut_file(mut_file: IO):
        xml_tree = etree.parse(mut_file)

    def parse_mut_file_from_path(self, path: PathLike):
        with open(path, 'r') as f:
            self.parse_mut_file(f.read())
