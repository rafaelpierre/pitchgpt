import pytest
import logging
from unittest import mock
from pitchgpt.data.pitchfork import ReviewFetcher

class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

@pytest.mark.asyncio
@mock.patch("httpx.AsyncClient.get", AsyncMock())
async def test_dispatch():

    from httpx import AsyncClient
    fetcher = ReviewFetcher()
    response = await fetcher.dispatch(start = 1, size = 12)
    logging.info(response)

    AsyncClient.get.assert_called_once()

@pytest.mark.asyncio
@mock.patch("pitchgpt.data.pitchfork.ReviewFetcher.dispatch", AsyncMock())
async def test_fetch():

    fetcher = ReviewFetcher()
    await fetcher.fetch(
        num_pages = 10,
        parallelism = 10
    )

    ReviewFetcher.dispatch.assert_called()

def test_get_review():

    suffix = "/reviews/albums/danny-brown-quaranta/"
    fetcher = ReviewFetcher()
    review = fetcher.get_review_text(url_suffix = suffix)
    logging.info(review)

    assert False