import pytest
from src.utils.functions import is_advanced_word

@pytest.mark.parametrize("word", [
    "abstruse",
    "supercalifragilisticexpialidocious",
])
def test_advanced_word(word):
    assert is_advanced_word(word)


@pytest.mark.parametrize("word", [
    "cat",
    "the",
    "a",
    "book"
])
def test_not_advanced_word(word):
    assert not is_advanced_word(word)

