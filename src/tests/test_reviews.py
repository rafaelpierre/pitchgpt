import pytest
from pitchgpt.data.pitchfork import ReviewFetcher
import logging

def test_get_review():

    suffix = "/reviews/albums/danny-brown-quaranta/"
    fetcher = ReviewFetcher()
    review = fetcher.get_review_text(url_suffix = suffix)
    logging.info(review)

    assert review

def test_aget_review():

    suffix = "/reviews/albums/danny-brown-quaranta/"
    fetcher = ReviewFetcher()
    review = fetcher.aget_review_text(url_suffix = suffix, sleep = 1)
    logging.info(review)

    assert review