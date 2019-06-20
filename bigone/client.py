import requests
import json
from jose import jwt
import time

from .exceptions import BigoneRequestException, BigoneAPIException

class Client(object):
    API_URL = 'https://b1.run/api'
    PUBLIC_API_VERSION = 'v3'
    PRIVATE_API_VERSION = 'v3'

    SIDE_BUY = 'BID'
    SIDE_SELL = 'ASK'

    CANDLE_PERIOD_1MINUTE = "min1"
    CANDLE_PERIOD_5MINUTE = "min5"
    CANDLE_PERIOD_15MINUTE = "min15"
    CANDLE_PERIOD_30MINUTE = "min30"
    CANDLE_PERIOD_1HOUR = "hour1"
    CANDLE_PERIOD_3HOUR = "hour3"
    CANDLE_PERIOD_4HOUR = "hour4"
    CANDLE_PERIOD_6HOUR = "hour6"
    CANDLE_PERIOD_12HOUR = "hour12"
    CANDLE_PERIOD_1DAY = "day1"
    CANDLE_PERIOD_1WEEK = "week1"
    CANDLE_PERIOD_1MONTH = "month1"

    def __init__(self, api_key, api_secret, requests_params=None):

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.session = self._init_session()
        self._requests_params = requests_params
        
        self.ping()


    def _init_session(self):

        session = requests.session()
        session.headers.update({'Accept': 'application/json',
                                'User-Agent': 'bigone/python'})
        return session

    def _create_api_uri(self, path, signed=False):
        v = self.PRIVATE_API_VERSION if signed else self.PUBLIC_API_VERSION
        return self.API_URL + '/' + v + path

    def _sign_token(self):
        payload = {
            "type": "OpenAPI",
            "sub": self.API_KEY,
            "nonce": int(round((time.time()) * 10**9))
        }
        return jwt.encode(payload, self.API_SECRET, algorithm="HS256")

    def _request(self, method, uri, signed, **kwargs):
        
        kwargs['timeout'] = 10

        if self._requests_params:
            kwargs.update(self._requests_params)

        if signed:
            kwargs['headers'] = {
                "Authorization": "Bearer " + self._sign_token()
            }

        #todo: handle pagenation request

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)
    
    def _handle_response(self, response):
        try:
            json_response = response.json()
            code = json_response['code']
            if code == 0:
                return json_response['data']
            message = json_response['message']
            raise BigoneAPIException(code, message)
        except:
            raise BigoneRequestException('Invalid Response: %s' % response.text)

    def _request_api(self, method, path, signed=False, **kwargs):
        uri = self._create_api_uri(path, signed)

        return self._request(method, uri, signed, **kwargs)

    def _get(self, path, signed=False, **kwargs):
        return self._request_api('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs):
        return self._request_api('post', path, signed, **kwargs)

    def _put(self, path, signed=False, **kwargs):
        return self._request_api('put', path, signed, **kwargs)

    def _delete(self, path, signed=False, **kwargs):
        return self._request_api('delete', path, signed, **kwargs)

    def ping(self):
        return self._get('/ping')

    def get_server_time(self):
        return self._get('/ping')

    def get_asset_pairs(self):
        return self._get('/asset_pairs')

    def get_asset_pair_info(self, asset_pair_name):
        res = self.get_asset_pairs()

        for item in res:
            if item['name'] == asset_pair_name.upper():
                return item
        return None
    
    def get_asset_pair_ticker(self, asset_pair_name):
        return self._get('/asset_pairs/%s/ticker' % asset_pair_name.upper())

    def get_asset_pair_trades(self, asset_pair_name):
        return self._get('/asset_pairs/%s/trades' % asset_pair_name.upper())

    def get_order_book(self, asset_pair_name, limit = 50):
        uri = '/asset_pairs/%s/depth' % asset_pair_name.upper()
        params = {
            'limit': limit
        }
        return self._get(uri, params = params)

    def get_candles(self, asset_pair_name, **params):
        uri = '/asset_pairs/%s/candles' % asset_pair_name.upper()
        return self._get(uri, params = params)

    def get_accounts(self):
        return self._get('/viewer/accounts', True)

    def get_asset_balance(self, asset_symbol):
        return self._get('/viewer/accounts/%s' % asset_symbol.upper(), True)

    def get_all_orders(self, **params):
        return self._get('/viewer/orders', True, params = params)

    def get_order(self, order_id):
        return self._get('/viewer/orders/%s' % order_id, True)

    def create_order(self, **params):
        return self._post('/viewer/orders', True, json = params)

    def order_limmit(self, **params):
        return self.create_order(**params)
    
    def order_limit_buy(self, **params):
        params.update({
            'side': self.SIDE_BUY
        })
        return self.order_limmit(**params)

    def order_limit_sell(self, **params):
        params.update({
            'side': self.SIDE_SELL
        })
        return self.order_limmit(**params)

    def cancel_order(self, order_id):
        return self._post('/viewer/orders/{id}/cancel' % order_id, True)

    def cancel_all_orders(self, asset_pair_name):
        params = {
            'asset_pair_name': asset_pair_name.upper()
        }
        return self._post('/viewer/orders/cancel', True, params = params)

    def get_my_trades(self, **params):
        return self._get('/viewer/trades', True, params = params)
    
    def get_withdraw_history(self, **params):
        return self._get('/viewer/withdrawals', True, params = params)

    def get_deposit_history(self, **params):
        return self._get('/viewer/deposits', True, params = params)

    def get_deposit_address(self, asset_symbol):
        return self._get('/viewer/assets/%s/address' % asset_symbol.upper(), True)
    