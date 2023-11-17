import pytest

@pytest.fixture
def url():
    basic_url = "https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Falbums%2Cchannels%2Freviews%2Falbums&sort=publishdate%20desc%2Cposition%20asc&size={size}&start={start}"
    return basic_url