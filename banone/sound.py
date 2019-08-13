"""Module providing the Sound class."""
import re
from collections import namedtuple


class Sound(namedtuple("Sound", "phone start_char")):
    """A sound that is part of a word."""

    __slots__ = ()

    re_full_vowels = re.compile("^[aeiouy29]+", re.I)

    def is_full_vowel(self) -> bool:
        """Return `True` if the sound is a full vowel."""
        if self.re_full_vowels.match(self.phone):
            return True
        return False
