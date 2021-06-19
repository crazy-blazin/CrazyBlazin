
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



k = ''


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
                    database[member.name] = {'coins': 100}
        

intents = discord.Intents.default()
intents.members = True
client = MyClient(intents = intents)


temp_status  = {}

with open('database.txt', 'r') as f:
    database = eval(f.read())




def add_coins(stream_state, user, cointype):
    if stream_state:
        if cointype in database[user]:
            database[user][cointype] = round(database[user][cointype] + 1, 2)
        else:
            database[user][cointype] =  100
    else:
        if cointype in database[user]:
            database[user][cointype] = round(database[user][cointype] + 0.33, 2)
        else:
            database[user][cointype] =  100
    print(f'Coins to : {user}')


def ticksystem():
    while True:
        for user in database:
            if user in temp_status:
                state = temp_status[user]
                channelid = str(state.channel.id)
                channel_state = str(state.channel)
                stream_state = state.self_stream
                if channelid != str(847583212926009374):
                    add_coins(stream_state, user, 'coins')
                else:
                    add_coins(stream_state, user, 'shekels')
        with open('database.txt', 'w', encoding='utf-8') as f:
            f.write(str(database))
        time.sleep(10)

t = threading.Thread(target=ticksystem)
t.daemon = False
t.start()


@client.event
async def on_voice_state_update(member, before, after):
    if member.name not in database:
        database[member.name] = {'coins': 1000}
    temp_status[member.name] = after

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!bal'):
        value = database[message.author.name]['coins']
        if 'shekels' in database[message.author.name]:
            shekval = database[message.author.name]['shekels']
        else:
            shekval = 100
            database[message.author.name]['shekels'] = shekval
        embed = discord.Embed(title=f"Balance", description=f"{message.author.name} current balance") #,color=Hex code

        embed.add_field(name=f"Crazy Blazin Coins", value=f'{round(value,2)} <:CBCcoin:831506214659293214>')
        embed.add_field(name=f"Shekels", value=f'{round(shekval,2)} ₪')
        await message.channel.send(embed=embed)

client.run(k)