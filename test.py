from numpy import int64
import pandas as pd
import yfinance as yf

data = yf.Ticker(str("msft").upper())
query = data.history(interval='1m', period='1d')

timestamps = list(pd.to_datetime(query.index).astype(int64) // 10**9)
prices = list(pd.DataFrame(query)["Open"])
graphData = [timestamps, prices]