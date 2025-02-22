from typing import Any, Dict, List, Optional
from unittest import mock

import pytest
# from braveblock import Adblocker
from pyppeteer.element_handle import ElementHandle
from pyppeteer.page import Page

try:
    from braveblock import Adblocker
except ImportError:
    pass

from dude_pyto import Scraper
from dude_pyto.optional.pyppeteer_scraper import PyppeteerScraper


@pytest.fixture()
def scraper_application_with_pyppeteer_parser() -> Scraper:
    scraper = PyppeteerScraper()
    scraper.adblock = Adblocker(rules=["https://dude_pyto.ron.sh/blockme.css"])
    return Scraper(scraper=scraper)


@pytest.fixture()
def async_pyppeteer_select(scraper_application: Scraper) -> None:
    @scraper_application.group(css=".custom-group")
    @scraper_application.select(css=".title")
    async def title(element: ElementHandle, page: Page) -> Dict:
        return {"title": await page.evaluate("(element) => element.textContent", element)}

    @scraper_application.select(css=".title", group_css=".custom-group")
    async def empty(element: ElementHandle, page: Page) -> Dict:
        return {}

    @scraper_application.group(css=".custom-group")
    @scraper_application.select(css=".title", url_match="example.com")
    async def url_dont_match(element: ElementHandle, page: Page) -> Dict:
        return {"title": await page.evaluate("(element) => element.textContent", element)}

    @scraper_application.select(css=".url", group_css=".custom-group")
    async def url(element: ElementHandle, page: Page) -> Dict:
        handle = await element.getProperty("href")
        return {"url": await handle.jsonValue()}


@pytest.fixture()
def async_pyppeteer_select_with_parser(scraper_application_with_pyppeteer_parser: Scraper) -> None:
    @scraper_application_with_pyppeteer_parser.group(css=".custom-group")
    @scraper_application_with_pyppeteer_parser.select(css=".title")
    async def title(element: ElementHandle, page: Page) -> Dict:
        return {"title": await page.evaluate("(element) => element.textContent", element)}

    @scraper_application_with_pyppeteer_parser.select(css=".title", group_css=".custom-group")
    async def empty(element: ElementHandle, page: Page) -> Dict:
        return {}

    @scraper_application_with_pyppeteer_parser.group(css=".custom-group")
    @scraper_application_with_pyppeteer_parser.select(css=".title", url_match="example.com")
    async def url_dont_match(element: ElementHandle, page: Page) -> Dict:
        return {"title": await page.evaluate("(element) => element.textContent", element)}

    @scraper_application_with_pyppeteer_parser.select(css=".url", group_css=".custom-group")
    async def url(element: ElementHandle, page: Page) -> Dict:
        handle = await element.getProperty("href")
        return {"url": await handle.jsonValue()}


@pytest.fixture()
def async_pyppeteer_xpath(scraper_application: Scraper) -> None:
    @scraper_application.select(
        xpath='.//p[contains(@class, "title")]', group_xpath='.//div[contains(@class, "custom-group")]'
    )
    async def title(element: ElementHandle, page: Page) -> Dict:
        return {"title": await page.evaluate("(element) => element.textContent", element)}

    @scraper_application.select(
        xpath='.//a[contains(@class, "url")]', group_xpath='.//div[contains(@class, "custom-group")]'
    )
    async def url(element: ElementHandle, page: Page) -> Dict:
        handle = await element.getProperty("href")
        return {"url": await handle.jsonValue()}


@pytest.fixture()
def async_pyppeteer_text(scraper_application: Scraper) -> None:
    @scraper_application.select(text="Title", group_css=".custom-group")
    async def title(element: ElementHandle, page: Page) -> Dict:
        return {"title": await page.evaluate("(element) => element.textContent", element)}

    @scraper_application.select(xpath='.//a[contains(@class, "url")]', group_css=".custom-group")
    async def url(element: ElementHandle, page: Page) -> Dict:
        handle = await element.getProperty("href")
        return {"url": await handle.jsonValue()}


