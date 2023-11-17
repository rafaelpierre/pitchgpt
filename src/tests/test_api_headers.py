from pitchgpt.data.models.headers import ApiHeaders
import logging

def test_headers(headers):

    api_headers = ApiHeaders()
    dict_headers = api_headers.model_dump(by_alias = True)
    logging.info(dict_headers)

    assert sorted(dict_headers.keys()) == sorted(headers.keys())