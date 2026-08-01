import pytest
from datetime import datetime
from src.utils.functions import (
    is_advanced_word,
    get_s3_bucket,
    get_current_timestamp
)


def test_get_current_timestamp_returns_iso_string():
    timestamp = get_current_timestamp()
    assert isinstance(timestamp, str)

    parsed = datetime.fromisoformat(timestamp)
    assert isinstance(parsed, datetime)


def test_get_s3_bucket_returns_string():
    bucket_name = get_s3_bucket()
    assert isinstance(bucket_name, str)
    assert len(bucket_name) > 0


@pytest.mark.parametrize("word", [
    "abstruse",
    "hello",
    "monday",
    "january",
    "supercalifragilisticexpialidocious",
])
def test_advanced_word(word):
    assert is_advanced_word(word)


@pytest.mark.parametrize("word", [
    "cat",
    "the",
    "a",
    "book",
    "run"
])
def test_not_advanced_word(word):
    assert not is_advanced_word(word)
