"""Module providing the Lemma class."""
from typing import Dict
from typing import Optional
from typing import Tuple

from banone.sound import SoundSequence


def remove_last_syllable(phon: str) -> str:
    """Remove the last syllable boundary in a phonetic string.

    Example: Turn `fa:-n` (stem of `fa:-n@`) into `fa:n`.
    """
    # Find the last hyphen marking a syllable boundary and remove it.
    i = phon.rfind("-")
    j = i + 1
    return phon[:i] + phon[j:]


class Lemma:
    """A lemma as it is found in the dictionary."""

    def __init__(self, orth: str, lemma_dict: Dict[str, str] = {}) -> None:
        """Initialize lemma from a dictionary entry."""
        self.orth = orth
        self.phon = lemma_dict.get("phon") or orth.lower()
        self.pos = lemma_dict.get("pos")
        self.determiner = lemma_dict.get("determiner")
        self.color = lemma_dict.get("color")
        self.property = lemma_dict.get("property")
        self.action = lemma_dict.get("action")

    def __str__(self) -> str:
        """Return the string representation of the lemma."""
        return self.orth

    def get_stem(self) -> Tuple[str, str]:
        """Get the stem of the lemma.

        "Stem" for our purposes is the part of a word that can be used for
        pun compound creation.
        """
        phon, orth = self.phon, self.orth

        # Remove schwa sound from the end of a noun ("Fahne" becomes "Fahn").
        if self.pos == "NN":
            if phon.endswith("@"):
                return remove_last_syllable(phon[:-1]), orth[:-1]

        # Get verb stem by removing final -en or -n.
        if self.pos == "VB":
            if phon.endswith("@n"):
                return remove_last_syllable(phon[:-2]), orth[:-2]
            # "zappeln"
            if phon.endswith("n"):
                return phon[:-1], orth[:-1]

        # Default: The stem is simply the full lemma.
        return phon, orth

    def merge(self, other: "Lemma") -> Optional["Lemma"]:
        """Merge another lemma into this one to form a compound."""
        sound_seq_base = SoundSequence(self.orth, self.phon)

        phon, orth = other.get_stem()
        sound_seq_extra = SoundSequence(orth, phon)

        compound_orth = sound_seq_base.merge(sound_seq_extra)

        if compound_orth:
            return Lemma(compound_orth)

        return None
