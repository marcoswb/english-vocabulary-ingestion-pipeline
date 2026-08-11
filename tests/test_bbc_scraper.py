import pytest
from datetime import datetime
from src.scrapers.bbc import format_time, BBC


def test_get_articles_to_extract(mocker):
    scraper = BBC()

    scraper._BBC__main_page = mocker.Mock()
    scraper._BBC__main_page.get_itens.return_value = ["item1", "item2"]

    result = scraper._get_articles_to_extract()

    scraper._BBC__main_page.load_page.assert_called_once()
    scraper._BBC__main_page.get_itens.assert_called_once_with(
        'a.Anchor-styles__AnchorStyled-sc-651d33db-0'
    )

    assert result == ["item1", "item2"]

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
