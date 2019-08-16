import pytest

from banone.sound import Sound
from banone.sound import SoundSequence


class TestSound:
    @pytest.mark.parametrize(
        ("sound", "is_vowel", "is_full_vowel"),
        [
            ("a", True, True),
            ("a:", True, True),
            ("U", True, True),
            ("aU", True, True),
            ("@", True, False),
            ("6", True, False),
            ("b", False, False),
            ("g", False, False),
        ],
    )
    def test_check_vowels(self, sound, is_vowel, is_full_vowel):
        sound = Sound(sound, 0, 1, False)

        assert sound.is_vowel() == is_vowel
        assert sound.is_full_vowel() == is_full_vowel


class TestSoundSequence:
    @pytest.mark.parametrize(
        ("orth", "phon", "phones", "phones2graphs", "syllables", "stress_index"),
        [
            ("Pfahl", "'pfa:l", ["pf", "a:", "l"], [0, 2, 4], [1, 1, 1], 1),
            ("Zahl", "'tsa:l", ["ts", "a:", "l"], [0, 1, 3], [1, 1, 1], 1),
            ("deutsch", "'dOYtS", ["d", "OY", "tS"], [0, 1, 3], [1, 1, 1], 1),
            (
                "Dschungel",
                "'dZU-N@l",
                ["dZ", "U", "N", "@", "l"],
                [0, 4, 5, 7, 8],
                [1, 1, 2, 2, 2],
                1,
            ),
            ("Pein", "'paIn", ["p", "aI", "n"], [0, 1, 3], [1, 1, 1], 1),
            ("Bein", "'baIn", ["b", "aI", "n"], [0, 1, 3], [1, 1, 1], 1),
            ("Teich", "'taIC", ["t", "aI", "C"], [0, 1, 3], [1, 1, 1], 1),
            ("Deich", "'daIC", ["d", "aI", "C"], [0, 1, 3], [1, 1, 1], 1),
            (
                "Kunst",
                "'kUnst",
                ["k", "U", "n", "s", "t"],
                [0, 1, 2, 3, 4],
                [1, 1, 1, 1, 1],
                1,
            ),
            (
                "Gunst",
                "'gUnst",
                ["g", "U", "n", "s", "t"],
                [0, 1, 2, 3, 4],
                [1, 1, 1, 1, 1],
                1,
            ),
            ("fast", "'fast", ["f", "a", "s", "t"], [0, 1, 2, 3], [1, 1, 1, 1], 1),
            ("was", "'vas", ["v", "a", "s"], [0, 1, 2], [1, 1, 1], 1),
            ("Tasse", "'ta-s@", ["t", "a", "s", "@"], [0, 1, 2, 4], [1, 1, 2, 2], 1),
            ("Hase", "'ha:-z@", ["h", "a:", "z", "@"], [0, 1, 2, 3], [1, 1, 2, 2], 1),
            (
                "waschen",
                "'va-S@n",
                ["v", "a", "S", "@", "n"],
                [0, 1, 2, 5, 6],
                [1, 1, 2, 2, 2],
                1,
            ),
            ("Genie", "Ze-'ni:", ["Z", "e", "n", "i:"], [0, 1, 2, 3], [1, 1, 2, 2], 3),
            ("sicher", "'zI-C6", ["z", "I", "C", "6"], [0, 1, 2, 4], [1, 1, 2, 2], 1),
            ("Jahr", "'ja:6", ["j", "a:", "6"], [0, 1, 3], [1, 1, 1], 1),
            ("Buch", "'bu:x", ["b", "u:", "x"], [0, 1, 2], [1, 1, 1], 1),
            ("Hand", "'hant", ["h", "a", "n", "t"], [0, 1, 2, 3], [1, 1, 1, 1], 1),
            ("mein", "'maIn", ["m", "aI", "n"], [0, 1, 3], [1, 1, 1], 1),
            ("nein", "'naIn", ["n", "aI", "n"], [0, 1, 3], [1, 1, 1], 1),
            ("Ding", "'dIN", ["d", "I", "N"], [0, 1, 2], [1, 1, 1], 1),
            ("Leim", "'laIm", ["l", "aI", "m"], [0, 1, 3], [1, 1, 1], 1),
            ("Reim", "'RaIm", ["R", "aI", "m"], [0, 1, 3], [1, 1, 1], 1),
            ("Eis", "'aIs", ["aI", "s"], [0, 2], [1, 1], 0),
            ("Haus", "'haUs", ["h", "aU", "s"], [0, 1, 3], [1, 1, 1], 1),
            ("Kreuz", "'kROYts", ["k", "R", "OY", "ts"], [0, 1, 2, 4], [1, 1, 1, 1], 2),
            ("Lied", "'li:t", ["l", "i:", "t"], [0, 1, 3], [1, 1, 1], 1),
            ("Beet", "'be:t", ["b", "e:", "t"], [0, 1, 3], [1, 1, 1], 1),
            ("spät", "'SpE:t", ["S", "p", "E:", "t"], [0, 1, 2, 3], [1, 1, 1, 1], 2),
            ("Tat", "'ta:t", ["t", "a:", "t"], [0, 1, 2], [1, 1, 1], 1),
            ("rot", "'Ro:t", ["R", "o:", "t"], [0, 1, 2], [1, 1, 1], 1),
            ("Blut", "'blu:t", ["b", "l", "u:", "t"], [0, 1, 2, 3], [1, 1, 1, 1], 2),
            ("süß", "'zy:s", ["z", "y:", "s"], [0, 1, 2], [1, 1, 1], 1),
            ("blöd", "'bl2:t", ["b", "l", "2:", "t"], [0, 1, 2, 3], [1, 1, 1, 1], 2),
            ("Sitz", "'zIts", ["z", "I", "ts"], [0, 1, 2], [1, 1, 1], 1),
            (
                "Gesetz",
                "g@-'zEts",
                ["g", "@", "z", "E", "ts"],
                [0, 1, 2, 3, 4],
                [1, 1, 2, 2, 2],
                3,
            ),
            ("Satz", "'zats", ["z", "a", "ts"], [0, 1, 2], [1, 1, 1], 1),
            ("Trotz", "'tROts", ["t", "R", "O", "ts"], [0, 1, 2, 3], [1, 1, 1, 1], 2),
            ("Schutz", "'SUts", ["S", "U", "ts"], [0, 3, 4], [1, 1, 1], 1),
            ("hübsch", "'hYpS", ["h", "Y", "p", "S"], [0, 1, 2, 3], [1, 1, 1, 1], 1),
            (
                "plötzlich",
                "'pl9ts-lIC",
                ["p", "l", "9", "ts", "l", "I", "C"],
                [0, 1, 2, 3, 5, 6, 7],
                [1, 1, 1, 1, 2, 2, 2],
                2,
            ),
            ("bitte", "'bI-t@", ["b", "I", "t", "@"], [0, 1, 2, 4], [1, 1, 2, 2], 1),
            ("bitter", "'bI-t6", ["b", "I", "t", "6"], [0, 1, 2, 4], [1, 1, 2, 2], 1),
        ],
    )
    def test_create(self, orth, phon, phones, phones2graphs, syllables, stress_index):
        sound_seq = SoundSequence(orth, phon)

        sounds = [
            Sound(phone, start_char, syllable, i == stress_index)
            for i, (phone, start_char, syllable) in enumerate(
                zip(phones, phones2graphs, syllables)
            )
        ]

        assert sound_seq.orth == orth
        assert sound_seq.phon == phon
        assert sound_seq.sounds == sounds

    @pytest.mark.parametrize(
        ("orth", "phon", "index", "phone"),
        [
            ("Ananas", "a-na-nas", 0, "a"),
            ("Banane", "ba-na:-n@", 3, "a:"),
            ("blau", "blaU", 2, "aU"),
        ],
    )
    def test_next(self, orth, phon, index, phone):
        sound_seq = SoundSequence(orth, phon)
        sound_seq.index = index

        assert next(sound_seq).phone == phone

    @pytest.mark.parametrize(("orth", "phon", "index"), [("Ananas", "a-na-nas", 6)])
    def test_next_at_end_of_list(self, orth, phon, index):
        sound_seq = SoundSequence(orth, phon)
        sound_seq.index = index

        with pytest.raises(StopIteration):
            next(sound_seq)

    @pytest.mark.parametrize(
        ("orth", "phon", "index"),
        [
            ("Ananas", "a-na-nas", 0),
            ("Banane", "ba-na:-n@", 1),
            ("blau", "blaU", 2),
            ("b", "b", 1),
        ],
    )
    def test_set_start_index(self, orth, phon, index):
        sound_seq = SoundSequence(orth, phon)
        sound_seq.set_start_index()

        assert sound_seq.index == index

    @pytest.mark.parametrize(
        ("orth", "phon", "count"),
        [
            ("Ananas", "a-na-nas", 3),
            ("schweben", "Sve:-b@n", 2),
            ("Fahne", "fa:-n@", 2),
            ("zappeln", "tsa-p@ln", 2),
        ],
    )
    def test_count_syllables(self, orth, phon, count):
        sound_seq = SoundSequence(orth, phon)

        assert sound_seq.count_syllables() == count

    @pytest.mark.parametrize(
        ("orth", "phon", "ends_with_schwa"),
        [
            ("Ananas", "a-na-nas", False),
            ("schweben", "Sve:-b@n", False),
            ("zappeln", "tsa-p@ln", False),
            ("Fahne", "fa:-n@", True),
        ],
    )
    def test_ends_with_schwa(self, orth, phon, ends_with_schwa):
        sound_seq = SoundSequence(orth, phon)

        assert sound_seq.ends_with_schwa() == ends_with_schwa
