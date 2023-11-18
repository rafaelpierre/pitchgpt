import pytest
from pitchgpt.data.pitchfork import PitchforkDataFetcher
import logging
from unittest import mock
from pitchgpt.data.pitchfork import PitchforkDataFetcher

class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

@pytest.mark.asyncio
@mock.patch("httpx.AsyncClient.get", AsyncMock())
async def test_dispatch():

    from httpx import AsyncClient
    fetcher = PitchforkDataFetcher()
    response = await fetcher.dispatch(start = 1, size = 12)
    logging.info(response)

    AsyncClient.get.assert_called_once()

@pytest.mark.asyncio
@mock.patch("pitchgpt.data.pitchfork.PitchforkDataFetcher.dispatch", AsyncMock())
async def test_fetch_all():

    

    fetcher = PitchforkDataFetcher()
    await fetcher.fetch_all(
        num_pages = 10,
        parallelism = 10
    )

    PitchforkDataFetcher.dispatch.assert_called()