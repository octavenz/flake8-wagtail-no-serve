import ast
import os
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


def test_has_serve_method():
    with open(os.path.join('tests', 'fixtures', 'invalid.py')) as fh:
        file_ = fh.read()
    assert _results(file_) == {
        '5:4 WNS page model should not define a custom serve method',
    }


def test_has_no_serve_method():
    with open(os.path.join('tests', 'fixtures', 'valid.py')) as fh:
        file_ = fh.read()
    assert _results(file_) == set()
