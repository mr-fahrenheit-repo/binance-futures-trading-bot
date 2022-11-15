# Import Libraries
import os
import pytz
import talib as ta
import pandas as pd
from binance.client import Client

# Binance API
binance_api = os.getenv('binance_api_key')
binance_secret = os.getenv('binance_secret_key')

# Set binance API Client
client = Client(binance_api, binance_secret)


# Getting all the stock with USDT pair symbol in a list
def stock_list():
  info = client.futures_exchange_info()
  df_info = pd.DataFrame(info['symbols'])
  df_info = df_info[df_info['symbol'].str.contains('USDT')]
  stock_list = list(df_info["symbol"])
  stock_list = [x for x in stock_list if x[-4:] == 'USDT']
  return stock_list


# Getting all the stock with non-USDT pair symbol in a list
def non_stock_list():
  info = client.futures_exchange_info()
  df_info = pd.DataFrame(info['symbols'])
  stock_list = list(df_info["symbol"])
  non_stock_list = [x for x in stock_list if x[-4:] != 'USDT']
  return non_stock_list


# Stock list pair data information
def pair_info():
  ex_info = client.futures_exchange_info()
  df_ex_info = pd.DataFrame(ex_info['symbols'])
  df_filters = pd.DataFrame(list(df_ex_info['filters']))
  filters = pd.DataFrame(list(df_filters[0]))
  tick = pd.DataFrame(list(df_filters[1]))
  data = df_ex_info[[
    'symbol', 'pricePrecision', 'quantityPrecision', 'timeInForce'
  ]]
  data = pd.concat([data, tick, filters], axis=1)
  pos_info = client.futures_position_information()
  df_pos_info = pd.DataFrame(pos_info)
  df_pos_info = df_pos_info[['symbol', 'leverage', 'marginType']]
  df_pos_info = df_pos_info.set_index(df_pos_info['symbol'])
  df_pos_info = df_pos_info.loc[list(data['symbol'])]
  df_pos_info = df_pos_info.reset_index(drop=True)
  data = pd.concat([data, df_pos_info], axis=1)
  data = data.loc[:, ~data.columns.duplicated()].copy()
  data = data.set_index(data['symbol'])
  data = data.drop([
    'symbol', 'filterType', 'stepSize', 'timeInForce', 'maxQty', 'minQty',
    'minPrice', 'maxPrice', 'tickSize'
  ],
                   axis=1)
  data = data.drop(non_stock_list())
  return data


# pairs leverage functions
def call_leverage(symbol):
  df = pair_info()
  df = df[['leverage']]
  x = int(df.loc[symbol, 'leverage'])
  return x


# price precission functions
def price_precision(symbol):
  x = pair_info()
  x = int(x.loc[symbol]['pricePrecision'])
  return x


# quantity precission size functions
def quantity_precision(symbol):
  x = pair_info()
  x = int(x.loc[symbol]['quantityPrecision'])
  return x


# Calling for account balance
def my_balance():
  data_balance = client.futures_account_balance()
  balance = pd.DataFrame(data_balance)
  balance = balance.drop(['updateTime'], axis=1)
  balance = balance.set_index('asset')
  balance = balance['balance']['USDT']
  balance = round(float(balance), 2)
  return balance


# Account balance
mybalance = my_balance()

# Captial per trade
caps = round(float(mybalance / 10), 2)  # float capital number number

# Profit percentage per trade
profit_percent = 5  # change this
take_profit = round(float(profit_percent / 100), 1)


# Confirming caps is enough for the trades
def caps_confirm():
  if (my_balance() - total_margin()) > caps:
    return True
  else:
    return False


# Market price functions
def market_price(symbol):
  x = client.futures_ticker(symbol=symbol)
  x = round(float(x['lastPrice']), price_precision(symbol))
  return x


# Change leverage for every stock pair
def leverage_change(symbol):
  for lev_range in range(21):
    try:
      client.futures_change_leverage(symbol=symbol, leverage=lev_range)
    except:
      pass
    else:
      print("{} Leverage is {}".format(symbol, lev_range))
      leverage = lev_range

  return leverage


# Change Margin Type for every stock pair
def change_margin(symbol):
  try:
    client.futures_change_margin_type(symbol=symbol, marginType='ISOLATED')
  except:
    print("Can't change margin type")
  else:
    print('Change margin type Success')
    print('{} margin type is ISOLATED'.format(symbol))


