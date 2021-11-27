#!/usr/bin/env python
from asyncio.tasks import wait
import os
from discord import voice_client
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
from datetime import date
import asyncio 
# OS modules
import os
import shutil

# Image modules
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw, ImageSequence
import subprocess
import audioread
import tempfile
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import pickle
from PIL import Image



with open('version.txt', 'r') as f:
    version = float(f.read())
    print(version)

with open('../key.txt', 'r') as f:
    k = str(f.read())


def check_version():
    global version
    with open('version.txt', 'r') as f:
        ver = float(f.read())
    if version != ver:
        os._exit(0)

def read_db():
    try:
        with open('../database.txt', 'r') as f:
            database = eval(f.read())
        return database
    except:
        print('read error')


def read_rewards():
    try:
        with open('rewards.txt', 'r') as f:
            rewards = eval(f.read())
        return rewards
    except:
        print('read error')

def write_db(database):
    try:
        with open('../database.txt', 'w', encoding='utf-8') as f:
            f.write(str(database))
    except:
        print('write error')



temp_status  = {}
database = read_db()
rewards = read_rewards()
        
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        global temp_status
        global database
        members = client.get_all_members()
        # database = read_db()
        for member in members:
            if member.name in database:
                temp_status[member.name] = member.voice
                role_names = [role.name for role in member.roles]
                if 'Bots' in role_names:
                    print(member.name)
                    database.pop(member.name, None)
                    temp_status.pop(member.name, None)
        

        with open('version.txt', 'r') as f:
            bot_version = float(f.read())
        # SEND TO PATCH LOG CHANNEL
        with open('patchnotes.txt', 'r', encoding='utf-8') as f:
            patchnotes = f.read()
        patchchannel = client.get_channel(831638592106921994)
        embed = discord.Embed(title=f"Crazy Blazin bot patch notes", description=f"Build {bot_version} patch notes.") #,color=Hex code
        embed.add_field(name=f"Patch notes:", value=f'{patchnotes}')
        await patchchannel.send(embed=embed)
        write_db(database)


        # members = self.get_all_members()
        # for member in members:
        #     role_names = [role.name for role in member.roles]
        #     if member.name not in database:
        #         role_names = [role.name for role in member.roles]
        #         if 'Bots' in role_names:
        #             pass
        #         else:
        #             database[member.name] = {'coins': 10}


# sio = socketio.Client()


intents = discord.Intents.default()
intents.members = True
client = MyClient(intents = intents)



def add_coins(stream_state, user, cointype):
    global database
    if stream_state:
        if cointype in database[user]:
            database[user][cointype] = round(database[user][cointype] + 1, 2)
        else:
            database[user][cointype] =  10
    else:
        if cointype in database[user]:
            database[user][cointype] = round(database[user][cointype] + 0.33, 2)
        else:
            database[user][cointype] =  10
    print(f'Coins to : {user}')
    write_db(database)


async def ticksystem():
    while True:
        global temp_status
        # database = read_db()
        global database
        write_db(database)

        for user in database:
            if user in temp_status:
                state = temp_status[user]
                if state != None:

                    if state.channel != None:
                        channelid = str(state.channel.id)
                        stream_state = state.self_stream
                        if channelid != 'None':
                            add_coins(stream_state, user, 'coins')

                    else:
                        channelid = str(0)

            write_db(database)
        await asyncio.sleep(10)


# async def timer():
#     await client.wait_until_ready()
#  await asyncio.sleep(4)
        

client.loop.create_task(ticksystem())
# client.loop.create_task(timer())


