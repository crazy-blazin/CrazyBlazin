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
import datetime
from config import *

import card_game.cardsystem as cardsystem
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


MAIN_CARD_LOCK = True


cards_stats = {'light': {':shield:': [40, 'Defence'], ':drop_of_blood:': [5, 'Steal']}, 'evil': {':drop_of_blood:': [20, 'Steal'], ':shield:': [5, 'Defence']}, 'artifact': {':drop_of_blood:': [0, 'Steal'], ':shield:': [10, 'Defence'], ':coin:': [100, 'Gold']}  }



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

def write_read_cards_database(database):
    if database != None:
        try:
            with open('../cards_database.txt', 'w', encoding='utf-8') as f:
                f.write(str(database))
            return database
        except:
            print('write error')
    else:
        print('write error - voice database is none')

def read_rewards():
    try:
        with open('rewards.txt', 'r') as f:
            rewards = eval(f.read())
        return rewards
    except:
        print('read error')


def read_cards_database():
    try:
        with open('../cards_database.txt', 'r') as f:
            cards_database = eval(f.read())
        return cards_database
    except:
        print('read error')

def write_db(database):
    if database != None:
        try:
            with open('../database.txt', 'w', encoding='utf-8') as f:
                f.write(str(database))
        except:
            print('write error')
    else:
        print('write error - database is none')



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
        vc_channels = client.guilds[0].voice_channels
        voice_channels = list(vc_channels)
        cards_database_save = {}
        if not os.path.exists('../cards_database.txt'):
            with open('../cards_database.txt', 'w', encoding='utf-8') as f:
                for member in members:
                    cards_database_save[member.name] = {'cards': [], 'stats': {}}

                f.write(str(cards_database_save))
                cards_database = read_cards_database()

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

cards_database = read_cards_database()

def add_coins(stream_state, user, cointype):
    # add coins to user
    global database
    # vc_channels = client.guilds[0].voice_channels
    # voice_channels = list(vc_channels)
    # extra_earned = 0
    # for vc in voice_channels:
    #     all_members_in_vc = list(vc.members)
    #     tot_members = len(all_members_in_vc)
    #     if user in voice_channels_database[str(vc.id)]['users']:
    #         total_owned = voice_channels_database[str(vc.id)]["users"][user]['amount']
    #         percent_ownage = (total_owned / voice_channels_database[str(vc.id)]['stocks'])
    #         if user in all_members_in_vc:
    #             tot_members -= 1
    #             # pass
    #         extra_earned += percent_ownage * tot_members*20
    #         database[user][cointype] = round(database[user][cointype] + extra_earned, 5) 

    if stream_state:
        if cointype in database[user]:
            database[user][cointype] = round(database[user][cointype] + 3.5, 5)
        else:
            database[user][cointype] =  10
    else:
        if cointype in database[user]:
            database[user][cointype] = round(database[user][cointype] + 0.85, 5)
        else:
            database[user][cointype] =  10
    print(f'Coins to : {user}')
    write_db(database)



