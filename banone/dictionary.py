"""Module providing the Dictionary class."""
from collections import Counter
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

    def show_stats(self) -> None:
        """Print statistics about the words currently in the dictionary."""
        pos_counter: Counter = Counter()

        for lemma in self:
            pos_counter.update([lemma.pos])

        print("========================")
        print("Dictionary stats")
        print("------------------------")

        for pos, count in pos_counter.most_common():
            print("{}:\t{:>10}".format(pos, count))

        print("------------------------")
        print("Total:\t{:>10}".format(sum(pos_counter.values())))
        print("========================")
