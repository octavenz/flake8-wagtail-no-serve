import ast
import os
import pytest

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


@pytest.mark.parametrize(
    ('filename', 'expected'),
    (
        ('valid_page_direct', set()),
        (
            'invalid_page_direct', {
                '5:4 WNS page model should not define a custom serve method',
            },
        ),
        (
            'invalid_page_indirect', {
                '9:4 WNS page model should not define a custom serve method',
            },
        ),
    ),
)
def test_has_serve_method(filename: str, expected: Set[str]):
    with open(os.path.join('tests', 'fixtures', f'{filename}.py')) as fh:
        file_ = fh.read()
    assert _results(file_) == expected
