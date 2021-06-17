
from asyncio.tasks import wait
import os
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
import requests
from flask import jsonify



# stonklist = ['Weapon Factory', 'Real estate GRUNMORS', 'Spellfrik', 'Minekartellet uftevik', 'Bommulsprodusenten Øldal']

# for stonkname in stonklist:
#     drift = 0
#     var = np.random.randn()
#     var = var*np.sign(var)
#     Stonk(stonkname, init_value = np.random.randint(100, 150), meanval = 0,  variance = var, drift = drift)


# logging.basicConfig(filename='main.log', level=logging.DEBUG)

# sio = socketio.Client(logger=logging)



# def run():
#     sio.connect('http://127.0.0.1:5000', wait = True)
#     while True:
#         for stonk in Stonk.all_stonks:
#             stonk.move_stonks()
#         sio.emit('stonk_values', Stonk.get_all_stonks_info())
#         sio.sleep(5)

# sio.start_background_task(target = run)


with open('database.txt', 'r') as f:
    database = eval(f.read())


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        members = self.get_all_members()
        for member in members:
            role_names = [role.name for role in member.roles]
            if member.name not in database:
                role_names = [role.name for role in member.roles]
                if 'Bots' in role_names:
                    pass
                else:
                    database[member.name] = {'coins': 1000}
        

intents = discord.Intents.default()
intents.members = True
client = MyClient(intents = intents)


with open('database.txt', 'r') as f:
    database = eval(f.read())

def ticksystem():
    time.sleep(10)
    tmp = database
    for user in database:
        if 'status' in database[user]:
            state = database[user]['status']
            channel_state = str(state.channel)
            stream_state = state.self_stream
            if channel_state != 'None':
                if stream_state:
                    try:
                        database[user]['coins'] = round(database[user]['coins'] + 1, 2)
                    except KeyError as msg:
                        print(msg)
                        pass
                    print(f'Stream activity: {user}')
                else:
                    try:
                        database[user]['coins'] = round(database[user]['coins'] + 0.33, 2)
                    except KeyError as msg:
                        print(msg)
                        pass
                print(f'Coins to : {user}')
        else:
            pass
    tmp.pop('status', None)
    with open('database.txt', 'w') as f:
        f.write(str(tmp))
    ticksystem()

t = threading.Thread(target=ticksystem)
t.daemon = True
t.start()


@client.event
async def on_voice_state_update(member, before, after):
    if member.name not in database:
        database[member.name] = {'coins': 1000}
    database[member.name]['status'] = after
    print(database)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    

    if message.content.startswith('!bal'):
        value = database[message.author.name]['coins']
        embed = discord.Embed(title=f"Balance", description=f"{message.author.name} current balance") #,color=Hex code

        embed.add_field(name=f"<:CBCcoin:831506214659293214> (CBC)", value=f'{round(value,2)}')
        await message.channel.send(embed=embed)


client.run(k)