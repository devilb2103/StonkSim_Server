def getDictValuesUnion(d):
    x = [keys for keys in dict(d).values()]
    added = []
    for i in x:
        added += i
    added = set(added)
    return [x for x in added]

def cleanTickerList(userData, tickerData):
    remainingTickers = getDictValuesUnion(userData) #tickers that are needed by users
    toPopTickers = [] #tickers that are to be removed from fetchList

    # mark tickers that need to be removed
    for x in tickerData.keys():
        if(x not in remainingTickers):
            toPopTickers.append(x)

    # remove tickers that arent needed
    for x in toPopTickers:
        tickerData.pop(x)