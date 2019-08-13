"""Module providing the Dictionary class."""
from pathlib import Path

import yaml
from typing import Dict
from typing import Iterator
from typing import Optional

from banone.lemma import Lemma


class Dictionary:
    """Dictionary of words to be used in joke riddles."""

    def __init__(self, path: Path) -> None:
        """Load Dictionary from a YAML file."""
        self.entries: Dict[str, Lemma] = {}
        with path.open(encoding="utf-8") as file:
            for orth, lemma_dict in yaml.safe_load(file).items():
                self.entries[orth] = Lemma(orth, lemma_dict)

    def __iter__(self) -> Iterator[Lemma]:
        """Iterate over dictionary entries."""
        for lemma in self.entries.values():
            yield lemma

    def lookup(self, s: str) -> Optional[Lemma]:
        """Look up a word in the dictionary."""
        return self.entries.get(s)

    def iter_nouns(self) -> Iterator[Lemma]:
        """Iterate over the nouns in the dictionary."""
        return (lemma for lemma in self if lemma.pos == "NN")
