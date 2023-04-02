import yfinance as yf
def getTickerInfo(ticker):
    query = yf.Ticker(str(ticker).upper()).history(interval='1m', period='1d') 
    
    # ^^^ gets data of a listed stock from the past day, intervals = 1 minute ^^^
    
    # symbol = yf.Ticker(str(ticker).upper()).fast_info['currency']
    data = None
    try:
        data = [
            # symbol,
            round(query['Close'][-1], 2), # current price   
            round((query['Close'][-1] - query['Close'][-2]), 2), # price change
            round(((query['Close'][-1] - query['Close'][-2])/query['Close'][-2])*100, 2), # price change %
            query['Volume'][-1], # volume
        ]
    except:
        data = None
    # print(data)
    return data

print(getTickerInfo("mssft"))