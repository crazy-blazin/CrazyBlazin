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



for l in range(0, 1):
    price = [20, 10, 200]
    tot = 0
    for i in range(1, 5000):
        #x = np.sin(i*0.05) + np.random.normal(7, 2)
        x = 450 + 0.3*price[-1] - 0.2*price[-2] + 0.4*price[-3] + np.random.normal(0, 250)
        price.append(x)
        if x <= 0:
            tot += 1
        # if price[-1] <= 0:
        #     price[-1] = 1


    plt.plot(price)
print(tot/5)
print(np.mean(price))
print(np.std(price))
plt.show()


# print((7 - 2)*100)

# from riotwatcher import LolWatcher, ApiError

# lol_watcher = LolWatcher('<your-api-key>')

# my_region = 'na1'

# me = lol_watcher.summoner.by_name(my_region, 'pseudonym117')
# print(me)

# # all objects are returned (by default) as a dict
# # lets see if i got diamond yet (i probably didnt)
# my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
# print(my_ranked_stats)

# # First we get the latest version of the game from data dragon
# versions = lol_watcher.data_dragon.versions_for_region(my_region)
# champions_version = versions['n']['champion']

# # Lets get some champions
# current_champ_list = lol_watcher.data_dragon.champions(champions_version)
# print(current_champ_list)

# # For Riot's API, the 404 status code indicates that the requested data wasn't found and
# # should be expected to occur in normal operation, as in the case of a an
# # invalid summoner name, match ID, etc.
# #
# # The 429 status code indicates that the user has sent too many requests
# # in a given amount of time ("rate limiting").

# try:
#     response = lol_watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
# except ApiError as err:
#     if err.response.status_code == 429:
#         print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
#         print('this retry-after is handled by default by the RiotWatcher library')
#         print('future requests wait until the retry-after time passes')
#     elif err.response.status_code == 404:
#         print('Summoner with that ridiculous name not found.')
#     else:
#         raise