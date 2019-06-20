from bigone.client import Client
from bigone.exceptions import BigoneRequestException, BigoneAPIException

import pytest
import requests_mock

client = Client('api_key', 'api_secret')

def test_invalid_json():
    """Test Invalid response Exception"""

    with pytest.raises(BigoneRequestException):
        with requests_mock.mock() as m:
            m.get('https://b1.run/api/v3/ping', text='<head></html>')
            client.ping()

def test_api_exception():
    """Test API response Exception"""

    with pytest.raises(BigoneAPIException):
        with requests_mock.mock() as m:
            json_obj = {"code": 40004, "message": "unauthorized", "data": None}
            m.get('https://b1.run/api/v3/ping', json=json_obj, status_code=400)
            client.ping()