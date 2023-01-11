import ast
import sys
from typing import Generator, Tuple, Type, Any, List

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

MESSAGE = 'WNS page model should not define a custom serve method'


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.problems: List[Tuple[int, int]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        # TODO: also check class inherits from wagtail's Page model
        for child in node.body:
            if isinstance(child, ast.FunctionDef) and child.name == 'serve':
                self.problems.append((child.lineno, child.col_offset))
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col in visitor.problems:
            yield line, col, MESSAGE, type(self)