async def card_drawing(total_sentence, type__, username):
    styles = {'Steampunk': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[9]/div/div/img', 'Fantasy': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[8]/div/div/img', 'Synthwave': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[11]/div/div/img', 'Pastel': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[5]/div/div/img', 'Mystical': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/img', 'Ukiyoe': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[10]/div/div/img', 'Dark fantasy': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[3]/div/div/img', 'HD': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[6]/div/div/img', 'Festive': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div/div/img', 'Psychic': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[4]/div/div/img', 'Vibrant': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[7]/div/div/img'}
    global MAIN_CARD_LOCK
    global cards_stats
    stats_gained_text = {}
    stats_gained_image = {}
    if MAIN_CARD_LOCK:
        MAIN_CARD_LOCK = False
        if type__ == 'artifact':
            stl = styles['Steampunk']
        if type__ == 'evil':
            stl = styles['Dark fantasy']
        else:
            stl = styles['Mystical']
        path_to_card = cardsystem.do_card(total_sentence, type_ = type__ , style = stl)
        img = Image.open(path_to_card)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Roboto-Black.ttf", 30)
        # draw.text((x, y),"Sample Text",(r,g,b))
        if type__ in cards_stats:
            stats = cards_stats[type__]
            for i, stat in enumerate(stats):
                stats_value = int(stats[stat][0])
                if stats_value > 0:
                    stats_gained = np.random.randint(0, int(stats[stat][0]))
                    stats_gained_text[stats[stat][1]] = stats_gained
                    stats_gained_image[stat] = stats_gained
                else:
                    stats_gained_text[stats[stat][1]] = 0
                    stats_gained_image[stat] = 0
                draw.text((70*(1 + 3*i), 1800),f"{stats[stat][1]}: {stats_gained_text[stats[stat][1]]}",(255,255,255),font=font)
                
        # draw.text((70*4, 1800),"CBC steal: 50",(255,255,255),font=font)
        draw.text((70, 1860),f"Type: {type__}",(255,0,255),font=font)
        draw.text((300, 1860),f"Rarity: Common",(255,0,255),font=font)
        path = f'../cards/{uuid.uuid4()}.jpg'
        if username in database:
            if 'cards' in database[username]:
                database[username]['cards'][path] = stats_gained_image
        img.save(path)
        MAIN_CARD_LOCK = True
        return path


async def ticksystem():
    while True:
        global temp_status
        # database = read_db()
        global database

        print('tick')
        total_stats = {}
        members = client.get_all_members()
        for member in members:
            total_stats[member.name] = {}
            role_names = [role.name for role in member.roles]
            if 'Bots' not in role_names:
                if member.name in database:
                    if len(database[member.name]['cards']) > 0:
                        for card in database[member.name]['cards']:
                            for stat in database[member.name]['cards'][card]:
                                if stat not in total_stats[member.name]:
                                    total_stats[member.name][stat] = database[member.name]['cards'][card][stat]
                                else:
                                    total_stats[member.name][stat] += database[member.name]['cards'][card][stat]

                                database[member.name][stat] = total_stats[member.name][stat]

        write_db(database)
        for user in database:
            # try:
            #     vc_channels = client.guilds[0].voice_channels
            #     voice_channels = list(vc_channels)
            #     for vc in voice_channels:
            #         all_members_in_vc = list(vc.members)
            #         for member in all_members_in_vc:
            #             if member.name in database:
            #                 for member2 in database:
            #                     if member.name != member2:
                                        
            #     #     tot_members = len(all_members_in_vc)

            # except IndexError:
            #     pass

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


            # total_gained
            write_db(database)
        await asyncio.sleep(10)


# async def timer():
#     await client.wait_until_ready()
#  await asyncio.sleep(4)


client.loop.create_task(ticksystem())

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
    global cards_database

    members = client.get_all_members()
    for member in members:
        if member.name not in database:
            role_names = [role.name for role in member.roles]
            if 'Bots' not in role_names:
                database[member.name] = {}
                database[member.name]['coins'] = 10
                database[member.name]['rewards'] = {}
                database[member.name]['cards'] = {}
    write_db(database)


    if message.content.startswith('!bal'):
        value = database[message.author.name]['coins']
        embed = discord.Embed(title=f"Balance", description=f"{message.author.name} current balance") #,color=Hex code
        embed.add_field(name=f"Crazy Blazin Coins", value=f'{round(value,5)} <:CBCcoin:831506214659293214>')

        for stat in database[message.author.name]:
            if stat != 'coins' and stat != 'rewards' and stat != 'cards':
                embed.add_field(name=stat, value=f'{database[message.author.name][stat]}')

        await message.channel.send(embed=embed)


    # if message.content.startswith('!lookup'):
    #     str_split = message.content.split(' ')
    #     if len(str_split) > 2 or len(str_split) < 2:
    #         await message.channel.send(f'Too many or few arguments. Use !lookup <target>')
    #     else:
    #         target = str(str_split[1])
    #         if target in database:
    #             value = database[target]['coins']
    #             rewards_user = database[target]['rewards']
    #             embed = discord.Embed(title=f"User stats", description=f"{target} current balance") #,color=Hex code
    #             for reward in rewards_user:
    #                 embed.add_field(name=f"{reward}", value=f'{rewards[reward][0]}')
    #             embed.add_field(name=f"Crazy Blazin Coins", value=f'{round(value,2)} <:CBCcoin:831506214659293214>')
    #             for key in voice_channels_database:
    #                 if target in voice_channels_database[key]['users']:
    #                     total_owned = voice_channels_database[key]["users"][target]['amount']
    #                     percent_ownage = round((total_owned / voice_channels_database[key]['stocks']) * 100, 2)
    #                     embed.add_field(name=f"{voice_channels_database[key]['name']}", value=f'Stake: {percent_ownage}%')
    #             await message.channel.send(embed=embed)
    #         else:
    #             await message.channel.send(f'User does not exist!')    
                

    # if message.content.startswith('!myrewards'):
    #     rewards_user = database[message.author.name]['rewards']
    #     embed = discord.Embed(title=f"Rewards", description=f"{message.author.name} current rewards") #,color=Hex code
    #     for reward in rewards_user:
    #         print(reward, rewards[reward])
    #         embed.add_field(name=f"{reward}", value=f'{rewards[reward][0]}')
    #     await message.channel.send(embed=embed)


    # if message.content.startswith('!rewardhelp'):

    #     embed = discord.Embed(title=f"Rewards", description=f"Current rewards") #,color=Hex code
    #     for reward in rewards:
    #         embed.add_field(name=f"{reward} {rewards[reward][0]}", value=f'{rewards[reward][1]}')
    #     await message.channel.send(embed=embed)


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

    # if message.content.startswith('!givereward'):
    #     str_split = message.content.split(' ')
    #     if len(str_split) > 3 or len(str_split) < 3:
    #         await message.channel.send(f'Too many or few arguments. Use !givereward <target> <reward>')
    #     reward = str(str_split[2])
    #     target = str_split[1]
    #     role_names = [role.name for role in message.author.roles]
    #     if 'Admin' in role_names or 'Server: Mod' in role_names:
    #         if target in database:
    #             if reward in rewards:
    #                 if reward in database[target]['rewards']:
    #                     database[target]['rewards'][reward] += 1
    #                 else:
    #                     database[target]['rewards'][reward] = 1
    #                 write_db(database)
    #                 await message.channel.send(f'{message.author.name} added {reward} {rewards[reward][0]} to {target}.')
    #             else:
    #                 await message.channel.send(f'Reward does not exist!')
    #     else:
    #         await message.channel.send(f'You are not admin or moderator!')
    

    if message.content.startswith('!changetime'):
        str_split = message.content.split(' ')
        if message.author.name == 'Foxxravin':
            time = str_split[1]
            global hour_cumww
            hour_cumww = int(time)

            await message.channel.send(f'Changed cum ww time to: {hour_cumww}')
        else:
            await message.channel.send(f'You are not Foxxravin!')


    if message.content.startswith('!draw'):
        if MAIN_CARD_LOCK:
            str_split = message.content.split(' ')
            if len(str_split) > 2 or len(str_split) < 2:
                await message.channel.send(f'Too many or few arguments. Use !draw <target>')
            else:
                if len(database[message.author.name]['cards']) < 10:
                        
                    await message.channel.send(f'Drawing cards.... Please wait.')
                    land = str_split[1].lower()
                    # lands = ['forest', 'mountain', 'desert', 'swamp', 'blackhole', 'tundra', 'angel', 'artifact', 'mountain']
                    lands = ['light', 'evil', 'artifact']
                    descriptions = ['Exiled', 'Ginger', 'Crimson', 'Ugly', 'Sexy', 'Perverted', 'Washed', 'Fermented']
                    type = ['Skeleton', 'Monster', 'Dragon', 'Angel', 'Demon', 'Ghost', 'Vampire', 'Devil', 'Worm', 'Cunt', 'Land', 'Spacestation', 'Space', 'Table', 'Forest', 'Desert', 'Blackhole', 'Mountain', 'Sink', 'Falls', 'Bat', 'Asshole', 'Paint', 'Gobling', 'Sky', 'Heaven', 'Goblet', 'Chicken', 'Lizard', 'Softgun', 'Teacher', 'Mentor', 'Beer', 'Eye', 'Tower']

                    random_land = np.random.randint(0, len(lands))
                    random_description = np.random.randint(0, len(descriptions))
                    random_type = np.random.randint(0, len(type))

                    total_sentence = f'{descriptions[random_description]} {type[random_type]}'
                    if land in lands:
                        path_imge = await card_drawing(total_sentence, land, message.author.name)
                        await message.channel.send(file=discord.File(path_imge))
                        
                    else:
                        await message.channel.send(f'Land does not exist!')
                else:
                    await message.channel.send(f'You can only have 10 cards!')
        else:
            await message.channel.send(f'Wait until last card is fully drawn!')

    
    if message.content.startswith('!paint'):
        styles = {'Steampunk': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[9]/div/div/img', 'Fantasy': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[8]/div/div/img', 'Synthwave': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[11]/div/div/img', 'Pastel': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[5]/div/div/img', 'Mystical': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/img', 'Ukiyoe': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[10]/div/div/img', 'Dark fantasy': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[3]/div/div/img', 'HD': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[6]/div/div/img', 'Festive': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div/div/img', 'Psychic': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[4]/div/div/img', 'Vibrant': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[7]/div/div/img'}
        str_split = message.content.split(' ')
        if len(str_split) < 2:
                await message.channel.send(f'Too many or few arguments. Use !draw <target>')
        else:
            str_split = str_split[1:]
            total_sentence = ''
            for word in str_split:
                total_sentence += word+' '
            await message.channel.send(f'Painting.... Please wait.')
            path_imge = cardsystem.do_card_regular(total_sentence)
            await message.channel.send(file=discord.File(path_imge))


    # if message.content.startswith('!buy'):
        
    #     str_split = message.content.split(' ')
    #     if len(str_split) > 3 or len(str_split) < 3:
    #         await message.channel.send(f'Too many or few arguments. Use !buy <vc_name> <amount>')
    #     else:
    #         vc_channels = client.guilds[0].voice_channels
    #         voice_channels = list(vc_channels)
    #         vc_name = str(str_split[1])
    #         amount = np.abs(float(str_split[2]))
    #         for key in voice_channels:
    #             keyid = str(key.id)
    #             if vc_name.lower() == str(key.name).lower():
    #                 voice_channels_database[keyid]['name'] = key.name
    #                 vc_value = float(voice_channels_database[keyid]['value'])
    #                 total_bought = [voice_channels_database[keyid]['users'][x]['amount'] for x in voice_channels_database[keyid]['users']]
    #                 total_bought = np.array(total_bought).sum() + amount
    #                 total_left =  (voice_channels_database[keyid]['stocks'] - total_bought) >= 0
    #                 target_has_to_pay = round((amount*0.05*vc_value + vc_value)*amount,2)
    #                 if (target_has_to_pay <= database[message.author.name]['coins']) and total_left:
    #                     database[message.author.name]['coins'] -= target_has_to_pay
    #                     if message.author.name in voice_channels_database[keyid]['users']:
    #                         voice_channels_database[keyid]['users'][message.author.name]['amount'] += amount
    #                     else:
    #                         voice_channels_database[keyid]['users'][message.author.name] = {'amount':amount}
                        
    #                     voice_channels_database[keyid]['value'] += amount*0.05*vc_value
    #                     # database[message.author.name]['rewards']['Investor'] = 1
    #                     write_read_voice_channels(voice_channels_database)
    #                     await message.channel.send(f'{message.author.name} Bought {amount} shares in {key.name} for {target_has_to_pay} <:CBCcoin:831506214659293214>.')
    #                     write_db(database)
    #                 else:
    #                     await message.channel.send(f'You do not have enough coins, you need {target_has_to_pay} <:CBCcoin:831506214659293214> for this purchase (amount^2 * 0.05*vc_value + vc_value*amount)).')
    #                 if not total_left:
    #                     await message.channel.send(f'All stocks of this channel has been bought or you are trying to buy too many!')

    # if message.content.startswith('!sell'):
    #     await message.channel.send(f'This function is disabled until fixed')
        # str_split = message.content.split(' ')
        # if len(str_split) > 3 or len(str_split) < 3:
        #     await message.channel.send(f'Too many or few arguments. Use !sell <vc_name> <amount>')
        # else:
        #     vc_channels = client.guilds[0].voice_channels
        #     voice_channels = list(vc_channels)
        #     vc_name = str(str_split[1])
        #     amount = np.abs(float(str_split[2]))
        #     for key in voice_channels:
        #         keyid = str(key.id)
        #         if vc_name.lower() == str(key.name).lower():
        #             voice_channels_database[keyid]['name'] = key.name
        #             vc_value = float(voice_channels_database[keyid]['value'])
        #             if amount <= voice_channels_database[keyid]['users'][message.author.name]['amount']:
        #                 target_earns = round(amount*vc_value, 2)
        #                 database[message.author.name]['coins'] += target_earns
        #                 voice_channels_database[keyid]['users'][message.author.name]['amount'] -= amount
                        
        #                 voice_channels_database[keyid]['value'] -= amount*0.05*vc_value
        #                 if voice_channels_database[keyid]['value'] <= 0:
        #                     voice_channels_database[keyid]['value'] = 0.5
        #                 # database[message.author.name]['rewards']['Investor'] = 1
        #                 write_read_voice_channels(voice_channels_database)
        #                 await message.channel.send(f'{message.author.name} Sold {amount} shares in {key.name} for {target_earns} <:CBCcoin:831506214659293214>.')
        #                 write_db(database)
        #             else:
        #                 await message.channel.send(f'You do not have that many shares!')

    #

    # if message.content.startswith('!vc'):
    #     embed = discord.Embed(title=f"Voice chat assets", description=f"Asset information for voice chats") #,color=Hex code
    #     vc_channels = client.guilds[0].voice_channels
    #     voice_channels = list(vc_channels)
    #     for key in voice_channels:
    #         voice_channels_database[str(key.id)]['name'] = str(key.name)

    #     for key in voice_channels_database:
    #         name = voice_channels_database[key]['name']
    #         value = round(voice_channels_database[key]['value'],3)
    #         stocks = round(voice_channels_database[key]['stocks'],3)
    #         users = voice_channels_database[key]['users']
    #         output = ''
    #         for user in users:
    #             percent_owned = round(users[user]['amount']/stocks*100,2)
    #             income_per_member = percent_owned * 1*20
    #             output += f'{user} | {percent_owned}%\n'

    #         embed.add_field(name=f"{name}", value=f'Price {value} <:CBCcoin:831506214659293214> + Fee\n {output}')
    #     await message.channel.send(embed=embed)

    
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
        embed.add_field(name=f"View a members profile", value=f'!lookup <target>')
        embed.add_field(name=f"Buy shares in a voicechat", value=f'!buy <vc_name> <amount>')
        embed.add_field(name=f"Check information about vc properties", value=f'!vc')
        await message.channel.send(embed=embed)
    

    write_db(database)


client.run(k)