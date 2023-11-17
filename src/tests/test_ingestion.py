import pytest
from pitchgpt.data.pitchfork import PitchforkDataFetcher
from tests.fixtures.pitchfork import url
import logging

@pytest.mark.asyncio
async def test_dispatch(url):
    fetcher = PitchforkDataFetcher()
    response = await fetcher.dispatch(start = 1, size = 12)
    logging.info(response)

    assert response
    assert isinstance(response, dict)

@pytest.mark.asyncio
async def test_fetch_all(url):
    fetcher = PitchforkDataFetcher()
    response = await fetcher.fetch_all(
        num_pages = 100,
        parallelism = 10
    )

    logging.info(response)
    assert response
    assert isinstance(response[0], dict)