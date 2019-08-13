import pytest

from banone.lemma import Lemma
from banone.lemma import Sound
from banone.lemma import VerbStemError
from tests.utils import load_test_data


class TestLemma:
    @pytest.mark.parametrize(
        ("orth", "lemma_dict"),
        [
            (None, None),
            ("", {}),
            ("Test", None),
            ("Ananas", {"pos": "NN", "determiner": "eine", "color": "gelb"}),
            (
                "Apfelsine",
                {
                    "pos": "NN",
                    "determiner": "eine",
                    "color": "orange",
                    "property": "rund",
                },
            ),
            (
                "Kaninchen",
                {
                    "pos": "NN",
                    "determiner": "ein",
                    "property": "niedlich",
                    "action": "hoppelt über die Wiese",
                },
            ),
            ("schweben", {"pos": "VB", "action": "berührt nicht den Boden"}),
        ],
    )
    def test_create(self, orth, lemma_dict):
        lemma = Lemma()

        if orth is not None:
            lemma = Lemma(orth)

        if lemma_dict is not None:
            lemma = Lemma(orth, lemma_dict)

        orth = orth or ""
        lemma_dict = lemma_dict or {}

        assert lemma.orth == orth
        assert lemma.pos == lemma_dict.get("pos")
        assert lemma.determiner == lemma_dict.get("determiner")
        assert lemma.color == lemma_dict.get("color")
        assert lemma.property == lemma_dict.get("property")
        assert lemma.action == lemma_dict.get("action")

    @pytest.mark.parametrize(
        ("phones", "index"),
        [
            (["a", "n", "a", "n", "a", "s"], 0),
            (["b", "a", "n", "a:", "n", "@"], 1),
            (["b", "l", "aU"], 2),
            (["b"], 1),
        ],
    )
    def test_set_start_index(self, phones, index):
        lemma = Lemma()
        lemma.sounds = [
            Sound(phone=s, start_char=i)
            for (s, i) in zip(phones, range(0, len(phones)))
        ]
        lemma.set_start_index()

        assert lemma.index == index

    @pytest.mark.parametrize(
        ("phones", "index", "sound"),
        [
            (["a", "n", "a", "n", "a", "s"], 0, "a"),
            (["b", "a", "n", "a:", "n", "@"], 3, "a:"),
            (["b", "l", "aU"], 2, "aU"),
        ],
    )
    def test_next(self, phones, index, sound):
        lemma = Lemma()
        lemma.sounds = [
            Sound(phone=s, start_char=i)
            for (s, i) in zip(phones, range(0, len(phones)))
        ]
        lemma.index = index

        assert next(lemma) == sound

    @pytest.mark.parametrize(("phones", "index"), [(["a", "n", "a", "n", "a", "s"], 6)])
    def test_next_at_end_of_list(self, phones, index):
        lemma = Lemma()
        lemma.sounds = [
            Sound(phone=s, start_char=i)
            for (s, i) in zip(phones, range(0, len(phones)))
        ]
        lemma.index = index

        with pytest.raises(StopIteration):
            next(lemma)

    @pytest.mark.parametrize(
        ("orth", "phon", "phones", "phones2graphs"),
        [
            ("Pfahl", "pfa:l", ["pf", "a:", "l"], [0, 2, 4]),
            ("Zahl", "tsa:l", ["ts", "a:", "l"], [0, 1, 3]),
            ("deutsch", "dOYtS", ["d", "OY", "tS"], [0, 1, 3]),
            ("Dschungel", "dZUN@l", ["dZ", "U", "N", "@", "l"], [0, 4, 5, 7, 8]),
            ("Pein", "paIn", ["p", "aI", "n"], [0, 1, 3]),
            ("Bein", "baIn", ["b", "aI", "n"], [0, 1, 3]),
            ("Teich", "taIC", ["t", "aI", "C"], [0, 1, 3]),
            ("Deich", "daIC", ["d", "aI", "C"], [0, 1, 3]),
            ("Kunst", "kUnst", ["k", "U", "n", "s", "t"], [0, 1, 2, 3, 4]),
            ("Gunst", "gUnst", ["g", "U", "n", "s", "t"], [0, 1, 2, 3, 4]),
            ("fast", "fast", ["f", "a", "s", "t"], [0, 1, 2, 3]),
            ("was", "vas", ["v", "a", "s"], [0, 1, 2]),
            ("Tasse", "tas@", ["t", "a", "s", "@"], [0, 1, 2, 4]),
            ("Hase", "ha:z@", ["h", "a:", "z", "@"], [0, 1, 2, 3]),
            ("waschen", "vaS@n", ["v", "a", "S", "@", "n"], [0, 1, 2, 5, 6]),
            ("Genie", "Zeni:", ["Z", "e", "n", "i:"], [0, 1, 2, 3]),
            ("sicher", "zIC6", ["z", "I", "C", "6"], [0, 1, 2, 4]),
            ("Jahr", "ja:6", ["j", "a:", "6"], [0, 1, 3]),
            ("Buch", "bu:x", ["b", "u:", "x"], [0, 1, 2]),
            ("Hand", "hant", ["h", "a", "n", "t"], [0, 1, 2, 3]),
            ("mein", "maIn", ["m", "aI", "n"], [0, 1, 3]),
            ("nein", "naIn", ["n", "aI", "n"], [0, 1, 3]),
            ("Ding", "dIN", ["d", "I", "N"], [0, 1, 2]),
            ("Leim", "laIm", ["l", "aI", "m"], [0, 1, 3]),
            ("Reim", "RaIm", ["R", "aI", "m"], [0, 1, 3]),
            ("Eis", "aIs", ["aI", "s"], [0, 2]),
            ("Haus", "haUs", ["h", "aU", "s"], [0, 1, 3]),
            ("Kreuz", "kROYts", ["k", "R", "OY", "ts"], [0, 1, 2, 4]),
            ("Lied", "li:t", ["l", "i:", "t"], [0, 1, 3]),
            ("Beet", "be:t", ["b", "e:", "t"], [0, 1, 3]),
            ("spät", "SpE:t", ["S", "p", "E:", "t"], [0, 1, 2, 3]),
            ("Tat", "ta:t", ["t", "a:", "t"], [0, 1, 2]),
            ("rot", "Ro:t", ["R", "o:", "t"], [0, 1, 2]),
            ("Blut", "blu:t", ["b", "l", "u:", "t"], [0, 1, 2, 3]),
            ("süß", "zy:s", ["z", "y:", "s"], [0, 1, 2]),
            ("blöd", "bl2:t", ["b", "l", "2:", "t"], [0, 1, 2, 3]),
            ("Sitz", "zIts", ["z", "I", "ts"], [0, 1, 2]),
            ("Gesetz", "g@zEts", ["g", "@", "z", "E", "ts"], [0, 1, 2, 3, 4]),
            ("Satz", "zats", ["z", "a", "ts"], [0, 1, 2]),
            ("Trotz", "tROts", ["t", "R", "O", "ts"], [0, 1, 2, 3]),
            ("Schutz", "SUts", ["S", "U", "ts"], [0, 3, 4]),
            ("hübsch", "hYpS", ["h", "Y", "p", "S"], [0, 1, 2, 3]),
            (
                "plötzlich",
                "pl9tslIC",
                ["p", "l", "9", "ts", "l", "I", "C"],
                [0, 1, 2, 3, 5, 6, 7],
            ),
            ("bitte", "bIt@", ["b", "I", "t", "@"], [0, 1, 2, 4]),
            ("bitter", "bIt6", ["b", "I", "t", "6"], [0, 1, 2, 4]),
        ],
    )
    def test_map_sounds_to_characters(self, orth, phon, phones, phones2graphs):
        lemma = Lemma(orth, {"phon": phon})
        # map_sounds_to_characters is called on initialization.

        sounds = [Sound(phone=s, start_char=i) for (s, i) in zip(phones, phones2graphs)]

        assert lemma.sounds == sounds

    @pytest.mark.parametrize(
        ("orth", "lemma_dict", "stem"),
        [
            ("Haus", {"pos": "NN"}, "Haus"),
            ("Fahne", {"pos": "NN"}, "Fahn"),
            ("Magie", {"pos": "NN"}, "Magie"),
            ("bauen", {"pos": "VB"}, "bau"),
            ("zappeln", {"pos": "VB"}, "zappel"),
            ("toll", {"pos": "ADJ"}, "toll"),
        ],
    )
    def test_get_stem(self, orth, lemma_dict, stem):
        lemma = Lemma(orth, lemma_dict)

        assert lemma.get_stem() == stem

    @pytest.mark.parametrize(("orth", "lemma_dict"), [("keinverb", {"pos": "VB"})])
    def test_get_verb_stem_with_error(self, orth, lemma_dict):
        lemma = Lemma(orth, lemma_dict)

        with pytest.raises(VerbStemError):
            lemma.get_stem()

    @pytest.mark.parametrize(
        ("str1", "str2", "compound"), load_test_data(["base", "extra", "compound"])
    )
    def test_merge(self, str1, str2, compound, fxt_dict):
        base = fxt_dict.lookup(str1)
        extra = fxt_dict.lookup(str2)

        assert base.merge(extra) == compound

    @pytest.mark.parametrize(
        ("str1", "str2"),
        [
            # The base word needs a minimum number of syllables to enable matching
            # of sounds with a distance > 1 (e.g. n/m).
            ("Kamin", "Fahne"),
            ("Kamin", "Schwan"),
            ("Kamin", "spannen"),
            # The base word should be longer than one syllable not counting an
            # unstressed end syllable.
            ("Fahne", "Schwan"),
            ("Fahne", "spannen"),
            # The base word should not have less syllables than the extra word.
            ("Pudel", "Nudelauflauf"),
        ],
    )
    def test_merge_fail(self, str1, str2, fxt_dict):
        base = fxt_dict.lookup(str1)
        extra = fxt_dict.lookup(str2)

        assert base.merge(extra) is None
