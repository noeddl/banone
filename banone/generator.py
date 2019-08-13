"""Module providing the Generator class."""
from pathlib import Path

from typing import List
from typing import Optional

from banone.dictionary import Dictionary
from banone.lemma import Lemma


class Generator:
    """Joke riddle generator."""

    def __init__(self, dict_path: Path):
        """Initialize generator."""
        self.dict = Dictionary(dict_path)

    def generate_question(self, base: Lemma, extra: Lemma) -> str:
        """Generate the question for asking for the result of merging two lemmas."""
        properties: List[Optional[str]] = []

        # If a color is specified, it should be mentioned first in the question.
        color = extra.color or base.color
        if color:
            properties.append(color)

        # Add additional properties.
        properties.append(base.property)
        properties.append(extra.property)
        properties.append(base.action)
        properties.append(extra.action)

        props = [prop for prop in properties if prop is not None]

        predicates = ", ".join(props[:-1])

        q = "Was ist {} und {}?".format(predicates, props[-1])

        return q

    def generate_answer(self, base: str, compound: str) -> Optional[str]:
        """Generate an answer containing `compound` and the determiner of `base`."""
        e = self.dict.lookup(base)
        if e:
            det = e.determiner
            if det:
                a = str.format("{} {}.", det.capitalize(), compound)
                return a
        return None

    def generate_riddle(self, base: Lemma, extra: Lemma) -> Optional[str]:
        """Generate a riddle with a question and an answer based on `s1` and `s2`."""
        compound = base.merge(extra)
        if compound:
            q = self.generate_question(base, extra)
            a = self.generate_answer(base.orth, compound)
            return str.format("{}\n{}", q, a)

        return None

    def generate_all(self) -> None:
        """Generate all possible riddles based on the current dictionary.

        This is mainly meant to be used for debugging.
        """
        for extra in self.dict:
            for base in self.dict.iter_nouns():
                if base.orth == extra.orth:
                    continue
                riddle = self.generate_riddle(base, extra)
                if riddle:
                    print(riddle + "\n")
