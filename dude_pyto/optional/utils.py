import logging
import time
from typing import Iterable, Optional, Tuple

import httpx
from httpx import Request

logger = logging.getLogger(__name__)


async def async_http_get(client: httpx.AsyncClient, request: Request) -> Tuple[Optional[str], str]:
    try:
        response = await client.send(request)
        response.raise_for_status()
        return response.text, str(response.url)
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        logger.warning(e)
        return None, str(request.url)


def http_get(client: httpx.Client, request: Request) -> Tuple[Optional[str], str]:
    try:
        response = client.send(request)
        response.raise_for_status()
        return response.text, str(response.url)
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        logger.warning(e)
        return None, str(request.url)


class HTTPXMixin:
    # @staticmethod
    def _block_httpx_request_if_needed(self, request: Request) -> None:
        url = str(request.url)
        source_url = (
            request.headers.get("referer") or request.headers.get("origin") or request.headers.get("host") or url
        )
        request_type = request.headers.get("sec-fetch-dest")
        # try:
        #     if self.adblock.check_network_urls(  # type: ignore
        #         url=url,
        #         source_url=source_url,
        #         request_type=request.headers.get("sec-fetch-dest") or "other",
        #     ):
        #         logger.info("URL %s has been blocked.", url)
        #         raise httpx.RequestError(message=f"URL {url} has been blocked.", request=request)
        # except AttributeError:
        #     httpx.RequestError()
        #     # logger.info("URL %s has been blocked.", url)
        #     # raise httpx.RequestError(message=f"URL {url} has been blocked.", request=request)

    async def _async_block_httpx_request_if_needed(self, request: Request) -> None:
        self._block_httpx_request_if_needed(request)

    def iter_requests(self) -> Iterable[Request]:
        try:
            while True:
                try:
                    url = next(self.iter_urls())  # type: ignore
                    yield Request(method="GET", url=url)
                    continue
                except StopIteration:
                    pass
                request = self.requests.popleft()  # type: ignore
                can_fetch, crawl_delay = self.can_fetch_and_crawl_delay(str(request.url))  # type: ignore
                if not can_fetch:
                    logger.info("Not allowed to crawl %s", str(request.url))
                    continue
                time.sleep(crawl_delay)
                self.current_url = str(request.url)  # type: ignore
                yield request
        except IndexError:
            pass


def get_chromedriver_latest_release() -> str:
    """
    https://chromedriver.chromium.org/downloads/version-selection
    """
    import browsers

    version = browsers.get("chrome")["version"].rsplit(".", 1)[0]

    with httpx.Client() as client:
        try:
            response = client.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}")
            response.raise_for_status()
            latest = response.text.strip()
            logger.info("Matching ChromeDriver latest release is %s", latest)
            return latest
        except httpx.HTTPStatusError as e:
            logger.exception(e)

        return "latest"
