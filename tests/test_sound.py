import pytest

from banone.sound import Sound


class TestSound:
    @pytest.mark.parametrize(
        ("sound", "is_full_vowel"),
        [
            ("a:", True),
            ("U", True),
            ("aU", True),
            ("@", False),
            ("b", False),
            ("g", False),
        ],
    )
    def test_is_full_vowel(self, sound, is_full_vowel):
        sound = Sound(sound, 0)

        assert sound.is_full_vowel() == is_full_vowel
