
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
import logging





# logging.basicConfig(filename='main.log', level=logging.DEBUG)

sio = socketio.Client()



with open('musicdatabase.txt', 'r') as f:
    musicdatabase = eval(f.read())


with open('musicdatabase.txt', 'r') as f:
    musicdatabase = eval(f.read())

def run():
    sio.connect('http://127.0.0.1:5000', wait = True)
    while True:
        with open('musicdatabase.txt', 'r') as f:
            musicdatabase = eval(f.read())
        ordered = {}
        final = []
        for music in musicdatabase:
            if 'upvotes' in musicdatabase[music]:
                ordered[music] = len(musicdatabase[music]['upvotes'])
        for link in sorted(ordered, key=ordered.get, reverse=True):
            final.append([link, ordered[link], musicdatabase[link]['added_by']])
        sio.emit('msg', final)
        sio.sleep(3)

sio.start_background_task(target = run)


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
                try:
                    channelid = str(state.channel.id)
                except:
                    channelid = str(0)
                channel_state = str(state.channel)
                stream_state = state.self_stream
                if channel_state != 'None':
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
async def on_reaction_add(reaction, user):
    if str(reaction.message.channel.id) == str(802515211348213760):
        if reaction.emoji == '💥':
            with open('musicdatabase.txt', 'r') as f:
                musicdatabase = eval(f.read())
            if reaction.message.content in musicdatabase:
                musicdatabase[reaction.message.content]['upvotes'].append(reaction.message.author.name)
            
            with open('musicdatabase.txt', 'w') as f:
                f.write(str(musicdatabase))


@client.event
async def on_reaction_remove(reaction, user):
    if str(reaction.message.channel.id) == str(802515211348213760):
        if reaction.emoji == '💥':
            with open('musicdatabase.txt', 'r') as f:
                musicdatabase = eval(f.read())
            if reaction.message.content in musicdatabase:
                if reaction.message.author.name in musicdatabase[reaction.message.content]['upvotes']:
                    musicdatabase[reaction.message.content]['upvotes'].remove(reaction.message.author.name)
            with open('musicdatabase.txt', 'w') as f:
                f.write(str(musicdatabase))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str(message.channel.id) == str(802515211348213760):
        with open('musicdatabase.txt', 'r') as f:
            musicdatabase = eval(f.read())
        if str(message.content) not in musicdatabase:
            musicdatabase[message.content] = {}
            musicdatabase[message.content]['upvotes'] = []
            musicdatabase[message.content]['added_by'] = message.author.name
        with open('musicdatabase.txt', 'w') as f:
            f.write(str(musicdatabase))
    
    if message.content.startswith('!bal'):
        value = database[message.author.name]['coins']
        if 'shekels' in database[message.author.name]:
            shekval = database[message.author.name]['shekels']
        else:
            shekval = 100
            database[message.author.name]['shekels'] = shekval
        embed = discord.Embed(title=f"Balance", description=f"{message.author.name} current balance") #,color=Hex code

        embed.add_field(name=f"Crazy Blazin Coins", value=f'{round(value,2)} <:CBCcoin:831506214659293214>')
        embed.add_field(name=f"Sheqalim", value=f'{round(shekval,2)} ₪')
        await message.channel.send(embed=embed)

client.run(k)