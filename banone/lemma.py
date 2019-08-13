"""Module providing the Lemma class."""
import re

from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional

from banone.sound import Sound


class VerbStemError(Exception):
    """Custom exception to catch errors related to FastText."""


class Lemma:
    """A lemma as it is found in the dictionary."""

    re_consonants = re.compile("[^aeiouäöü]*", re.I)
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
    """,
        re.VERBOSE,
    )
    sound_char_map = {
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

    def __init__(self, orth: str = "", lemma_dict: Dict[str, str] = {}) -> None:
        """Initialize lemma from a dictionary entry."""
        self.orth = orth
        self.phon = lemma_dict.get("phon") or orth.lower()
        self.pos = lemma_dict.get("pos")
        self.determiner = lemma_dict.get("determiner")
        self.color = lemma_dict.get("color")
        self.property = lemma_dict.get("property")
        self.action = lemma_dict.get("action")
        self.index = 0
        self.ignore_unstressed_end = False
        self.sounds: List[Sound] = self.map_sounds_to_characters()
        self.syllables = self.phon.split("-")

    def __len__(self) -> int:
        """Return number of sounds of this lemma."""
        length = len(self.sounds)

        if self.ignore_unstressed_end:
            if self.pos == "NN" and self.sounds[-1].phone == "@":
                return length - 1

            if self.pos == "VB":
                if self.sounds[-1].phone == "n":
                    if self.sounds[-2].phone == "@":
                        return length - 2
                    return length - 1

        return length

    def __str__(self) -> str:
        """Return orthographic representation of this lemma."""
        if len(self) < len(self.sounds):
            last_sound = self.sounds[len(self)]
            index = last_sound.start_char
            return self.orth[:index]
        return self.orth

    def __iter__(self) -> Iterator:
        """Return iterator."""
        return self

    def __next__(self) -> str:
        """Return next sound of this lemma."""
        if self.index < len(self):
            sound = self.sounds[self.index]
            self.index += 1
            return sound.phone
        raise StopIteration

    def map_sounds_to_characters(self) -> List[Sound]:
        """Create of mapping of sounds to characters."""
        w = self.phon
        v = self.orth.lower()
        index = 0

        sounds = []

        for m in self.re_sounds.finditer(w):
            s = m.group()
            sound = Sound(phone=s, start_char=index)
            for graph in self.sound_char_map.get(s, [s]):
                if v.startswith(graph):
                    sounds.append(sound)
                    step = len(graph)
                    v = v[step:]
                    index += step

        return sounds

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
        self.index = len(self.sounds)

    def get_distance(self, snd1: str, snd2: str) -> int:
        """Return `True` if `snd1` and `snd2` represent two matching sounds."""
        if snd1 == snd2:
            return 0

        if set([snd1, snd2]) == set(["a:", "a"]) or set([snd1, snd2]) == set(
            ["o:", "o"]
        ):
            return 1

        if (
            set([snd1, snd2]) == set(["m", "n"])
            or set([snd1, snd2]) == set(["l", "R"])
            or set([snd1, snd2]) == set(["pf", "p"])
        ):
            return 2

        return 100

    def get_syllable_count(self) -> int:
        """Return the number of syllables of the lemma."""
        # Ignore unstressed end syllable.
        if len(self) < len(self.sounds):
            return len(self.syllables) - 1
        return len(self.syllables)

    def merge(self, other: "Lemma") -> Optional[str]:
        """Merge another lemma into this one to form a compound."""
        # The base word must have more than one syllable not counting an unstressed
        # end syllable.
        if self.get_syllable_count() < 2:
            return None

        # Both words need to have at least the same number of syllables.
        if other.get_syllable_count() > self.get_syllable_count():
            return None

        # For each of the words, get the position at which the first vowel is found.
        self.set_start_index()
        other.set_start_index()

        self.ignore_unstressed_end = False
        other.ignore_unstressed_end = True

        # Compare words.
        for snd1 in self:
            # Get next sound.
            snd2 = next(other)

            dist = self.get_distance(snd1, snd2)

            match = dist <= 1 or (dist == 2 and len(self.syllables) > 2)

            if not match:
                return None

            if other.index == len(other):
                break

        sound = self.sounds[self.index]
        index = sound.start_char
        s = str(other) + self.orth[index:]

        return s.capitalize()
