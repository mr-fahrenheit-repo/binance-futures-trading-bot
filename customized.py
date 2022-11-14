from binance_client import my_balance

# Account balance 
mybalance = my_balance()

# Captial per trade
caps = round(float(mybalance/13.3333),2) # float capital number number

# Profit percentage per trade 
profit_percent = 66 # change this
take_profit = round(float(profit_percent / 100),1)