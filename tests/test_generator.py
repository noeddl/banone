from pathlib import Path

import pytest

from banone.generator import Generator
from banone.lemma import Lemma
from tests.utils import load_test_data


class TestGenerator:
    @pytest.fixture(scope="class")
    def fxt_generator(self):
        return Generator(Path("banone/dict/de.yaml"))

    @pytest.mark.parametrize(
        ("base_str", "extra_str", "question"),
        load_test_data(["base", "extra", "question"]),
    )
    def test_generate_question(self, base_str, extra_str, question, fxt_generator):
        base = fxt_generator.dict.lookup(base_str)
        extra = fxt_generator.dict.lookup(extra_str)

        assert fxt_generator.generate_question(base, extra) == question

    @pytest.mark.parametrize(
        ("base_str", "compound_str", "answer"),
        load_test_data(["base", "compound", "answer"]),
    )
    def test_generate_answer(
        self, base_str, compound_str, answer, fxt_generator, fxt_dict
    ):
        base = fxt_dict.lookup(base_str)
        compound = Lemma(compound_str)

        assert fxt_generator.generate_answer(base, compound) == answer

    @pytest.mark.parametrize(
        ("base_str", "extra_str", "question", "answer"),
        load_test_data(["base", "extra", "question", "answer"]),
    )
    def test_generate_riddle(
        self, base_str, extra_str, question, answer, fxt_generator
    ):
        base = fxt_generator.dict.lookup(base_str)
        extra = fxt_generator.dict.lookup(extra_str)

        assert fxt_generator.generate_riddle(base, extra) == str.format(
            "{}\n{}", question, answer
        )
