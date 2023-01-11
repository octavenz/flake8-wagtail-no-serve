import ast
from typing import Set

from flake8_wagtail_no_serve import Plugin


def _results(s: str) -> Set[str]:
    """Helper function for running plugin in tests"""
    tree = ast.parse(s)
    plugin = Plugin(tree)
    return {
        f'{line}:{col} {message}'
        for line, col, message, _ in plugin.run()
    }


def test_trivial_case():
    assert _results('') == set()