@client.event
async def on_voice_state_update(member, before, after):
    global temp_status
    global database
    role_names = [role.name for role in member.guild.roles]
    if member.name not in database and 'Bots' not in role_names:
        database[member.name] = {'coins': 10}
        database[member.name]['rewards'] = {}
        write_db(database)
    

    temp_status[member.name] = after

        # if 'Timer' in database[member.name]:
        #     curr_timer = database[member.name]['Timer']
        #     role_names = [role.name for role in member.guild.roles]
        #     if curr_timer <= 0 and 'Crazy Blazin Gold' in role_names:
        #         role = get(member.guild.roles, name='Crazy Blazin Gold')
        #         await member.remove_roles(role)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global database
    global rewards

    members = client.get_all_members()
    for member in members:
        if member.name not in database:
            role_names = [role.name for role in member.roles]
            if 'Bots' not in role_names:
                database[member.name] = {}
                database[member.name]['coins'] = 10
                database[member.name]['rewards'] = {}
    write_db(database)


    if message.content.startswith('!bal'):
        value = database[message.author.name]['coins']
        embed = discord.Embed(title=f"Balance", description=f"{message.author.name} current balance") #,color=Hex code
        embed.add_field(name=f"Crazy Blazin Coins", value=f'{round(value,2)} <:CBCcoin:831506214659293214>')
        await message.channel.send(embed=embed)


    if message.content.startswith('!myrewards'):
        rewards_user = database[message.author.name]['rewards']
        embed = discord.Embed(title=f"Rewards", description=f"{message.author.name} current rewards") #,color=Hex code
        for reward in rewards_user:
            embed.add_field(name=f"{reward}", value=f'{rewards[reward][0]}')
        await message.channel.send(embed=embed)


    if message.content.startswith('!rewardhelp'):

        embed = discord.Embed(title=f"Rewards", description=f"Current rewards") #,color=Hex code
        for reward in rewards:
            embed.add_field(name=f"{reward} {rewards[reward][0]}", value=f'{rewards[reward][1]}')
        await message.channel.send(embed=embed)


    if message.content.startswith('!top'):
            temp_stats  = {}
            for user in database:
                coins = database[user]['coins']
                temp_stats[user] = round(coins,2)
            index = 1
            embed = discord.Embed(title="Top coins history", description="Users that have had the most coins ever") #,color=Hex code
            medaljonger = [':crown:', ':second_place:', ':third_place:']
            for key in sorted(temp_stats, key=temp_stats.get, reverse=True):
                if (index < 11) and index < len(temp_stats):
                    if index < 4:
                        embed.add_field(name=f"{index}{medaljonger[index-1]}. {key}", value=f'{temp_stats[key]} <:CBCcoin:831506214659293214>')
                    else:
                        embed.add_field(name=f"{index}. {key}", value=f'{temp_stats[key]} <:CBCcoin:831506214659293214>')
                else:
                    await message.channel.send(embed=embed)
                    return
                index += 1

    if message.content.startswith('!givereward'):
        str_split = message.content.split(' ')
        if len(str_split) > 3 or len(str_split) < 3:
            await message.channel.send(f'Too many or few arguments. Use !givereward <target> <reward>')
        reward = str(str_split[2])
        target = str_split[1]
        role_names = [role.name for role in message.author.roles]
        if 'Admin' in role_names or 'Server: Mod' in role_names:
            if target in database:
                if reward in rewards:
                    if reward in database[target]['rewards']:
                        database[target]['rewards'][reward] += 1
                    else:
                        database[target]['rewards'][reward] = 1
                    write_db(database)
                    await message.channel.send(f'{message.author.name} added {reward} {rewards[reward][0]} to {target}.')
                else:
                    await message.channel.send(f'Reward does not exist!')
        else:
            await message.channel.send(f'You are not admin or moderator!')
    

    if message.content.startswith('!changetime'):
        str_split = message.content.split(' ')
        if message.author.name == 'Foxxravin':
            time = str_split[1]
            global hour_cumww
            hour_cumww = int(time)

            await message.channel.send(f'Changed cum ww time to: {hour_cumww}')
        else:
            await message.channel.send(f'You are not Foxxravin!')


    
    # if message.content.startswith('!buy gold'):
        
    #     str_split = message.content.split(' ')
    #     if len(str_split) > 2 or len(str_split) < 2:
    #         await message.channel.send(f'Too many or few arguments. Use !buy gold')
    #     else:
    #         # database = read_db()
    #         if 1000 <= database[message.author.name]['coins']:
    #             database[message.author.name]['coins'] -= 1000

    #             member = message.author
    #             role = get(member.guild.roles, name='Crazy Blazin Gold')
    #             await member.add_roles(role)
    #             # await bot.remove_roles(user, 'member')
    #             await message.channel.send(f'{message.author.name} Bought Crazy Blazin Gold Role for one month!')

    #             database[message.author.name]['Timer'] = 2592000
    #             write_db(database)

    #         else:
    #             await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC) to buy Crazy Blazin Gold! Price: 1000 <:CBCcoin:831506214659293214> (CBC)')
    


    if message.content.startswith('!help'):
        # helps commands
        embed = discord.Embed(title=f"Commands", description=f"All commands for crazy blazin server")
        embed.add_field(name=f"Balance", value=f'!bal')
        embed.add_field(name=f"Give rewards MUST BE ADMIN OR MOD", value=f'!givereward <username> <name of award>')
        embed.add_field(name=f"View all the rewards and their description", value=f'!rewardhelp')
        embed.add_field(name=f"View toplist for the members with the most coins", value=f'!top')
        embed.add_field(name=f"View all your current rewards", value=f'!myrewards')
        await message.channel.send(embed=embed)

    


    write_db(database)


client.run(k)