# function for defining quantity
def quantities(price, symbol):
  leverage = call_leverage(symbol)
  init_caps = caps
  quantity = leverage * init_caps
  quantity = round(float(quantity / price), quantity_precision(symbol))
  return quantity


#Total margin in active position
def total_margin():
  x = client.futures_position_information()
  df = pd.DataFrame(x)
  df[['unRealizedProfit',
      'isolatedWallet']] = df[['unRealizedProfit',
                               'isolatedWallet']].astype(float)
  df = df[['symbol', 'unRealizedProfit', 'isolatedWallet']]
  df = df.loc[df['isolatedWallet'].values > 0]
  margin = df['isolatedWallet'].sum()
  return margin


# Total UnRealized Profit in active position
def total_pnl():
  x = client.futures_position_information()
  df = pd.DataFrame(x)
  df[['unRealizedProfit',
      'isolatedWallet']] = df[['unRealizedProfit',
                               'isolatedWallet']].astype(float)
  df = df[['symbol', 'unRealizedProfit', 'isolatedWallet']]
  df = df.loc[df['isolatedWallet'].values > 0]
  pnl = df['unRealizedProfit'].sum()
  return pnl


# Order quantity in active position
def order_quantity(symbol):
  x = client.futures_position_information()
  df = pd.DataFrame(x)
  df[['positionAmt', 'unRealizedProfit', 'isolatedWallet'
      ]] = df[['positionAmt', 'unRealizedProfit',
               'isolatedWallet']].astype(float)
  df = df[['symbol', 'positionAmt', 'unRealizedProfit', 'isolatedWallet']]
  df = df.loc[df['isolatedWallet'].values > 0]
  df = df.set_index(df['symbol'])
  quantity = round(float(df['positionAmt'][symbol]),
                   quantity_precision(symbol))
  return quantity


# Order price in active position
def order_price(symbol):
  x = client.futures_position_information()
  df = pd.DataFrame(x)
  df[['positionAmt', 'entryPrice', 'unRealizedProfit',
      'isolatedWallet']] = df[[
        'positionAmt', 'entryPrice', 'unRealizedProfit', 'isolatedWallet'
      ]].astype(float)
  df = df[[
    'symbol', 'positionAmt', 'entryPrice', 'unRealizedProfit', 'isolatedWallet'
  ]]
  df = df.loc[df['isolatedWallet'].values > 0]
  df = df.set_index(df['symbol'])
  price = round(float(df['entryPrice'][symbol]), price_precision(symbol))
  return price


# check the order
def check_order(symbol):
  x = client.futures_position_information()
  df = pd.DataFrame(x)
  df[['positionAmt', 'entryPrice', 'unRealizedProfit',
      'isolatedWallet']] = df[[
        'positionAmt', 'entryPrice', 'unRealizedProfit', 'isolatedWallet'
      ]].astype(float)
  df = df[[
    'symbol', 'positionAmt', 'entryPrice', 'unRealizedProfit', 'isolatedWallet'
  ]]
  df = df.loc[df['isolatedWallet'].values > 0]
  df = df.set_index(df['symbol'])
  check = symbol in df.index
  return check


# List of active order
def order_list():
  x = client.futures_position_information()
  df = pd.DataFrame(x)
  df[['positionAmt', 'unRealizedProfit', 'isolatedWallet'
      ]] = df[['positionAmt', 'unRealizedProfit',
               'isolatedWallet']].astype(float)
  df = df[['symbol', 'positionAmt', 'unRealizedProfit', 'isolatedWallet']]
  df = df.loc[df['isolatedWallet'].values > 0]
  order_list = list(df['symbol'])
  return order_list


# create list of every open order
def open_order_list():
  x = client.futures_get_open_orders()
  df = pd.DataFrame(x)
  open_list = list(df['symbol'])
  return open_list


# canceling all open order list
def cancel_open_order():
  for i in open_order_list():
    client.futures_cancel_all_open_orders(symbol=i)


# Create Buy Order functions
def cancel_buy_order(symbol):
  order = client.futures_create_order(symbol=symbol,
                                      side='SELL',
                                      type='MARKET',
                                      quantity=order_quantity(symbol))
  return order


# Create Sell Order functions
def cancel_sell_order(symbol):
  order = client.futures_create_order(symbol=symbol,
                                      side='BUY',
                                      type='MARKET',
                                      quantity=order_quantity(symbol))
  return order


# Create Buy Order functions
def buy_order(symbol):
  order = client.futures_create_order(symbol=symbol,
                                      side='BUY',
                                      type='MARKET',
                                      quantity=quantities(
                                        market_price(symbol), symbol))
  return order