@pytest.fixture()
def async_pyppeteer_regex(scraper_application: Scraper) -> None:
    @scraper_application.select(regex=".*", group_css=".custom-group")
    async def url(element: ElementHandle, page: Page) -> Dict:
        return {}


@pytest.fixture()
def async_pyppeteer_setup(scraper_application: Scraper) -> None:
    @scraper_application.select(css=":root", setup=True)
    async def check_page(element: ElementHandle, page: Page) -> None:
        assert element is not None
        assert page is not None


@pytest.fixture()
def async_pyppeteer_navigate(scraper_application: Scraper) -> None:
    @scraper_application.select(css=":root", navigate=True)
    async def next_page(element: ElementHandle, page: Page) -> bool:
        assert element is not None
        assert page is not None
        return True


@pytest.fixture()
def scraper_with_parser_save(scraper_application_with_pyppeteer_parser: Scraper, mock_database: mock.MagicMock) -> None:
    @scraper_application_with_pyppeteer_parser.save("custom")
    def save_to_database(data: Any, output: Optional[str]) -> bool:
        mock_database.save(data)
        return True


def test_full_flow(
    scraper_application: Scraper,
    async_pyppeteer_select: None,
    async_pyppeteer_setup: None,
    async_pyppeteer_navigate: None,
    expected_browser_data: List[Dict],
    file_url: str,
    scraper_save: None,
    mock_database: mock.MagicMock,
    mock_database_per_page: mock.MagicMock,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 6

    scraper_application.run(urls=[file_url], pages=2, format="custom", parser="pyppeteer", follow_urls=True)

    mock_database_per_page.save.assert_called_with(expected_browser_data)
    mock_database.save.assert_not_called()


def test_full_flow_async_without_setup_and_navigate(
    scraper_application: Scraper,
    async_pyppeteer_select: None,
    expected_browser_data: List[Dict],
    file_url: str,
    scraper_save: None,
    mock_database: mock.MagicMock,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 4

    scraper_application.run(urls=[file_url], pages=2, format="custom", parser="pyppeteer")

    mock_database.save.assert_called_with(expected_browser_data)


def test_full_flow_xpath(
    scraper_application: Scraper,
    async_pyppeteer_xpath: None,
    async_pyppeteer_setup: None,
    async_pyppeteer_navigate: None,
    expected_browser_data: List[Dict],
    file_url: str,
    scraper_save: None,
    mock_database: mock.MagicMock,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 4

    scraper_application.run(urls=[file_url], pages=2, format="custom", parser="pyppeteer")

    mock_database.save.assert_called_with(expected_browser_data)


def test_full_flow_text(
    scraper_application: Scraper,
    async_pyppeteer_text: None,
    async_pyppeteer_setup: None,
    async_pyppeteer_navigate: None,
    expected_browser_data: List[Dict],
    file_url: str,
    scraper_save: None,
    mock_database: mock.MagicMock,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 4

    scraper_application.run(urls=[file_url], pages=2, format="custom", parser="pyppeteer")

    mock_database.save.assert_called_with(expected_browser_data)


def test_unsupported_regex(
    scraper_application: Scraper,
    async_pyppeteer_regex: None,
    expected_browser_data: List[Dict],
    file_url: str,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 1

    with pytest.raises(Exception):
        scraper_application.run(urls=[file_url], pages=2, format="custom", parser="pyppeteer")


def test_scraper_with_parser(
    scraper_application_with_pyppeteer_parser: Scraper,
    async_pyppeteer_select_with_parser: None,
    expected_browser_data: List[Dict],
    file_url: str,
    scraper_with_parser_save: None,
    mock_database: mock.MagicMock,
) -> None:
    assert scraper_application_with_pyppeteer_parser.has_async is True
    assert scraper_application_with_pyppeteer_parser.scraper is not None
    assert len(scraper_application_with_pyppeteer_parser.scraper.rules) == 4

    scraper_application_with_pyppeteer_parser.run(urls=[file_url], pages=2, format="custom", parser="pyppeteer")

    mock_database.save.assert_called_with(expected_browser_data)
