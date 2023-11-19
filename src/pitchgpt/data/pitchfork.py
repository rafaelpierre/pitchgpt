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
import nest_asyncio

nest_asyncio.apply()

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
    
    def get_review_text(self, url_suffix: str, sleep: int = 0):
        
        url = "https://pitchfork.com{url_suffix}".format(url_suffix = url_suffix)
        logging.info(f"URL: {url}")
        session = HTMLSession()

        r = session.get(url)
        if r.status_code != 200:
            raise HTTPError(f"HTTP Error: {r.status_code}")
        
        r.html.render(sleep = sleep)
        div_selector_options = [
            "[class='contents dropcap']",
            "[class='body__inner-container']"
        ]
        elements = []
        selector_idx = 0

        while not elements and (selector_idx < len(div_selector_options)):
            selector = div_selector_options[selector_idx]
            elements = r.html.find(selector)
            logging.info(f"Elements: {elements}")
            if elements:
                paragraphs = elements[0].find("p")
                break
            logging.info(f"Paragraphs")
            selector_idx += 1

        review_text = "\n".join([paragraph.text for paragraph in paragraphs])
        logging.info(review_text)
        
        return review_text
    
    async def aget_review_text(self, url_suffix: str, sleep: int = 0):
        
        url = "https://pitchfork.com{url_suffix}".format(url_suffix = url_suffix)
        logging.info(f"URL: {url}")
        asession = AsyncHTMLSession()

        r = await asession.get(url)
        await r.html.arender(sleep = sleep)
        div_selector_options = [
            "[class='contents dropcap']",
            "[class='body__inner-container']"
        ]
        elements = []
        selector_idx = 0

        while not elements and (selector_idx < len(div_selector_options)):
            selector = div_selector_options[selector_idx]
            elements = r.html.find(selector)
            logging.info(f"Elements: {elements}")
            if elements:
                paragraphs = elements[0].find("p")
                break
            logging.info(f"Paragraphs")
            selector_idx += 1

        review_text = "\n".join([paragraph.text for paragraph in paragraphs])
        logging.info(review_text)
        
        return review_text
