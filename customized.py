import pandas as pd
from binance_client import client

# Calling for account balance
def my_balance():
  data_balance = client.futures_account_balance()
  balance = pd.DataFrame(data_balance)
  balance = balance.drop(['updateTime'], axis = 1)
  balance = balance.set_index('asset')
  balance = balance['balance']['USDT']
  balance = round(float(balance),2)
  return balance

# Calling for account balance string
def my_balance_string():
  data_balance = client.futures_account_balance()
  balance = pd.DataFrame(data_balance)
  balance = balance.drop(['updateTime'], axis = 1)
  balance = balance.set_index('asset')
  balance = balance['balance']['USDT']
  balance = str(round(float(balance),2)) + "USDT"
  return balance

# Account balance 
mybalance = my_balance()

# Captial per trade
caps = round(float(mybalance/12.76),2) # float capital number number

# Profit percentage per trade 
profit_percent = 66 # change this
take_profit = round(float(profit_percent / 100),1)