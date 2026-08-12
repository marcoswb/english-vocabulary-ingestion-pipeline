import pytest
from datetime import datetime
from src.scrapers.bbc import format_time, BBC


@pytest.fixture
def scraper(mocker):
    scraper = BBC()
    scraper._BBC__main_page = mocker.Mock()
    return scraper


def test_get_articles_to_extract(scraper):
    scraper._BBC__main_page.get_itens.return_value = ["item1", "item2"]

    result = scraper._get_articles_to_extract()

    scraper._BBC__main_page.load_page.assert_called_once()
    scraper._BBC__main_page.get_itens.assert_called_once_with(
        'a.Anchor-styles__AnchorStyled-sc-651d33db-0'
    )

    assert result == ["item1", "item2"]


def test_get_link_from_item_without_href(scraper):
    item = {"hrefe": "https://www.bbc.com/news/article"}
    with pytest.raises(KeyError):
        scraper._get_link_from_item(item)


def test_get_link_from_item_with_valid_internal_link(scraper):
    link_base = "https://www.bbc.com/news/article"
    item = {"href": str(link_base)}

    scraper._BBC__main_page.is_link.return_value = True
    scraper._BBC__main_page.is_internal_link.return_value = True

    result = scraper._get_link_from_item(item)

    scraper._BBC__main_page.is_link.assert_called_once_with(link_base)
    scraper._BBC__main_page.is_internal_link.assert_called_once_with("/news/article")

    assert result == link_base


def test_get_link_from_item_with_invalid_internal_link(scraper):
    link_base = "https://www.bbc.com/news"
    item = {"href": str(link_base)}

    scraper._BBC__main_page.is_link.return_value = True
    scraper._BBC__main_page.is_internal_link.return_value = False

    result = scraper._get_link_from_item(item)

    scraper._BBC__main_page.is_link.assert_called_once_with(link_base)
    scraper._BBC__main_page.is_internal_link.assert_called_once_with("/news")

    assert result is None


def test_get_link_from_item_with_external_link(scraper):
    link_base = "https://www.google.com"
    item = {"href": str(link_base)}

    scraper._BBC__main_page.is_link.return_value = True

    result = scraper._get_link_from_item(item)

    scraper._BBC__main_page.is_link.assert_called_once_with(link_base)
    scraper._BBC__main_page.is_internal_link.assert_not_called()

    assert result == link_base


def test_get_link_from_item_with_relative_link(scraper):
    item = {"href": "/news/article"}

    scraper._BBC__main_page.is_link.return_value = False
    scraper._BBC__main_page.is_internal_link.return_value = True

    result = scraper._get_link_from_item(item)

    scraper._BBC__main_page.is_link.assert_called_once_with("/news/article")
    scraper._BBC__main_page.is_internal_link.assert_called_once_with("/news/article")

    assert result == "https://www.bbc.com/news/article"


def test_get_link_from_item_with_invalid_link(scraper):
    item = {"href": "invalid_link"}

    scraper._BBC__main_page.is_link.return_value = False
    scraper._BBC__main_page.is_internal_link.return_value = False

    result = scraper._get_link_from_item(item)

    scraper._BBC__main_page.is_link.assert_called_once_with("invalid_link")
    scraper._BBC__main_page.is_internal_link.assert_called_once_with("invalid_link")

    assert result is None


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
