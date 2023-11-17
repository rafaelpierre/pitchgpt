from httpx import AsyncClient
from pydantic import BaseModel
import pydantic
from pitchgpt.data.models.headers import ApiHeaders
from tenacity import (
    wait_random,
    wait_fixed,
    stop_after_attempt,
    retry
)
import asyncio

class PitchforkDataFetcher(BaseModel):

    api_headers: ApiHeaders = ApiHeaders()
    start: int = 1
    size: int = 12
    base_url: str = "https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Falbums%2Cchannels%2Freviews%2Falbums&sort=publishdate%20desc%2Cposition%20asc&size={size}&start={start}"

    @pydantic.computed_field()
    @property
    def headers(self) -> dict:
        return self.api_headers.model_dump(by_alias = True)

    @retry(
        stop = stop_after_attempt(10),
        reraise = True,
        wait = wait_fixed(2) + wait_random(0, 5)
    )
    async def dispatch(
        self,
        start: int,
        size: int,
    ):

        url = self.base_url.format(start = start, size = size)

        async with AsyncClient(http2=True) as client:
            response = await client.get(
                url = url,
                headers = self.headers
            )

            return response.json()

    async def fetch_all(self, num_pages: int = 10, parallelism: int = 2):
        
        results = []
        start = self.start
        current_batch = 0

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