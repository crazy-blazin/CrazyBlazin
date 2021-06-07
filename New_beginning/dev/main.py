
import os
from web.server import stonk_values
import matplotlib.pyplot as plt
import numpy as np
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import time
import threading
from discord.utils import get
from collections import Counter
import asyncio
from discord.ext import tasks
import datetime
import socketio
import uuid


class Stonk:
    all_stonks = []
    def __init__(self, name, init_value = 5, meanval= 0,  variance = 5, drift = 1.1):
        self.id = str(uuid.uuid1())
        self.name = name
        self.variance = variance
        self.mean = meanval
        self.drift = drift
        self.current_price = init_value
        self.y = [init_value]
        self.x = [1]
        self.all_stonks.append(self)
        self.onehourdifference = round(np.random.normal(0, 5), 2)


    def get_info(self):
        info = {'id': self.id,
                'name': self.name,
                'y': self.y,
                'x': self.x,
                'current_price': self.current_price,
                'onehourdifference': self.onehourdifference}
        return info

    
    def move_stonks(self):
        y = round(self.drift + self.y[-1] + np.random.normal(self.mean, self.variance),2)
        if len(self.y) < 120:
            onehourindex = 0
        else:
            onehourindex = -120
        self.onehourdifference = round(((y - self.y[onehourindex])/( 0.000001 + self.y[onehourindex]))*100, 2)
        self.y.append(y)
        self.y = self.y[-1000:]
        self.x.append(self.x[-1]+1)
        self.x = self.x[-1000:]
        self.current_price = self.y[-1]

    @staticmethod
    def get_all_stonks_info():
        all_stonks_info = []
        for stonk in Stonk.all_stonks:
            all_stonks_info.append(stonk.get_info())
        return all_stonks_info



class Consumables:
    def __init__(self, name = 'Test'):
        pass


class Items:
    index = 0
    def __init__(self, name = 'Test', cost = 100, dmg = 0, health_regen = 1, armor = 0, income = 0):
        self.index += 1
        self.cost = cost
        self.name = name
        self.dmg = dmg
        self.coinpertick = dmg
        self.health_regen = health_regen
        self.armor = armor
        self.income = income



class Users:
    all_users = []
    def __init__(self, name = '', max_health = 150,  health = 100, armor = 1, dmg = 2, faction = '', coinpertick = 2) -> None:
        self.name = name
        self.maxhealth = max_health
        self.maxtickets = 20
        self.health = health
        self.health_regen = 0
        self.armor = armor
        self.dmg = dmg
        self.coins = 0
        self.total_income = 0
        self.faction = faction
        self.coinpertick = coinpertick
        self.items = []
        self.tickets = 0
        self.all_users.append(self)


    def add_items(self, item):
        self.items.append(item)

    
    @staticmethod
    def tick():
        for user in Users.all_users:
            user.coinpertick = 0
            user.health_regen = 0
            for item in user.items:
                user.coinpertick += item.income
                user.health_regen += item.health_regen
                user.dmg += item.health_regen
                user.coins += item.coinpertick
            
            health = user.health + user.health_regen
            if health >= user.maxhealth:
                user.health = user.maxhealth
            else:
                user.health += user.health_regen
            
            tickets = user.tickets + 1
            if tickets >= user.maxtickets:
                user.tickets = user.maxtickets
            else:
                user.tickets += 1


class Faction:
    all_factions = []
    index = 0
    def __init__(self, name = 'Test', maxhealth = 1000, health = 0, armor = 0, health_regen = 0):
        self.index += 1
        self.name = name
        self.health = health
        self.maxhealth = maxhealth
        self.tickets = 0
        self.maxtickets = 30
        self.health_regen = health_regen
        self.armor = armor
        self.coins = 0
        self.members = []
        self.all_factions.append(self)
    
    @staticmethod
    def tick():
        for faction in Faction.all_factions:
            health = 0
            faction.armor = 0
            faction.health_regen = 0
            for user in faction.all_users:
                faction.armor += user.armor
                faction.health_regen += user.health_regen

            health = faction.health + faction.health_regen
            if health >= faction.maxhealth:
                faction.health = faction.maxhealth
            else:
                faction.health += faction.health_regen
            
            tickets = faction.tickets + 1
            if tickets >= faction.maxtickets:
                faction.tickets = faction.maxtickets
            else:
                faction.tickets += 1
    
    def add_members(self, member):
        self.members.append(member)



The_high_council = Faction(name = 'The High Council')
The_resistance = Faction(name = 'The Resistance')



Users()
print(Users.all_users)


Stonk('Ak47 Factory', init_value = 5, meanval = 0,  variance = 5, drift = 0.1)
Stonk('Real estate GRUNMORS', init_value = 100, meanval= 0,  variance = 50, drift = 1.1)
Stonk('Spellfrik', init_value = 50, meanval = 0,  variance = 1, drift = 0.5)


sio = socketio.Client()
sio.connect('http://127.0.0.1:5000')

while True:
    for stonk in Stonk.all_stonks:
        stonk.move_stonks()
    sio.emit('stonk_values', Stonk.get_all_stonks_info())
    time.sleep(7)

