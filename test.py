import yfinance as yf
while True:
    for x in ['tsla']:
        query = yf.Ticker(str(x).upper()).history(interval='1m', period='1d')
        # symbol = yf.Ticker(str(x).upper()).info()['currency']
        data = [
            # symbol,
            round(query['Close'][-1], 2), # current price
            round((query['Close'][-1] - query['Close'][-2]), 2), # price change
            round(((query['Close'][-1] - query['Close'][-2])/query['Close'][-2])*100, 2), # price change %
            query['Volume'][-1], # volume
        ]
        print(data)