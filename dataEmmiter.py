import csv
from dataWriter import getUserData

tempStreamData = {}

async def emitStockData(sio): # emits data for each client indivisually
    while True:
        userData = getUserData()[0]
        tickerData = loadCSV()
        for x in userData.keys():
            streamData = {}

            # for each ticker for a specific user
            for ticker in userData[x]:
                # get data for that ticker
                data = tickerData[ticker]
                if("NA" not in data): #check if ticker has no data, only then add it to stream data that is to be emitted
                    streamData[ticker] = data

            # check if data is repeating, ont send it if it is to avoid unnecesarry bandwidth usage
            if((x not in tempStreamData.keys()) or 
               (x in tempStreamData.keys() and tempStreamData[x] != streamData)): 
                tempStreamData[x] = streamData
                await sio.emit("tickerStream", streamData, room=str(x)) # emit streamdata to user with id "x"
                await sio.sleep(0.3) #sleep for 0.3 sec between indivisual user emit
            else:
                print("recurring data")
        await sio.sleep(3) # sleep for 3 sec between all user emit loop

# async def emitStockData(sio): # emits data for each ticker indivisually 
#     # (more efficient in terms of server load and update rate)
#     tickerData = {}
#     while True:
#         newtickerData = loadCSV()
#         for x in newtickerData.keys():
#             if((x not in tickerData.keys()) or (x in tickerData.keys() and newtickerData[x] != tickerData[x])):
#                 tickerData[x] = newtickerData[x]
#                 await sio.emit(str(x), tickerData[x]) # emit tickerdata with event name x (the stock ticker)
#                 await sio.sleep(0.05) #sleep for 0.3 sec between indivisual ticker emit
#         await sio.sleep(1) # sleep for 3 sec between the ticker emit loop

def loadCSV():
    with open("data.csv") as csvfile: 
        csvreader = csv.reader(csvfile)
        transformedData = {}
        for x in csvreader:
            transformedData[x[0]] = x[1:]
        return transformedData