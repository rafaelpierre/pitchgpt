from httpx import AsyncClient, HTTPError
from requests_html import HTMLSession, AsyncHTMLSession
from pydantic import BaseModel
from pitchgpt.config import PitchGptConfig
from tenacity import (
    wait_random,
    wait_fixed,
    stop_after_attempt,
    retry,
    retry_if_exception_type
)
import asyncio
import logging
import pyppeteer


class ReviewFetcher(BaseModel):

    config: PitchGptConfig = PitchGptConfig()
    start: int = 1
    size: int = 12

    @retry(
        stop = stop_after_attempt(10),
        reraise = True,
        wait = wait_fixed(2) + wait_random(0, 5),
        retry = retry_if_exception_type(HTTPError)
    )
    async def dispatch(
        self,
        start: int,
        size: int,
    ):
        url = self.config.base_url.format(start = start, size = size)
        logging.info(f"URL: {url}")

        async with AsyncClient(http2=True) as client:
            response = await client.get(
                url = url,
                headers = self.config.headers
            )
            logging.info(f"Response: {response.json()}")
            return response.json()

    async def fetch(self, num_pages: int = 10, parallelism: int = 2):
        
        results = []
        start = self.start
        current_batch = 0
        logging.info(f"parallelism={parallelism}, num_pages={num_pages}")

        while start <= num_pages:
            tasks = [
                asyncio.create_task(self.dispatch(start = page, size = self.size))
                for page
                in range(
                    start * current_batch + 1,
                    start * current_batch + parallelism
                )
            ]

            responses = await asyncio.gather(*tasks)
            results.extend(responses)
            start += len(responses)

        return results
    
    def parse_text(
        self,
        html,
        selector_options = ["contents dropcap","body__inner-container"]
    ):
        elements = []
        selector_idx = 0

        while not elements and (selector_idx < len(selector_options)):
            selector = selector_options[selector_idx]
            elements = html.find(f"[class='{selector}']")
            logging.info(f"Elements: {elements}")
            if elements:
                paragraphs = elements[0].find("p")
                break
            logging.info(f"Paragraphs")
            selector_idx += 1

        text = "\n".join([paragraph.text for paragraph in paragraphs])
        return text
    
    def get_review_text(
        self,
        url_suffix: str,
        sleep: int = 0,
        session = HTMLSession()
    ):
        
        url = "https://pitchfork.com{url_suffix}".format(url_suffix = url_suffix)
        logging.info(f"URL: {url}")

        r = session.get(url)
        r.html.render(sleep = sleep)
        
        text = self.parse_text(html = r.html)
        logging.info(text)
        
        return text
    
    async def aget_review_text(self, url_suffix: str, sleep: int = 2, session = AsyncHTMLSession()):
        
        loop = asyncio.get_event_loop()
        session.loop = loop

        url = "https://pitchfork.com{url_suffix}".format(url_suffix = url_suffix)
        logging.info(f"URL: {url}")

        r = await session.get(url)
        await r.html.arender(sleep = sleep)
        
        text = self.parse_text(html = r.html)
        logging.info(text)
        
        return text