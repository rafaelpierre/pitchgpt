import pytest
from pitchgpt.data.pitchfork import ReviewFetcher
import logging
import asyncio

def test_get_review():

    suffix = "/reviews/albums/danny-brown-quaranta/"
    fetcher = ReviewFetcher()
    review = fetcher.get_review_text(url_suffix = suffix)
    logging.info(review)

    assert review

@pytest.mark.asyncio
async def test_aget_review():

    suffix = "/reviews/albums/danny-brown-quaranta/"
    fetcher = ReviewFetcher()
    review = await fetcher.aget_review_text(url_suffix = suffix, sleep = 3)
    logging.info(review)

    assert review