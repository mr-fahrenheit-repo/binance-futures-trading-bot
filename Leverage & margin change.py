from binance_client import leverage_change
from binance_client import change_margin
from binance_client import stock_list

# Change Leverage to the highest for every pairs
for x in stock_list():
  leverage_change(x)
  
# Change Margin type to Isolated
for x in stock_list():
  change_margin(x)