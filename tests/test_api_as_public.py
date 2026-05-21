from requests import codes

from grawgo.api import Api


def test_status(api_as_public: Api):
    assert api_as_public.status().status_code == codes.ok
