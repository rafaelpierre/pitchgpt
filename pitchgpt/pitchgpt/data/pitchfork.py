import tenacity
from httpx import AsyncClient
from pydantic import BaseModel


class PitchforkDataFetcher(BaseModel):

    retry_min_seconds: int = 2
    retry_max_seconds: int = 5
    headers: dict = {
        "Accept": "application/json"
    }


    async def dispatch(url: str):

        async with AsyncClient(http2=True) as client:


    async def fetch_all(parallelism: int = 10):
        raise NotImplementedError()
