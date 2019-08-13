from pathlib import Path

import pytest

from banone.generator import Generator
from tests.utils import load_test_data


class TestGenerator:
    @pytest.fixture(scope="class")
    def fxt_generator(self):
        return Generator(Path("banone/dict/de.yaml"))

    @pytest.mark.parametrize(
        ("str1", "str2", "question"), load_test_data(["base", "extra", "question"])
    )
    def test_generate_question(self, str1, str2, question, fxt_generator):
        base = fxt_generator.dict.lookup(str1)
        extra = fxt_generator.dict.lookup(str2)

        assert fxt_generator.generate_question(base, extra) == question

    @pytest.mark.parametrize(
        ("base", "compound", "answer"), load_test_data(["base", "compound", "answer"])
    )
    def test_generate_answer(self, base, compound, answer, fxt_generator):
        assert fxt_generator.generate_answer(base, compound) == answer

    @pytest.mark.parametrize(
        ("str1", "str2", "question", "answer"),
        load_test_data(["base", "extra", "question", "answer"]),
    )
    def test_generate_riddle(self, str1, str2, question, answer, fxt_generator):
        base = fxt_generator.dict.lookup(str1)
        extra = fxt_generator.dict.lookup(str2)

        assert fxt_generator.generate_riddle(base, extra) == str.format(
            "{}\n{}", question, answer
        )
