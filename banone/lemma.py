"""Module providing the Lemma class."""
import re

from typing import Dict
from typing import Optional


class VerbStemError(Exception):
    """Custom exception to catch errors related to FastText."""


class Lemma:
    """A lemma as it is found in the dictionary."""

    re_consonants = re.compile("[^aeiouäöü]*", re.I)

    def __init__(self, orth: str, lemma_dict: Dict[str, str] = {}) -> None:
        """Initialize lemma from a dictionary entry."""
        self.orth = orth
        self.pos = lemma_dict.get("pos")
        self.determiner = lemma_dict.get("determiner")
        self.color = lemma_dict.get("color")
        self.property = lemma_dict.get("property")
        self.action = lemma_dict.get("action")

    def get_stem(self) -> str:
        """Get the stem of this lemma.

        "Stem" for our purposes is the part of a word that can be used for
        pun compound creation.
        """
        orth = self.orth

        # Remove Schwa sound from the end of a noun ("Fahne" becomes "Fahn").
        if self.pos == "NN":
            if orth.endswith("e") and not orth.endswith("ie"):
                return orth[:-1]

        # Get verb stem by removing final -en or -n.
        if self.pos == "VB":
            if orth.endswith("en"):
                return orth[:-2]
            # "zappeln"
            elif orth.endswith("n"):
                return orth[:-1]
            else:
                msg = '"{}"" does not seem to be a verb (does not end in -en or -n)'
                raise VerbStemError(msg.format(orth))

        # Default: The stem is simply the full lemma.
        return orth

    def get_onset_length(self) -> int:
        """Return the length of the first syllable onset of this lemma.

        The onset of a syllable is a cluster of consonants until the first vowel.

        Examples:
        The first syllable in "Banane" is "Ba", its onset is "B".
        The onset of "Schwan" (which consists of only one syllable) "Schw".
        The first syllable in "Uhu" is "U", its onset is "".

        """
        match = self.re_consonants.match(self.orth)

        # The regex should always match but let's check to make mypy happy.
        if match is None:
            return 0

        return match.end()

    def merge(self, other: "Lemma") -> Optional[str]:
        """Merge another lemma into this one to form a compound."""
        s1 = other.get_stem().lower()
        s2 = self.orth.lower()

        # For each of the words, get the position at which the first vowel is found.
        i1 = other.get_onset_length()
        i2 = self.get_onset_length()

        # Compare words.
        while i1 < len(s1) and i2 < len(s2):
            # Get next character.
            c1, c2 = s1[i1], s2[i2]

            # Easy case: characters are the same.
            if c1 == c2:
                i1 += 1
                i2 += 1
            # Allow certain character combinations to match.
            elif (
                set([c1, c2]) == set(["d", "t"])
                or set([c1, c2]) == set(["m", "n"])
                or set([c1, c2]) == set(["r", "l"])
                or set([c1, c2]) == set(["p", "f"])
            ):
                i1 += 1
                i2 += 1
            # Dehnungs-h as in "Fahne".
            elif c1 == "h":
                i1 += 1
            elif c2 == "h":
                i2 += 1
            # Double characters such as "mm" in "fromm".
            elif c1 == s1[i1 - 1]:
                i1 += 1
            elif c2 == s2[i2 - 1]:
                i2 += 1
            # No match found.
            else:
                return None

        s = s1 + s2[i2:]
        return s.capitalize()