# Create Sell Order functions
def sell_order(symbol):
  order = client.futures_create_order(symbol=symbol,
                                      side='SELL',
                                      type='MARKET',
                                      quantity=quantities(
                                        market_price(symbol), symbol))
  return order


# Take profit for sell order
def sell_take_profit(symbol):
  order = client.futures_create_order(
    symbol=symbol,
    side='BUY',
    type='TAKE_PROFIT',
    quantity=abs(order_quantity(symbol)),
    price=round(
      float(order_price(symbol) * (1 - (take_profit / call_leverage(symbol)))),
      price_precision(symbol)),
    stopPrice=round(
      float(order_price(symbol) * (1 - (take_profit / call_leverage(symbol)))),
      price_precision(symbol)),
    reduceOnly=True,
    timeInForce='GTC')
  return order


# Stop loss for sell order
def sell_stop_loss(symbol):
  order = client.futures_create_order(
    symbol=symbol,
    side='BUY',
    type='STOP',
    quantity=abs(order_quantity(symbol)),
    price=order_price(symbol),
    stopPrice=round(
      float(order_price(symbol) * (1 + (1 / call_leverage(symbol)))),
      price_precision(symbol)),
    reduceOnly=True,
    timeInForce='GTC')
  return order


# Take profit for buy order
def buy_take_profit(symbol):
  order = client.futures_create_order(
    symbol=symbol,
    side='SELL',
    type='TAKE_PROFIT',
    quantity=abs(order_quantity(symbol)),
    price=round(
      float(order_price(symbol) * (1 + (take_profit / call_leverage(symbol)))),
      price_precision(symbol)),
    stopPrice=round(
      float(order_price(symbol) * (1 + (take_profit / call_leverage(symbol)))),
      price_precision(symbol)),
    reduceOnly=True,
    timeInForce='GTC')
  return order


# Stop loss for buy order
def buy_stop_loss(symbol):
  order = client.futures_create_order(
    symbol=symbol,
    side='SELL',
    type='STOP',
    quantity=abs(order_quantity(symbol)),
    price=order_price(symbol),
    stopPrice=round(
      float(order_price(symbol) * (1 - (1 / call_leverage(symbol)))),
      price_precision(symbol)),
    reduceOnly=True,
    timeInForce='GTC')
  return order


# PNL >= total margin
def pnl_reached():
  if total_pnl() > (total_margin() * 0.5):
    return True
  else:
    return False


# Cancel all active order under pnl_reached condition
def cancel_active_order():
  for i in order_list():
    if order_quantity(i) > 0:
      cancel_buy_order(i)
    else:
      cancel_sell_order(i)


# Get the the data for 24 hours period
def data_fetcher(stock_name):
  # fetch the data from binance
  crypto = client.futures_klines(symbol=stock_name,
                                 interval=client.KLINE_INTERVAL_5MINUTE,
                                 limit=308)

  # Make columns names
  columns = [
    'datetime', 'open', 'high', 'low', 'close', 'volume', 'close time',
    'quote asset volume', 'number of trade', 'taker buy base', 'taker buy',
    'ignore'
  ]

  # Convert the data into dataframe
  df = pd.DataFrame(crypto, columns=columns)

  # Convert datetime columns as datetime type
  df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

  # Convert OHLC columns into float
  df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low',
                                             'close']].astype(float)

  # set datetime column as index
  df = df.set_index('datetime')

  # Convert Timezones
  df = df.tz_localize(pytz.timezone('UTC'))
  df.index = df.index.tz_convert('Asia/Jakarta')

  # Reset dataframe index
  df = df.reset_index()

  # Remove the timezone stamp
  df['datetime'] = df['datetime'].dt.tz_localize(None)

  #Drop unnecessary columns
  df = df.drop([
    'volume', 'close time', 'quote asset volume', 'number of trade',
    'taker buy base', 'taker buy', 'ignore'
  ],
               axis=1)

  # set datetime column as index
  df = df.set_index('datetime')

  # Make ema indicator columns
  df['ema'] = ta.EMA(df['close'], 9)

  # Make ma indicator columns
  df['ma'] = ta.MA(df['close'], 20)

  # Make Parabolic SAR indicator columns
  df['sar'] = ta.SAR(df['high'], df['low'], acceleration=0.02, maximum=0.2)

  # Remove the first 20 columns with no ema, ma, & calc
  df = df.iloc[20:]

  return df
