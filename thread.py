from time import sleep
from numpy import int64
import pandas as pd
import yfinance as yf
import csv

toDelist = {}

def getTickerInfo(ticker):
    query = None
    prevClose = None
    graphData = []
    try:
        data = yf.Ticker(str(ticker).upper())
        query = data.history(interval='1m', period='1d')
        
        timestamps = list(pd.to_datetime(query.index).view(int64) // 10**9)
        prices = list(pd.DataFrame(query)["Open"])
        graphData = [timestamps, prices]
        
        prevClose = data.fast_info["previousClose"]
        # ^^^ gets data of a listed stock from the past day, intervals = 1 minute ^^^
        if(type(prevClose) != float):
            prevClose = query['Close'][-2]
        
    except Exception as e:
        toDelist[ticker] = ""
        print(toDelist)
        print(e)

    # symbol = yf.Ticker(str(ticker).upper()).fast_info['currency']
    # print(query)
    data = None
    try:
        data = [
            # symbol,
            round(query['Close'][-1], 2), # current price
            round(query['Close'][-1] - prevClose, 2), # price change
            round(((query['Close'][-1] - prevClose)/prevClose)*100, 2), # price change %
            round(query['Open'][0], 2), # opening price
            round(query['Close'][0], 2), # Previous Closing Price
            round(query['Volume'][-2], 2), # Volume
            f"{round(query['Low'][0], 2)} - {round(query['High'][0], 2)}", # Daily Range,
            graphData
        ]
    except Exception as e:
        print(e)
        data = None
    return data

def loadCSV():
    with open("data.csv") as csvfile: 
        csvreader = csv.reader(csvfile)
        transformedData = {}
        for x in csvreader:
            transformedData[x[0]] = x[1:]
        return transformedData

def writeToCSV(data):
    lines = []
    for x in data.keys():
        transformedData = [x] + data[x]
        lines.append(transformedData)
    with open("data.csv", 'w', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(lines)

def thread():
    while True: # main thread program
        tickers = loadCSV() # first ticker load -----> 1
        for x in tickers.keys():
            fetchedData = getTickerInfo(str(x))
            if(fetchedData != None):
                tickers[x] = fetchedData # write data to each corresponding ticker in the array
        updatedTickers = loadCSV() # get ticker data updated AFTER tickers were loaded (Second ticker load -----> 2)
        finalTickers = {} # returned ticker list (final) thats to be written to csv
        # account for added / removed tickers
        # 1) added tickers
        for x in tickers.keys(): # add tickers with queried values that are present in the second ticker load (2)
            if((x in updatedTickers.keys()) and (x not in toDelist.keys())):
                finalTickers[x] = tickers[x]

        # 2) removed tickers
        for x in updatedTickers.keys(): # initialize tickers which were added newly in the second ticker load (2)
            if(x not in tickers.keys()):
                finalTickers[x] = ["NA"]*4

        writeToCSV(finalTickers) # write updated data to data.csv
        toDelist.clear()
        # print("update cycle completed") # debug
        sleep(1) # because yfinance api is rate limited (i think / hota h / chalta h / safe rehna h)