# Importing functions

# Report exectution on telegram
from notifications import telegram_send

# Countdown timer 
from timer import countdown

# USDT paired stock list
from binance_client import stock_list

# Data fetcher from binance
from binance_client import data_fetcher

# Make Buy order 
from binance_client import buy_order

# Make stop loss order on  Buy order
from binance_client import buy_stop_loss

# Make take profit order on Buy order
from binance_client import buy_take_profit

# Make Sell order 
from binance_client import sell_order

# Make stop loss order on Sell order
from binance_client import sell_stop_loss

# Make take profit order on Sell order
from binance_client import sell_take_profit

# Remove warning
import warnings
warnings.filterwarnings('ignore')

# Program looping
while True:
  try:
    for x in stock_list():
      # Varible for the stock name 
      symbol = x
      
      # fetch the data from binance
      data = data_fetcher(symbol)
  
      # Variable for close, ema, ma, sar for 1st value from last
      val_1= data.iloc[-1]
      close_1 = val_1['close']
      open_1 = val_1['open']
      ema_1 = val_1['ema']
      ma_1 = val_1['ma']
      sar_1 = val_1['sar']
  
      # Variable for close, ema, ma, sar for 2st value from last
      val_2= data.iloc[-2]
      close_2 = val_2['close']
      open_2 = val_2['open']
      ema_2 = val_2['ema']
      ma_2 = val_2['ma']
      sar_2 = val_2['sar']
  
      # Variable for close, ema, ma, sar for 3st value from last
      val_3= data.iloc[-3]
      close_3 = val_3['close']
      open_3 = val_3['open']
      ema_3 = val_3['ema']
      ma_3 = val_3['ma']
      sar_3 = val_3['sar']
      
      # Quantile variable of the data
      q0 = float(data['ma'].quantile([0]))
      q1 = float(data['ma'].quantile([0.25]))
      q2 = float(data['ma'].quantile([0.5]))
      q3 = float(data['ma'].quantile([0.75]))
      q4 = float(data['ma'].quantile([1]))
      data_mean = float(data['ma'].mean())
      
      # Range of each quantiles  
      q1bd = ma_1 <= q1 + (q1*0.1) and ma_1 >= q1 - (q1*0.1)
      q0bd = ma_1 <= q0 + (q0*0.1) and ma_1 >= q0 - (q0*0.1)
      q3bd = ma_1 <= q3 + (q3*0.1) and ma_1 >= q3 - (q3*0.1)
      q4bd = ma_1 <= q4 + (q4*0.1) and ma_1 >= q4 - (q4*0.1)
  
      # Buy function 1
      def buy1():
          if (ma_3 > ema_3 > sar_3 and
            ma_2 > ema_2 > sar_2 and
            close_1 > ema_1 > ma_1 > sar_1 and
            (((close_1 - sar_1)/close_1)*100) > 0.5):
              return True
          else:
              return False
  
      # Buy function 2
      def buy2():
          if (sar_3 > ema_3 and
            sar_2 > ema_2 and
            ema_1 > sar_1 and
            (((close_1 - sar_1)/close_1)*100) > 0.75):
              return True
          else:
              return False
      
      # Buy confrim function
      def tx_confirm():
          if (q0bd and
              q1bd and
              q3bd and
              q4bd == True):
              return True
          else:
            return False
  
      # Sell function 1
      def sell1():
          if (sar_3 > ema_3 > ma_3 and
            sar_2 > ema_2 > ma_2 and
            sar_1 > ma_1 > ema_1 > close_1 and
            (((sar_1 - close_1)/sar_1)*100) > 0.5):
              return True
          else:
              return False
  
      # Sell function 2
      def sell2():
          if (ema_3 > sar_3 and
            ema_2 > sar_2 and
            sar_1 > ema_1 and
            (((sar_1 - close_1)/sar_1)*100) > 0.75):
              return True
          else:
              return False
  
      if buy1() == True:
        print('Buy signal 1 for {}'.format(symbol)),
        print('Waiting for confirmation...'),
        countdown(150)
        buy_df = data_fetcher(symbol)
        if buy_df['ema'].iloc[-1] > ema_1 and tx_confirm() == True:
          while True:
            try:
              buy_order(symbol)
            except:
              print('Failed to put Stop Loss Order')
              print('Retrying...')
            else:
              break
          countdown(60),
          while True:
            try:
              buy_stop_loss(symbol)
            except:
              print('Failed to put Stop Loss Order')
              print('Retrying...')
            else:
              break
          while True:
            try:
              buy_take_profit(symbol)
            except:
              print('Failed to put Take Profit Order')
              print('Retrying...')
            else:
              break
          telegram_send('Signal confirm, {} BUY LONG NOW !!!'.format(symbol)),
          print('Buying {}'.format(symbol))
        else:
          print('Signal not confirm')
      elif buy2() == True:
        print('Buy signal 2 for {}'.format(symbol)),
        print('Waiting for confirmation...'),
        countdown(150)
        buy_df = data_fetcher(symbol)
        if buy_df['ema'].iloc[-1] > ema_1 and tx_confirm() == True:
          while True:
            try:
              buy_order(symbol)
            except:
              print('Failed to put Stop Loss Order')
              print('Retrying...')
            else:
              break
          countdown(60),
          while True:
            try:
              buy_stop_loss(symbol)
            except:
              print('Failed to put Stop Loss Order')
              print('Retrying...')
            else:
              break
          while True:
            try:
              buy_take_profit(symbol)
            except:
              print('Failed to put Take Profit Order')
              print('Retrying...')
            else:
              break
          telegram_send('Signal confirm, {} BUY LONG NOW !!!'.format(symbol)),
          print('Buying {}'.format(symbol))
        else:
          print('Signal not confirm')
      elif sell1() == True:
        print('Sell signal 1 for {}'.format(symbol)),
        print('Waiting for confirmation...'),
        countdown(150)
        sell_df = data_fetcher(symbol)
        if sell_df['ema'].iloc[-1] < ema_1 and tx_confirm() == True:
          while True:
            try:
              sell_order(symbol)
            except:
              print('Failed to put Stop Loss Order')
              print('Retrying...')
            else:
              break
          countdown(60),
          while True:
            try:
              sell_stop_loss(symbol)
            except:
              print('Failed to put Stop Loss Order')
              print('Retrying...')
            else:
              break
          while True:
            try:
              sell_take_profit(symbol)
            except:
              print('Failed to put Take Profit Order')
              print('Retrying...')
            else:
              break
          telegram_send('Signal confirm, {} BUY SHORT NOW !!!'.format(symbol)),
          print('Selling {}'.format(symbol))
        else:
          print('Signal not confirm')
      elif sell2() == True:
        print('Sell signal 2 {}'.format(symbol)),
        print('Waiting for confirmation...'),
        countdown(150)
        sell_df = data_fetcher(symbol)
        if sell_df['ema'].iloc[-1] < ema_1 and tx_confirm() == True:
          while True:
            try:
              sell_order(symbol)
            except:
              print('Failed to put Stop Loss Order')
              print('Retrying...')
            else:
              break
          countdown(60),
          while True:
            try:
              sell_stop_loss(symbol)
            except:
              print('Failed to put Stop Loss Order')
              print('Retrying...')
            else:
              break
          while True:
            try:
              sell_take_profit(symbol)
            except:
              print('Failed to put Take Profit Order')
              print('Retrying...')
            else:
              break
          telegram_send('Signal confirm, {} BUY SHORT NOW !!!'.format(symbol)),
          print('Selling {}'.format(symbol))
        else:
          print('Signal not confirm')
      else:
        print('Scanning {} is done'.format(symbol))
  except:
    print('Process Failed')
    print('Retrying...')
  else:
    pass