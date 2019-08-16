import pytest

from banone.lemma import Lemma
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
        ("orth", "lemma_dict", "phon_stem", "orth_stem"),
        [
            ("Haus", {"phon": "haUs", "pos": "NN"}, "haUs", "Haus"),
            ("Magie", {"phon": "ma-gi:", "pos": "NN"}, "ma-gi:", "Magie"),
            ("Fahne", {"phon": "fa:-n@", "pos": "NN"}, "fa:n", "Fahn"),
            ("Banane", {"phon": "ba-na:-n@", "pos": "NN"}, "ba-na:n", "Banan"),
            ("bauen", {"phon": "baU-@n", "pos": "VB"}, "baU", "bau"),
            ("malen", {"phon": "ma:-l@n", "pos": "VB"}, "ma:l", "mal"),
            ("anmalen", {"phon": "an-ma:-l@n", "pos": "VB"}, "an-ma:l", "anmal"),
            ("zappeln", {"phon": "tsa-p@ln", "pos": "VB"}, "tsa-p@l", "zappel"),
            ("toll", {"phon": "tOl", "pos": "ADJ"}, "tOl", "toll"),
        ],
    )
    def test_get_stem(self, orth, lemma_dict, phon_stem, orth_stem):
        lemma = Lemma(orth, lemma_dict)

        assert lemma.get_stem() == (phon_stem, orth_stem)

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
            # If two stressed vowels shall be matched they must have the same length.
            ("Tannzapfen", "Fahne"),
        ],
    )
    def test_merge_fail(self, str1, str2, fxt_dict):
        base = fxt_dict.lookup(str1)
        extra = fxt_dict.lookup(str2)

        assert base.merge(extra) is None
