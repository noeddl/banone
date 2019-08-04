import pytest

from banone.lemma import Lemma
from banone.lemma import VerbStemError
from tests.utils import load_test_data


class TestLemma:
    @pytest.mark.parametrize(
        ("orth", "lemma_dict"),
        [
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
        lemma = Lemma(orth)
        if lemma_dict is not None:
            lemma = Lemma(orth, lemma_dict)

        lemma_dict = lemma_dict or {}

        assert lemma.orth == orth
        assert lemma.pos == lemma_dict.get("pos")
        assert lemma.determiner == lemma_dict.get("determiner")
        assert lemma.color == lemma_dict.get("color")
        assert lemma.property == lemma_dict.get("property")
        assert lemma.action == lemma_dict.get("action")

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
        ("orth", "length"),
        [("Schwan", 4), ("Banane", 1), ("Uhu", 0), ("Lärm", 1), ("Schmutz", 4)],
    )
    def test_get_onset_length(self, orth, length):
        lemma = Lemma(orth)
        assert lemma.get_onset_length() == length

    @pytest.mark.parametrize(
        ("str1", "str2", "compound"), load_test_data(["base", "extra", "compound"])
    )
    def test_merge(self, str1, str2, compound, fxt_dict):
        base = fxt_dict.lookup(str1)
        extra = fxt_dict.lookup(str2)

        assert base.merge(extra) == compound
