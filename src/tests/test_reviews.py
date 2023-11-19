from pitchgpt.data.pitchfork import ReviewFetcher
import logging

def test_get_review():

    suffix = "/reviews/albums/danny-brown-quaranta/"
    fetcher = ReviewFetcher()
    review = fetcher.get_review_text(url_suffix = suffix)
    logging.info(review)

    assert review