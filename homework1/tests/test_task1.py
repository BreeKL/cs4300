# Python path updated in pytest.ini as described in https://pytest-with-eric.com/automation/pytest-tox-poetry/
from task1 import main
import pytest


def test_hello(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, World!"