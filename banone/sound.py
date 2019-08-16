"""Module providing classes to handle the phonetic representations of words."""
import re

from typing import Iterator
from typing import List
from typing import NamedTuple
from typing import Optional

re_vowels = re.compile("^[aeiouy29@6]", re.I)
re_full_vowels = re.compile("^[aeiouy29]", re.I)


class Sound(NamedTuple):
    """A sound that is part of a word."""

    phone: str
    start_char: int
    syllable: int
    stressed: bool

    def __str__(self) -> str:
        """Return the string representation of the sound."""
        return self.phone

    def is_vowel(self) -> bool:
        """Return `True` if the sound is a vowel including schwa and vocalic r."""
        if re_vowels.match(self.phone):
            return True
        return False

    def is_full_vowel(self) -> bool:
        """Return `True` if the sound is a full vowel."""
        if re_full_vowels.match(self.phone):
            return True
        return False

    def get_distance(self, other: "Sound") -> int:
        """Return a numerical distance between this sound and another."""
        p1, p2 = self.phone, other.phone

        if p1 == p2:
            return 0

        # Match long and short vowels such as "a" and "a:" but only if the short vowel
        # is not stressed.
        if (p1 == p2 + ":" and not other.stressed) or (
            p2 == p1 + ":" and not self.stressed
        ):
            return 1

        if (
            set([p1, p2]) == set(["m", "n"])
            or set([p1, p2]) == set(["l", "R"])
            or set([p1, p2]) == set(["pf", "p"])
        ):
            return 2

        return 100


class SoundSequence:
    """A sequence of sounds that form a word."""

    re_sounds = re.compile(
        """
          pf|t[sS]|dZ       # affricates
        | [pbtdkg]          # plosives
        | [fvszSZCjxh]      # fricatives
        | [mnNlR]           # sonorants
        | a[IU]|OY          # diphthongs
        | [ieEaouy2][:]?    # vowels that can be lengthened (when stressed)
        | [IOUY9]           # vowels that are always short
        | [@6]              # schwa and vocalic r
        | [-']              # syllable boundary and stress - not actually sounds
    """,
        re.VERBOSE,
    )

    phone_graph_map = {
        "pf": ["pf"],
        "ts": ["tz", "z"],
        "tS": ["tsch"],
        "dZ": ["dsch", "j"],
        "p": ["pp", "p", "b"],
        "b": ["bb", "b"],
        "t": ["tt", "dt", "t", "d"],
        "d": ["dd", "d"],
        "k": ["ck", "kk", "k", "g"],
        "g": ["gg", "g"],
        "f": ["f", "v"],
        "v": ["v", "w"],
        "s": ["ss", "ß", "s"],
        "z": ["s"],
        "S": ["sch", "s"],
        "Z": ["g"],
        "C": ["ch"],
        "j": ["j", "i"],
        "x": ["ch"],
        "h": ["h"],
        "m": ["mm", "m"],
        "n": ["nn", "n"],
        "N": ["ng", "n"],
        "l": ["ll", "l"],
        "R": ["rr", "r"],
        "aI": ["ai", "ei"],
        "aU": ["au"],
        "OY": ["äu", "eu", "oi"],
        "i:": ["ieh", "ie", "i"],
        "e:": ["eh", "ee", "e"],
        "E:": ["äh", "ä"],
        "a:": ["ah", "aa", "a"],
        "o:": ["oh", "oo", "o"],
        "u:": ["uh", "u"],
        "y:": ["üh", "ü"],
        "2:": ["öh", "ö"],
        "I": ["i"],
        "E": ["e", "ä"],
        "a": ["a"],
        "O": ["o"],
        "U": ["u"],
        "Y": ["ü"],
        "9": ["ö"],
        "@": ["e"],
        "6": ["er", "r"],
    }

    def __init__(self, orth: str, phon: str) -> None:
        """Initialize the sound sequence."""
        self.orth = orth
        self.phon = phon
        self.sounds = self._parse()
        self.index = 0

    def __len__(self) -> int:
        """Return number of sounds in this sequence."""
        return len(self.sounds)

    def __iter__(self) -> Iterator:
        """Return iterator."""
        return self

    def __next__(self) -> Sound:
        """Return next sound of this sequence."""
        if self.index < len(self):
            sound = self.sounds[self.index]
            self.index += 1
            return sound
        raise StopIteration

    def _parse(self) -> List[Sound]:
        """Create of mapping of sounds to characters."""
        w = self.phon
        v = self.orth.lower()
        index = 0

        syllable = 1
        stressed = False
        sounds = []

        for m in self.re_sounds.finditer(w):
            s = m.group()

            # Keep track of stress.
            if s == "'":
                stressed = True
                continue

            # Keep track of syllable boundaries.
            if s == "-":
                syllable += 1
                continue

            sound = Sound(phone=s, start_char=index, syllable=syllable, stressed=False)

            # Add stress to the first full vowel in the syllable.
            if sound.is_full_vowel() and stressed:
                sound = sound._replace(stressed=True)
                stressed = False

            for graph in self.phone_graph_map.get(s, [s]):
                if v.startswith(graph):
                    sounds.append(sound)
                    step = len(graph)
                    v = v[step:]
                    index += step

        return sounds

    def set_start_index(self) -> None:
        """Set the index of the iterator to the first full vowel of the word.

        This is the same as ignoring the onset of the first syllable. The onset
        of a syllable is a cluster of consonants until the first vowel.

        Examples:
        The first syllable in "Banane" is "Ba", its onset is "B".
        The onset of "Schwan" (which consists of only one syllable) "Schw".
        The first syllable in "Uhu" is "U", its onset is "".

        """
        for i, sound in enumerate(self.sounds):
            if sound.is_full_vowel():
                self.index = i
                return

        # If the word only consists of consonants (which is very unlikely)
        # jump directly to the end.
        self.index = len(self)

    def count_syllables(self) -> int:
        """Return the number of syllables of the sound sequence."""
        last_sound = self.sounds[-1]
        return last_sound.syllable

    def ends_with_schwa(self) -> bool:
        """Return `True` if the last sound in the sequence is a schwa."""
        last_sound = self.sounds[-1]
        return last_sound.phone == "@"

    def merge(self, other: "SoundSequence") -> Optional[str]:
        """Merge another lemma into this one to form a compound."""
        # The base word must have more than one syllable not counting an unstressed
        # end syllable.
        if self.count_syllables() < 2:
            return None

        # Short words ending in a schwa such as "Fahne" are no good bases.
        if self.count_syllables() == 2 and self.ends_with_schwa():
            return None

        # The extra word may not be longer than the base word.
        if other.count_syllables() > self.count_syllables():
            return None

        # For each of the words, get the position at which the first vowel is found.
        self.set_start_index()
        other.set_start_index()

        # Compare words.
        for snd1 in self:
            # Get next sound.
            snd2 = next(other)

            dist = snd1.get_distance(snd2)

            match = dist <= 1 or (dist == 2 and self.count_syllables() > 2)

            if not match:
                return None

            if other.index == len(other):
                break

        sound = self.sounds[self.index]
        index = sound.start_char
        s = other.orth + self.orth[index:]

        return s.capitalize()
