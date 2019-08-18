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
        is_properties: List[Optional[str]] = []

        # If a color is specified, it should be mentioned first in the question.
        color = extra.color or base.color
        if color:
            is_properties.append(color)

        # Add additional properties.
        is_properties.append(base.property)
        is_properties.append(extra.property)
        props = [prop for prop in is_properties if prop is not None]

        # Add actions.
        actions = [prop for prop in [base.action, extra.action] if prop is not None]

        all_props = props + actions
        predicates = ", ".join(all_props[:-1])

        # Add a copula verb if there are properties that are adjectives.
        if props:
            predicates = "ist {}".format(predicates)

        q = "Was {} und {}?".format(predicates, all_props[-1])

        return q

    def generate_answer(self, base: Lemma, compound: Lemma) -> Optional[str]:
        """Generate an answer containing `compound` and the determiner of `base`."""
        det = base.determiner
        if det:
            a = str.format("{} {}.", det.capitalize(), compound)
            return a
        return None

    def generate_riddle(self, base: Lemma, extra: Lemma) -> Optional[str]:
        """Generate a joke riddle using the lemmas `base` and `extra`."""
        compound = base.merge(extra)
        if compound:
            q = self.generate_question(base, extra)
            a = self.generate_answer(base, compound)
            return str.format("{}\n{}", q, a)

        return None

    def generate_all(self) -> None:
        """Generate all possible riddles based on the current dictionary."""
        riddle_counter = 0
        for extra in self.dict:
            for base in self.dict.iter_nouns():
                if base.orth == extra.orth:
                    continue
                riddle = self.generate_riddle(base, extra)
                if riddle:
                    print(riddle + "\n")
                    riddle_counter += 1

        print("{} riddles were generated.\n".format(riddle_counter))
