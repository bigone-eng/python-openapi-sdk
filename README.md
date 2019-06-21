BigONE 并不保证本程序的正确性，使用者应该知道并理解其中的风险，并自愿承担由于代码原因造成的损失。

# python-openapi-sdk
OpenAPI SDK written in Python

# Quick Start
```python
from bigone.client import Client
client = Client(api_key, secret_key)

# get all asset pairs
asset_pairs = client.get_asset_pairs()
for asset_pair in asset_pairs:
    # print(asset_pair['name'])
    pass

# get asset pair by name
one_usdt_info = client.get_asset_pair_info('ONE-USDT')
#print(one_usdt_info)

# get ONE-USDT's ticker
one_usdt_ticker = client.get_asset_pair_ticker('ONE-USDT')
#print(one_usdt_ticker)

# get ONE-USDT's depth
one_usdt_depth = client.get_order_book('ONE-USDT')
#print(one_usdt_depth)

# get ONE-USDT's trades
one_usdt_trades = client.get_asset_pair_trades('ONE-USDT')
# print(one_usdt_trades)

# get ONE-USDT's min5 candles
one_usdt_candles = client.get_candles('ONE-USDT', period = client.CANDLE_PERIOD_5MINUTE)
# print(one_usdt_candles)

# get all accounts
accounts = client.get_accounts()
for account in accounts:
    symbol = account['asset_symbol']
    balance = Decimal(account['balance'])
    locked_balance = Decimal(account['locked_balance'])

    if not balance.is_zero():
        # print("%s: %s" % (symbol,balance - locked_balance))
        pass

# get one balance
one_account = client.get_asset_balance('ONE')
# print(one_account)

# create limit order
# todo:

# get all orders
orders = client.get_all_orders()
# print(orders)
```
