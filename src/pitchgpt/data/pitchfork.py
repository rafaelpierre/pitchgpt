from httpx import AsyncClient, HTTPError
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

class PitchforkDataFetcher(BaseModel):

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

    async def fetch_all(self, num_pages: int = 10, parallelism: int = 2):
        
        results = []
        start = self.start
        current_batch = 0
        logging.info(f"parallelism={parallelism}, num_pages={num_pages}")

        while start < num_pages:
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