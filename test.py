# from riotwatcher import LolWatcher

# key = "RGAPI-9e29ac1b-8163-4d0a-a119-b086692403d0"

# watcher = LolWatcher(key)

# def printstats(summonername):
#     summoner = watcher.summoner.by_name('euw1', summonername)
#     recentmatchlists = watcher.match.matchlist_by_account_recent ('euw1', "Foxxravin" ['accountId'])
#     print(recentmatchlists)


# printstats("Foxxravin")




from riotwatcher import LolWatcher

key = ""
summonername = "Foxxravin"
region = "euw1"


watcher = LolWatcher(key)


my_region = region
#My region
summoner = watcher.summoner.by_name(my_region, summonername)
stats = watcher.league.by_summoner(my_region, summoner['id'])

print(summoner['id'])


print(stats)

wins = 0
loss = 0
for i, stat in enumerate(stats):
    wins += int(stats[i]['wins'])
    loss += int(stats[i]['losses'])
print(wins)
print(loss)



recentmatchlists = watcher.match.matchlist_by_account(my_region, summoner['id']) #Get a list of data for the last 20 games


print(recentmatchlists)