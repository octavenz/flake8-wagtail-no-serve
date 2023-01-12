import ast
import re
import sys

from dataclasses import dataclass
from typing import Generator, Tuple, Type, Any, List

if sys.version_info < (3, 8):
    import importlib_metadata  # pragma: <3.8 cover
else:
    import importlib.metadata as importlib_metadata  # pragma: >=3.8 cover

MESSAGE = 'WNS page model should not define a custom serve method'
BASES = '[A-Za-z]*Page'


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.problems: List[Tuple[int, int]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        has_page_base = len([base.id for base in node.bases if re.match(BASES, base.id)]) > 0
        if node.bases and has_page_base:
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == 'serve':
                    self.problems.append((child.lineno, child.col_offset))
        self.generic_visit(node)


@dataclass(frozen=True)
class Plugin:
    tree: ast.AST
    name: str = __name__
    version: str = importlib_metadata.version(__name__)

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self.tree)
        for line, col in visitor.problems:
            yield line, col, MESSAGE, type(self)
