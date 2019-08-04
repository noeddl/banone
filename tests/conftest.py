from pathlib import Path

import pytest

from banone.dictionary import Dictionary


@pytest.fixture(scope="session")
def fxt_dict():
    return Dictionary(Path("banone/dict/de.yaml"))
