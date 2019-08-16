"""Module providing the Lemma class."""
from typing import Dict
from typing import Optional
from typing import Tuple

from banone.sound import SoundSequence


class VerbStemError(Exception):
    """Custom exception to catch errors related to FastText."""


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

    def __init__(self, orth: str = "", lemma_dict: Dict[str, str] = {}) -> None:
        """Initialize lemma from a dictionary entry."""
        self.orth = orth
        self.phon = lemma_dict.get("phon") or orth.lower()
        self.pos = lemma_dict.get("pos")
        self.determiner = lemma_dict.get("determiner")
        self.color = lemma_dict.get("color")
        self.property = lemma_dict.get("property")
        self.action = lemma_dict.get("action")

    def get_stem(self) -> Tuple[str, str]:
        """Get the stem of this lemma.

        "Stem" for our purposes is the part of a word that can be used for
        pun compound creation.
        """
        phon, orth = self.phon, self.orth

        # Remove Schwa sound from the end of a noun ("Fahne" becomes "Fahn").
        if self.pos == "NN":
            if phon.endswith("@"):
                return remove_last_syllable(phon[:-1]), orth[:-1]

        # Get verb stem by removing final -en or -n.
        if self.pos == "VB":
            if phon.endswith("@n"):
                return remove_last_syllable(phon[:-2]), orth[:-2]
            # "zappeln"
            elif phon.endswith("n"):
                return phon[:-1], orth[:-1]
            else:
                msg = '"{}"" does not seem to be a verb (does not end in -en or -n)'
                raise VerbStemError(msg.format(phon))

        # Default: The stem is simply the full lemma.
        return phon, orth

    def merge(self, other: "Lemma") -> Optional[str]:
        """Merge another lemma into this one to form a compound."""
        sound_seq_base = SoundSequence(self.orth, self.phon)

        phon, orth = other.get_stem()
        sound_seq_extra = SoundSequence(orth, phon)

        return sound_seq_base.merge(sound_seq_extra)
