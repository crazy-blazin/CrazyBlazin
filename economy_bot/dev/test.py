from weakref import KeyedRef
import matplotlib.pyplot as plt
import numpy as np

# a = {}
# try:
#     a['rww'] += 1
# except KeyError as msg:
#     print(KeyError)


# x = np.random.normal(1,10, 1000)

# plt.hist(x , bins = 100)
# plt.show()



for l in range(0, 10):
    price = [53]
    for i in range(1, 1000):
        price.append(0.1 + price[-1] + np.random.normal(0, 5))
        # if price[-1] <= 0:
        #     price[-1] = 1


    plt.plot(price)
plt.show()


# from pantheon import pantheon
# import asyncio

# server = "euw1"
# api_key = "RGAPI-XXXX"

# def requestsLog(url, status, headers):
#     print(url)
#     print(status)
#     print(headers)

# panth = pantheon.Pantheon(server, api_key, errorHandling=True, requestsLoggingFunction=requestsLog, debug=True)

# async def getSummonerId(name):
#     try:
#         data = await panth.getSummonerByName(name)
#         return (data['id'],data['accountId'])
#     except Exception as e:
#         print(e)


# async def getRecentMatchlist(accountId):
#     try:
#         data = await panth.getMatchlist(accountId, params={"endIndex":10})
#         return data
#     except Exception as e:
#         print(e)

# async def getRecentMatches(accountId):
#     try:
#         matchlist = await getRecentMatchlist(accountId)
#         tasks = [panth.getMatch(match['gameId']) for match in matchlist['matches']]
#         return await asyncio.gather(*tasks)
#     except Exception as e:
#         print(e)


# name = "Canisback"

# loop = asyncio.get_event_loop()  

# (summonerId, accountId) = loop.run_until_complete(getSummonerId(name))
# print(summonerId)
# print(accountId)
# print(loop.run_until_complete(getRecentMatches(accountId)))