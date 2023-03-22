from utils import cleanTickerList
import csv

tickerData = {} #{ticker1: [data1, data2....., data4], ticker2: []....., tickerN:[]}
userData = {} #{user1:[ticker1, ticker2..., tickerN], user2:[ticker1, ticker2..., tickerN]}

async def addUser(sio, sid):
    if(sid not in userData.keys()):
        userData[sid] = []
    print(sid, "connected")

async def removeUser(sio, sid):
    userData.pop(sid)
    cleanTickerList(userData, tickerData)
    print(sid, "disconnected")

def addTicker(sid, ticker):
    loadCSV()
    for x in ticker["tickers"]:
        if(x not in userData[sid]):
            if(len(userData[sid]) == 0):
                userData[sid] = [x]
            else:
                userData[sid].append(x)
            tickerData[x] = ["NA"]*4
    writeToCSV(tickerData)


# FIX THE ISSUE WHERE REMOVING 1 TICKER 
# > > > WIPES < < < THE ENTIRE DATA.CSV FOLE SOBBBBBB
def removeTicker(sid, ticker):
    tickerData = loadCSV()
    if(ticker["tickers"] in userData[sid]):
        userData[sid].remove(ticker["tickers"])
    cleanTickerList(userData, tickerData)
    writeToCSV(tickerData)

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

def getUserData():
    return [userData]