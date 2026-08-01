import pytest
from datetime import datetime
from src.scrapers.bbc import format_time


@pytest.mark.parametrize("str_time", [
    "1 hour ago",
    "15 hours ago",
    "1 minute ago",
    "57 minutes ago",
    "1 day ago",
    "4 days ago",
    "11 days ago",
])
def test_format_time(str_time):
    timestamp = format_time(str_time)
    assert timestamp is not None

    parsed = datetime.fromisoformat(timestamp)
    assert isinstance(parsed, datetime)

@pytest.mark.parametrize("str_time", [
    "4 May 2026",
    "20 July 2026",
    "31 May 2026",
    "Yesterday",
    "abc",
    ""
])
def test_format_time_invalid(str_time):
    assert format_time(str_time) is None
