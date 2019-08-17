"""Main module."""
from pathlib import Path

from banone.generator import Generator


def main() -> None:
    """Run the banone generator."""
    dict_path = Path(__file__).resolve().parent.joinpath("dict/de.yaml")
    gen = Generator(dict_path)
    gen.generate_all()

    gen.dict.show_stats()
