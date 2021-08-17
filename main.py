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

import serial


arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.5)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    data = arduino.readline()
    return data

def get_temp_hum():
    while True:
        try:
            b = round(float(arduino.readline().decode().rstrip()),2)
            break
        except:
            pass
    return f'Temperature @ Foxxravin: {b} degrees celsius '

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

def write_db(database):
    try:
        with open('../database.txt', 'w', encoding='utf-8') as f:
            f.write(str(database))
    except:
        print('write error')


# logging.basicConfig(filename='main.log', level=logging.DEBUG)



def run_ledlight():
    # Run lighting system
    global temp_status
    print('event')
    lock_mem = False
    lock_jord = False
    for user in temp_status:
        if temp_status[user] != None:
            if temp_status[user].channel != None:
                if user == 'JordanLTD':
                    lock_jord = True
                else:
                    if temp_status[user].channel != None:
                        lock_mem = True
    
    if lock_jord:
        write_read('1')
        write_read('1')
        write_read('1')
        write_read('1')
        write_read('1')
    else:
        if lock_mem:
            write_read('2')
            write_read('2')
            write_read('2')
            write_read('2')
        else:
            write_read('3')
            write_read('3')
            write_read('3')
            write_read('3')

class Gift:
    all_gifts = []
    def __init__(self, id, username, amount):
        self.amount = amount
        self.username = username
        self.id = id
        self.all_gifts.append(self)


temp_status  = {}
database = read_db()

        
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
        with open('version.txt', 'r') as f:
            bot_version = float(f.read())
        # SEND TO PATCH LOG CHANNEL
        with open('patchnotes.txt', 'r', encoding='utf-8') as f:
            patchnotes = f.read()
        patchchannel = client.get_channel(831638592106921994)
        embed = discord.Embed(title=f"Crazy Blazin bot patch notes", description=f"Build {bot_version} patch notes.") #,color=Hex code
        embed.add_field(name=f"Patch notes:", value=f'{patchnotes}')
        await patchchannel.send(embed=embed)


        # members = self.get_all_members()
        # for member in members:
        #     role_names = [role.name for role in member.roles]
        #     if member.name not in database:
        #         role_names = [role.name for role in member.roles]
        #         if 'Bots' in role_names:
        #             pass
        #         else:
        #             database[member.name] = {'coins': 100}


# sio = socketio.Client()



# with open('musicdatabase.txt', 'r') as f:
#     musicdatabase = eval(f.read())


# def run():
#     sio.connect('http://127.0.0.1:5000', wait = True)
#     while True:
#         with open('musicdatabase.txt', 'r') as f:
#             musicdatabase = eval(f.read())
        
#         ordered = {}
#         final = []
#         for music in musicdatabase:
#             if 'upvotes' in musicdatabase[music]:
#                 ordered[music] = len(musicdatabase[music]['upvotes'])
#         for link in sorted(ordered, key=ordered.get, reverse=True):
#             final.append([link, ordered[link], musicdatabase[link]['added_by']])
#         sio.emit('msg', final)
#         sio.sleep(3)

# sio.start_background_task(target = run)

intents = discord.Intents.default()
intents.members = True
client = MyClient(intents = intents)




def create_gif(username, price, jellys, special = False, filename = ''):

    # create/delete our temp files folder
    if os.path.exists('frames'):
        shutil.rmtree('frames')
    os.mkdir('frames')

    # load in the background image
    if special:
        gif_image = Image.open('background2.gif')
    else:
        gif_image = Image.open('background.gif')

    # set up colours and vars
    x = 10
    y = 10
    silver = (100, 100, 100)
    purple = (100, 0, 200)
    pink = (255, 0, 255)
    white = (255, 255, 255)

    text_name = f"{username}"
    text_price = f"Looted {price} CBC!!!!"
    text_price_jell = f"Looted {jellys} luck jells!!"

    # load the font
    font = ImageFont.truetype("ShortBaby-Mg2w.ttf", 30)
    # draw = ImageDraw.Draw(img_background)

    # add text to each frame
    # frames = []
    if special:
        for N, frame in enumerate(ImageSequence.Iterator(gif_image)):
            frame2 = frame.copy().convert('RGBA').resize((400, 300), resample=(1))
            draw = ImageDraw.Draw(frame2)
            # draw.text((x, y), text_name, silver, font=font)
            # draw.text((x, y), text_name, white, font=font)

            if N%10 == 0:
                # draw.text((x+50, y+200), text_name, white, font=font)
                if N > 187:
                    draw.text((x+90, y+230), text_name, white, font=font)
                    draw.text((x+60, y+70), text_price, white, font=font)
                    if jellys > 0:
                        draw.text((x+40, y+110), text_price_jell, white, font=font)
            else:
                if N > 170:
                    draw.text((x+90, y+230), text_name, pink, font=font)
                    if N > 187:
                        draw.text((x+60, y+70), text_price, pink, font=font)
                        if jellys > 0:
                            draw.text((x+40, y+110), text_price_jell, pink, font=font)
                        

            # draw.text((x+10, y+10), text_price, silver, font=font)
            # draw.text((x+10, y+10), text_price, white, font=font)
            frame2.save("./frames/{}.png".format(str(N).zfill(3)))
            # frames.append(frame)

    else:
        for N, frame in enumerate(ImageSequence.Iterator(gif_image)):
            frame2 = frame.copy().convert('RGBA').resize((400, 300), resample=(1))
            draw = ImageDraw.Draw(frame2)
            draw.text((x+90, y+230), text_name, pink, font=font)
            # draw.text((x, y), text_name, silver, font=font)
            # draw.text((x, y), text_name, white, font=font)

            if N%10 == 0:
                # draw.text((x+50, y+200), text_name, white, font=font)
                if N > 35:
                    draw.text((x+60, y+70), text_price, white, font=font)
                    if jellys > 0:
                        draw.text((x+40, y+110), text_price_jell, white, font=font)
            else:
                if N > 35:
                    draw.text((x+60, y+70), text_price, pink, font=font)
                    if jellys > 0:
                        draw.text((x+40, y+110), text_price_jell, pink, font=font)
                        

            # draw.text((x+10, y+10), text_price, silver, font=font)
            # draw.text((x+10, y+10), text_price, white, font=font)
            frame2.save("./frames/{}.png".format(str(N).zfill(3)))
            # frames.append(frame)

        for N2 in range(1, 50):
            frame = frame.copy().convert('RGBA').resize((400, 300), resample=(1))
            draw = ImageDraw.Draw(frame)
            draw.text((x+90, y+230), text_name, pink, font=font)
            # draw.text((x, y), text_name, silver, font=font)
            # draw.text((x, y), text_name, white, font=font)

            if N2%10 == 0:
                draw.text((x+60, y+70), text_price, white, font=font)
                if jellys > 0:
                        draw.text((x+40, y+110), text_price_jell, white, font=font)
            else:
                draw.text((x+60, y+70), text_price, pink, font=font)
                if jellys > 0:
                        draw.text((x+40, y+110), text_price_jell, pink, font=font)
            # draw.text((x+10, y+10), text_price, silver, font=font)
            # draw.text((x+10, y+10), text_price, white, font=font)
            frame.save("./frames/{}.png".format(str(N+N2).zfill(3)))
            # frames.append(frame)

    # frames[0].save('out.gif', save_all=True, append_images=frames[1:])
    # del frames

    # # output the result

    os.system('ffmpeg -i frames/%03d.png -vf scale=500:-1:sws_dither=ed,palettegen -y palette.png')
    # os.system('ffmpeg -i image%d.jpg video.flv')
    # os.system('ffmpeg -i video.flv -i palette.png -filter_complex "fps=1.2,scale=900:-1:flags=lanczos[x];[x][1:v]paletteuse" out.gif')
    os.system(f'ffmpeg -framerate 15 -i frames/%03d.png -c:v ffv1 -r 15 -y {filename}.avi')
    os.system(f'ffmpeg -i {filename}.avi -i palette.png -filter_complex "fps=15,scale=300:-1:flags=lanczos[x];[x][1:v]paletteuse" -y -loop -1 {filename}.gif')
    # os.system('ffmpeg -y -i out.flv out.gif')

    # clean up
    shutil.rmtree('frames')
    os.remove(f'{filename}.avi')
    os.remove('palette.png')


hour_cumww = 10
EVENT_IN_PROGRESS = False



def add_coins(stream_state, user, cointype):
    global database
    # database = read_db()
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
    write_db(database)


async def ticksystem():
    while True:
        global temp_status
        # database = read_db()
        global database
        for user in database:
            # if 'cumww' not in database[user]:
            #     database[user]['cumww'] = False
            # if database[user]['cumww']:
            #     cumww_user = user
            
            if 'topcoins' not in database[user]:
                database[user]['topcoins'] = database[user]['coins']
            else:
                if database[user]['coins'] >= database[user]['topcoins']:
                    database[user]['topcoins'] = database[user]['coins']
            write_db(database)
            # database = read_db()


        for user in database:
            if user in temp_status:
                state = temp_status[user]
                if state != None:

                    if state.channel != None:
                        channelid = str(state.channel.id)
                        stream_state = state.self_stream
                        if channelid != 'None':
                            if channelid != str(847583212926009374):
                                add_coins(stream_state, user, 'coins')
                            else:
                                add_coins(stream_state, user, 'shekels')
                    else:
                        channelid = str(0)

            # database = read_db()
            
            
            if 'Timer' in database[user]:
                if database[user]['Timer'] <= 0:
                    database[user]['Timer'] = 0
                else:
                    database[user]['Timer'] -= 10
            
            # if 'Crowned' not in database[user]:
            #     database[user]['Crowned'] = False
                
            # if database[user]['Crowned']:
            #     if 'coins' in database[user]:
            #         database[user]['coins'] = round(database[user]['coins'] + 0.1, 2)
            #         print(f'Crowned Coins to : {user}')
            #     else:
            #         database[user]['coins'] =  100
            
            # if 'bitten' not in database[user]:
            #     database[user]['bitten'] = False
            # if database[user]['bitten']:
            #     database[user]['coins'] -= 1
            #     database[cumww_user]['coins'] += 1
            #     database[cumww_user]["totalcoinsbitten"] += 1
            
            write_db(database)
        # check_version()
        await asyncio.sleep(10)


async def timer():
    await client.wait_until_ready()
    # channel = client.get_channel(867753681301929994)
    # msg_sent = False
    # msg_sent_reveal = False

    while True:
        run_ledlight()
        print('timer running')
        global hour_cumww
        # database = read_db()
        global database
        time = datetime.datetime.now
        print(hour_cumww)
        if time().hour == int(hour_cumww):# and time().minute == 9:
            # print('TIME IS ON ', hour_cumww)
            if not msg_sent:
                # print('ww is chosen!')
                # rand_cumwolf = np.random.choice(list(database.keys()))
                # members = client.get_all_members()
                for user in database:
                    # if 'wascumww' in database[user]:
                    #     if database[user]['wascumww']:
                    #         if "totalcoinsbitten" not in database[user]:
                    #             await channel.send(f'Last cum werewolf was: {user}!')
                    #         else:
                    #             await channel.send(f'Last cum werewolf was: {user}. This cum loving werewolf stole a total of {database[user]["totalcoinsbitten"]} CBC!')
                    database[user]['cumww'] = False
                    database[user]['guesswolf'] = True
                    database[user]['bitten'] = False
                    database[user]['active_wolf'] = False
                    database[user]['wascumww'] = False
                    database[user]['lootbox'] = True
                    database[user]['lootkeysgiven'] = True
                    database[user]['totalcoinsbitten'] = 0
                # for member in members:
                #     if member.name == rand_cumwolf:
                #         await member.send('You are now the cum werewolf, bite users to drain their coins! !bite <user>. New werewolf will be assigned in 24 hours! NB! You should send the command directly to this bot so no one sees it! If you do not want to be cum werewolf write !cumresign.')
                #         await channel.send(f'A new cum werewolf has been chosen! Try to guess who before he/she steals all your coins!')
                #         database[rand_cumwolf]['cumww'] = True
                #         database[rand_cumwolf]['wascumww'] = True
                # msg_sent = True
                write_db(database)
        else:
            msg_sent = False
        
        # time = datetime.datetime.now
        # if time().hour%4 == 0:# and time().minute == 9:
        #     if not msg_sent_reveal:
        #         for user in database:
        #             if database[user]['cumww']:
        #                 rand_cumwolf_split = [char for char in user]
        #                 random_letter = np.random.choice(rand_cumwolf_split)
        #                 await channel.send(f'Hint: Random letter/number from username is: {random_letter.lower()}')
        #         msg_sent_reveal = True
        # else:
        #     msg_sent_reveal = False

        # check_version()
        await asyncio.sleep(4)
        

client.loop.create_task(ticksystem())
client.loop.create_task(timer())


@client.event
async def on_voice_state_update(member, before, after):
    global temp_status
    # database = read_db()
    global database
    if member.name not in database:
        database[member.name] = {'coins': 100}
        write_db(database)
    

    temp_status[member.name] = after

    run_ledlight()



    if member.name in database:
        if 'Timer' in database[member.name]:
            curr_timer = database[member.name]['Timer']
            role_names = [role.name for role in member.guild.roles]
            if curr_timer <= 0 and 'Crazy Blazin Gold' in role_names:
                role = get(member.guild.roles, name='Crazy Blazin Gold')
                await member.remove_roles(role)



# @client.event
# async def on_reaction_add(reaction, user):
#     if str(reaction.message.channel.id) == str(795738540251545620):
#         if reaction.emoji == '💥':
#             with open('musicdatabase.txt', 'r') as f:
#                 musicdatabase = eval(f.read())
#             if reaction.message.content in musicdatabase:
#                 musicdatabase[reaction.message.content]['upvotes'].append(reaction.message.author.name)

#             with open('musicdatabaseBACKUP.txt', 'w') as f:
#                 f.write(str(musicdatabase))
            
#             with open('musicdatabase.txt', 'w') as f:
#                 f.write(str(musicdatabase))


# @client.event
# async def on_reaction_remove(reaction, user):
#     if str(reaction.message.channel.id) == str(795738540251545620):
#         if reaction.emoji == '💥':
#             with open('musicdatabase.txt', 'r') as f:
#                 musicdatabase = eval(f.read())
#             with open('musicdatabaseBACKUP.txt', 'w') as f:
#                 f.write(str(musicdatabase))
#             if reaction.message.content in musicdatabase:
#                 if reaction.message.author.name in musicdatabase[reaction.message.content]['upvotes']:
#                     musicdatabase[reaction.message.content]['upvotes'].remove(reaction.message.author.name)
#             with open('musicdatabase.txt', 'w') as f:
#                 f.write(str(musicdatabase))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    get_temp_hum()
    
    global database

    file_checker = os.path.isfile('web/giftcard.txt')
    if file_checker:
        with open('web/giftcard.txt', 'r') as f:
            giftcards = f.read().split('\n')[:-1]
            for gift_users in giftcards:
                gift_users = eval(gift_users)
                database[gift_users[0]]['coins'] += gift_users[1]
        os.remove('web/giftcard.txt')

    members = client.get_all_members()
    for member in members:
        if member.name not in database:
            role_names = [role.name for role in member.roles]
            if 'Bots' not in role_names:
                database[member.name] = {}
                database[member.name]['cumww'] = False
                database[member.name]['bitten'] = False
                database[member.name]['coins'] = 100
                database[member.name]['shekels'] = 100
                database[member.name]['guesswolf'] = True
                database[member.name]["totalcoinsbitten"] = 0
    write_db(database)
    # if str(message.channel.id) == str(795738540251545620):
    #     with open('musicdatabase.txt', 'r') as f:
    #         musicdatabase = eval(f.read())
    #     with open('musicdatabaseBACKUP.txt', 'w') as f:
    #             f.write(str(musicdatabase))
    #     if str(message.content) not in musicdatabase:
    #         musicdatabase[message.content] = {}
    #         musicdatabase[message.content]['upvotes'] = []
    #         musicdatabase[message.content]['added_by'] = message.author.name
    #     with open('musicdatabase.txt', 'w') as f:
    #         f.write(str(musicdatabase))

    if message.content.startswith('!bal'):
        # database = read_db()
        value = database[message.author.name]['coins']

        if 'shekels' in database[message.author.name]:
            shekval = database[message.author.name]['shekels']
        else:
            shekval = 100
            database[message.author.name]['shekels'] = shekval
        embed = discord.Embed(title=f"Balance", description=f"{message.author.name} current balance") #,color=Hex code


        if 'jellys' not in database[message.author.name]:
            database[message.author.name]['jellys'] = 0
            write_db(database)

        if 'lootkeys' not in database[message.author.name]:
            database[message.author.name]['lootkeys'] = 0
            write_db(database)

        # if 'spankcoin' in database[message.author.name]:
        #     embed.add_field(name=f"Spank coins", value=f'{round(valuespank,2)} <:raised_hands_tone1:859521216115900457>')
        embed.add_field(name=f"Crazy Blazin Coins", value=f'{round(value,2)} <:CBCcoin:831506214659293214>')
        embed.add_field(name=f"Sheqalim", value=f'₪ {round(shekval,2)}')
        embed.add_field(name=f"Key shards", value=f' ({database[message.author.name]["lootkeys"]}/3) :key: ')
        embed.add_field(name=f"Luck jells", value=f' {database[message.author.name]["jellys"]} :kiwi: ')
        await message.channel.send(embed=embed)


    if message.content.startswith('!refundall'):
        str_split = message.content.split(' ')
        amount = float(str_split[1])*np.sign(float(str_split[1]))
        if message.author.name == 'Foxxravin':
            # database = read_db()
            for user in database:
                if 'coins' in database[user]:
                    database[user]['coins'] += int(amount)

            write_db(database)

            await message.channel.send(f'All users have been refunded {amount} <:CBCcoin:831506214659293214>')
        else:
            await message.channel.send(f'You are not Foxxravin!')



    if message.content.startswith('!restartdaily'):
        str_split = message.content.split(' ')
        if message.author.name == 'Foxxravin':
            # database = read_db()
            for user in database:
                database[user]['lootbox'] = True
            write_db(database)
            await message.channel.send(f'All users have reset daily chest!')
        else:
            await message.channel.send(f'You are not Foxxravin!')
    


    if message.content.startswith('!transfer'):
        str_split = message.content.split(' ')
        if len(str_split) > 3 or len(str_split) < 3:
            await message.channel.send(f'Too many or few arguments. Use !transfer <target> <amount>')
        amount = round(float(str_split[2]),2)
        target = str_split[1]
        # database = read_db()
        if message.author.name == 'Foxxravin' and target in database:
            if 'coins' in database[target]:
                database[target]['coins'] += amount
            write_db(database)
            await message.channel.send(f'{message.author.name} transfered {amount} <:CBCcoin:831506214659293214> to {target}.')
        else:
            await message.channel.send(f'You are not Foxxravin!')
    

    if message.content.startswith('!changetime'):
        str_split = message.content.split(' ')
        if message.author.name == 'Foxxravin':
            time = str_split[1]
            global hour_cumww
            hour_cumww = int(time)

            await message.channel.send(f'Changed cum ww time to: {hour_cumww}')
        else:
            await message.channel.send(f'You are not Foxxravin!')


    
    if message.content.startswith('!buy gold'):
        
        str_split = message.content.split(' ')
        if len(str_split) > 2 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !buy gold')
        else:
            # database = read_db()
            if 1000 <= database[message.author.name]['coins']:
                database[message.author.name]['coins'] -= 1000

                member = message.author
                role = get(member.guild.roles, name='Crazy Blazin Gold')
                await member.add_roles(role)
                # await bot.remove_roles(user, 'member')
                await message.channel.send(f'{message.author.name} Bought Crazy Blazin Gold Role for one month!')

                database[message.author.name]['Timer'] = 2592000
                write_db(database)

            else:
                await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC) to buy Crazy Blazin Gold! Price: 1000 <:CBCcoin:831506214659293214> (CBC)')
    


                
    if message.content.startswith('!gamble'):
        str_split = message.content.split(' ')
        if len(str_split) > 2 or len(str_split) < 2 and str_split[0] != '!gambleall':
            await message.channel.send(f'Too many or few arguments. Use !gamble <amount>')
        else:
            # database = read_db()
            try:
                if str_split[0] == '!gambleall':
                    amount = database[message.author.name]['coins']
                else:
                    amount = float(str_split[1])*np.sign(float(str_split[1]))
                if amount <= database[message.author.name]['coins']:
                    database[message.author.name]['coins'] -= amount

                    if 'jellys' not in database[message.author.name]:
                        database[message.author.name]['jellys'] = 0
                        write_db(database)
                    
                    jellpoints = database[message.author.name]['jellys']
                    if jellpoints > 15:
                        jellpoints = 15
                    roll = np.random.randint(1, 101)
                    if roll > (51-jellpoints):
                        database[message.author.name]['coins'] += 2*amount
                        database[message.author.name]['coins'] = round(database[message.author.name]['coins'], 2)
                        await message.channel.send(f'{message.author.name} Rolled {roll} and won {round(2*amount,2)}<:CBCcoin:831506214659293214>  :partying_face:. Win chance({round(((50+jellpoints)/100)*100, 2)}%)')
                        write_db(database)
                    else:
                        await message.channel.send(f'{message.author.name} Rolled {roll} and lost {amount} <:CBCcoin:831506214659293214> :frowning2: Win chance({round(((50+jellpoints)/100)*100, 2)}%)')
                        write_db(database)
                    
                    if database[message.author.name]['coins'] >= database[message.author.name]['topcoins']:
                        database[message.author.name]['topcoins'] = database[message.author.name]['coins']
                        write_db(database)
                else:
                    await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC) to gamble!')
            except Exception as e:
                print(e)


    # if message.content.startswith('!uwuprison'):
    #     str_split = message.content.split(' ')
    #     if len(str_split) > 2 or len(str_split) < 2:
    #         await message.channel.send(f'Too many or few arguments. Use !uwuprison <target>')
    
    #     else:
    #         database = read_db()
            
    #         target = str(str_split[1])
    #         if 1 <= database[message.author.name]['coins']:
    #             database[message.author.name]['coins'] -= 200

    #             await message.channel.send(f'{message.author.name} sent {target} to UwU prison <:aegao:849030455189438485> !')
    #             write_db(database)
    #             rpgmusicpath = r"uw.mp3"
    #             # grab the user who sent the command
    #             user = message.author
    #             channel = None
    #             voice_channel = user.voice.channel
    #             if voice_channel != None:
    #                 channel = voice_channel.name
    #                 vc = await voice_channel.connect()
    #                 vc.play(discord.FFmpegPCMAudio(rpgmusicpath))
    #                 await asyncio.sleep(5)
    #                 vc.stop()
    #                 await vc.disconnect()
    #             else:
    #                 await message.channel.send('User is not in a channel.')
    #         else:
    #             await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC) to send {target} to UwU prison!')
        

    
    if message.content.startswith('!coinswap'):
        str_split = message.content.split(' ')
        if len(str_split) > 2 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !coinswap <amount>')
        else:
            # database = read_db()
            
            amount = round(float(str_split[1])*np.sign(float(str_split[1])),2)
            if amount <= database[message.author.name]['shekels']:
                database[message.author.name]['shekels'] -= amount
                database[message.author.name]['coins'] += amount

                await message.channel.send(f'{message.author.name} swapped ₪ {amount} for {amount} <:CBCcoin:831506214659293214>!')
                write_db(database)
            else:
                await message.channel.send(f'{message.author.name} does not have enough ₪ to swap to (CBC)!')




    if message.content.startswith('!help'):
        embed = discord.Embed(title=f"Commands", description=f"All commands for crazy blazin server")
        embed.add_field(name=f"Balance", value=f'!bal')
        embed.add_field(name=f"Gamble crazy blazin coins", value=f'!gamble <amount>')
        embed.add_field(name=f"Gamble everything.", value=f'!gambleall')
        embed.add_field(name=f"Buy gold account price: 1000 CBC", value=f'!buy gold')
        embed.add_field(name=f"Show users with historically most coins.", value=f'!top')
        embed.add_field(name=f"Swap ₪ shekels for crazy blazin coins <:CBCcoin:831506214659293214>", value=f'!coinswap <amount>')
        embed.add_field(name=f"Grab your daily loot! Can only be used once per day.", value=f'!daily')
        embed.add_field(name=f"Give a key shard to someone you appreciate. Can only be used once per day.", value=f'!givekey <target>')
        embed.add_field(name=f"Start loot crate event in a voice channel (ADMINS/MODS) only!.", value=f'!startevent')
        embed.add_field(name=f"Get temperature @ foxx!.", value=f'!foxxdeg')
        await message.channel.send(embed=embed)

    
    if message.content.startswith('!daily'):
        # database = read_db()

        random_id = np.random.randint(0, 10000)
        gif_name = f'out_{random_id}'
        if 'lootbox' not in database[message.author.name]:
            database[message.author.name]['lootbox'] = True
            write_db(database)
        
        if 'lootkeys' not in database[message.author.name]:
            database[message.author.name]['lootkeys'] = 0
            write_db(database)

        if database[message.author.name]['lootkeys'] >= 3:
            database[message.author.name]['lootkeys'] -= 3
            await message.channel.send(f'You have used 3 key shards to open daily chest, you have now ({database[message.author.name]["lootkeys"]}/3) :key: shards left!')
            price = np.random.randint(10, 10000)
            database[message.author.name]['coins'] += price
            jellylickpercentage = np.random.randint(0, 101)

            if jellylickpercentage <= 10:
                jellys = np.random.randint(1, 4)
                if 'jellys' in database[message.author.name]:
                    database[message.author.name]['jellys'] += jellys
                else:
                    database[message.author.name]['jellys'] = jellys
            else:
                jellys = 0
            write_db(database)
            create_gif(message.author.name, price, jellys, special=False, filename = gif_name)
            await message.channel.send(file=discord.File(gif_name+'.gif'))
            os.remove(gif_name+'.gif')
        else:
            if database[message.author.name]['lootbox']:
            # if True:
                database[message.author.name]['lootbox'] = False
                price = np.random.randint(10, 10000)
                jellylickpercentage = np.random.randint(0, 101)
                if jellylickpercentage <= 10:
                    jellys = np.random.randint(1, 4)
                    if 'jellys' in database[message.author.name]:
                        database[message.author.name]['jellys'] += jellys
                    else:
                        database[message.author.name]['jellys'] = jellys
                else:
                    jellys = 0
                database[message.author.name]['coins'] += price
                write_db(database)
                create_gif(message.author.name, price, jellys, special=False, filename = gif_name)
                await message.channel.send(file=discord.File(gif_name+'.gif'))
                os.remove(gif_name+'.gif')
            else:
                await message.channel.send(f'You have already looted today and not enough key shards!')



    if message.content.startswith('!givekey'):
        str_split = message.content.split(' ')
        if len(str_split) > 2 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !givekey <target>')
        else:
            # database = read_db()
            target = str_split[1]
            if target in database:
                if target == message.author.name:
                    await message.channel.send(f'You cannot give key shard to yourself!')
                else:
                    if 'lootkeysgiven' in database[message.author.name]:
                        if database[message.author.name]['lootkeysgiven']:
                            if 'lootkeys' not in database[target]:
                                database[target]['lootkeys'] = 0
                            
                            database[target]['lootkeys'] += 1
                            await message.channel.send(f'{message.author.name} gave 1 key shard to {target}!')
                            write_db(database)
                        else:
                            await message.channel.send(f'You have already given out key shard today!')

                    else:
                        database[message.author.name]['lootkeysgiven'] = False
                        if 'lootkeys' not in database[target]:
                            database[target]['lootkeys'] = 0
                        database[target]['lootkeys'] += 1
                        await message.channel.send(f'{message.author.name} gave 1 key shard to {target}!')
                        write_db(database)
            else:
                await message.channel.send(f'Target does not exist!')


    if message.content.startswith('!restartserver'):
        if message.author.name == 'Foxxravin':
            await message.channel.send(f'Restarting server....')
            subprocess.run("start python restart.bat", shell=True, check=True)
        else:
            await message.channel.send(f'You are not Foxxravin!')


    if message.content.startswith('!getuserinfo'):
        if message.author.name == 'Foxxravin':
            str_split = message.content.split(' ')
            if len(str_split) > 2 or len(str_split) < 2:
                await message.channel.send(f'Too many or few arguments. Use !getuserinfo <target>')
            else:
                target = str_split[1]
                if target in database:
                    await message.channel.send(str(database[target]))
                else:
                    await message.channel.send('Target not in database!')
        else:
            await message.channel.send(f'You are not Foxxravin!')



    if message.content.startswith('!foxxdeg'):
        temp = get_temp_hum()
        print(temp)
        await message.channel.send(temp)
        

    
    if message.content.startswith('!changeuserinfo'):
        if message.author.name == 'Foxxravin':
            str_split = message.content.split(' ')
            if len(str_split) > 4 or len(str_split) < 4:
                await message.channel.send(f'Too many or few arguments. Use !changeuserinfo <target> <statname> <value>')
            else:
                target = str_split[1]
                statname = str_split[2]
                value = eval(str_split[3])

                if target in database:
                    if statname in database[target]:
                        database[target][statname] = value
                        await message.channel.send('Target stat value changed by admin')
                    else:
                        await message.channel.send(f'{statname} does not exist in the database!')
                else:
                    await message.channel.send('Target not in database!')
        else:
            await message.channel.send(f'You are not Foxxravin!')



    if message.content.startswith('!makegift'):
        role_names = [role.name for role in message.author.roles]
        if 'Admin' in role_names or 'Server: Influencer' in role_names:
            str_split = message.content.split(' ')
            if len(str_split) > 3 or len(str_split) < 3:
                await message.channel.send(f'Too many or few arguments. Use !makegift <target> <amount>')
            else:
                username = str_split[1]
                amount = int(str_split[2])
                if username in database:
                    id = str(uuid.uuid1())[-5:]

                    requests.get(f'http://f571b8f37f9d.ngrok.io/admin/api/gift_creation/{id}/{username}/{amount}')
                    img = qrcode.make(f'http://f571b8f37f9d.ngrok.io/api/{id}')
                    im2 = Image.open('images/NEW_CB_LOGO_gift.png')
                    print(f'http://f571b8f37f9d.ngrok.io/api/{id}')

                    dst = Image.new('RGB', (im2.width, im2.height + img.height))
                    dst.paste(im2, (0, 0))
                    dst.paste(img, (0, im2.height))
                    dst.save("some_file.png")

                    await message.channel.send(file=discord.File('some_file.png'))
                    os.remove('some_file.png')
                else:
                    await message.channel.send('Username not in database!')
        else:
            await message.channel.send(f'You are not a mod or admin!')


                
    
    # if message.content.startswith('!crown'):
    #     str_split = message.content.split(' ')
    #     if len(str_split) > 2 or len(str_split) < 2:
    #         await message.channel.send(f'Too many or few arguments. Use !crown <target>')
    #     else:
    #         if message.author.name == 'JordanLTD':
    #             database = read_db()
                
    #             target = str_split[1]
    #             members = client.get_all_members()

    #             for user in database:
    #                 if 'Crowned' not in database[user]:
    #                     database[user]['Crowned'] = False
    #                 if database[user]['Crowned']:
    #                     database[user]['Crowned'] = False
    #                 if user == target and target != 'JordanLTD':
    #                     database[user]['Crowned'] = True

    #             for member in members:
    #                 if member.name == target:
    #                     role = get(member.guild.roles, name='Crowned')
    #                     await member.add_roles(role)
    #                 else:
    #                     role_names = [role.name for role in member.roles]
    #                     if 'Crowned' in role_names:
    #                         role = get(member.guild.roles, name='Crowned')
    #                         await member.remove_roles(role)

    #             write_db(database)

    #             await message.channel.send(f'{target} has been crowned by {message.author.name}:princess:, {target} will now have passive <:CBCcoin:831506214659293214> income until the crown is given to someone else or removed!')
    #         else:
    #             await message.channel.send(f'Only Yarden/Jordan/ירדן‎ :princess: can give someone the crown!‎')
    
    # if message.content.startswith('!removecrown'):
    #     if message.author.name == 'JordanLTD':
    #         database = read_db()
    #         for user in database:
    #             if 'Crowned' not in database[user]:
    #                 database[user]['Crowned'] = False
    #             if database[user]['Crowned']:
    #                 database[user]['Crowned'] = False
                
    #         write_db(database)

    #         members = client.get_all_members()
    #         for member in members:
    #             role_names = [role.name for role in member.roles]
    #             if 'Crowned' in role_names:
    #                 role = get(member.guild.roles, name='Crowned')
    #                 await member.remove_roles(role)

    #         await message.channel.send(f'{message.author.name}:princess: has removed the crown from the holder!')
    #     else:
    #         await message.channel.send(f'Only Yarden/Jordan/ירדן‎ :princess: can remove crown!')
    

    if message.content.startswith('!top'):
        # database = read_db()
        temp_stats  = {}
        for user in database:
            coins = database[user]['topcoins']
            temp_stats[user] = round(coins,2)

        index = 1
        embed = discord.Embed(title="Top coins history", description="Users that have had the most coins ever") #,color=Hex code
        medaljonger = [':crown:', ':second_place:', ':third_place:']
        for key in sorted(temp_stats, key=temp_stats.get, reverse=True):
            if (index < 11):
                if index < 4:
                    embed.add_field(name=f"{index}{medaljonger[index-1]}. {key}", value=f'{temp_stats[key]} <:CBCcoin:831506214659293214>')
                else:
                    embed.add_field(name=f"{index}. {key}", value=f'{temp_stats[key]} <:CBCcoin:831506214659293214>')
            else:
                await message.channel.send(embed=embed)
                return
            index += 1



    if message.content.startswith('!startevent'):
        global EVENT_IN_PROGRESS
        if not EVENT_IN_PROGRESS:
            random_id = np.random.randint(0, 10000)
            gif_name = f'out_{random_id}'
            EVENT_IN_PROGRESS = True
            role_names = [role.name for role in message.author.roles]
            if 'Admin' in role_names or 'Server: Mod' in role_names:
                members = client.get_all_members()
                tot_in_voice = []
                for member in members:
                    state = member.voice
                    if state != None:
                        tot_in_voice.append(member.name)

                if len(tot_in_voice) > 3:
                    await message.channel.send(f'{message.author.name} started a chest event!')
                    await asyncio.sleep(3)
                    await message.channel.send(f'ARE EVERYBODY READY??????? Are you ready!???? YOU MUST JOIN A VOICE CHAT WITHIN 1 MINUTE TO GET THE PRICE!!!!')
                    await asyncio.sleep(60)
                    jell = np.random.randint(0,2)
                    price = np.random.randint(0,20000)
                    winner = np.random.choice(tot_in_voice, 1)[0]
                    if 'jellys' not in database[winner]:
                        database[winner]['jellys'] = 0
                    database[winner]['jellys'] += jell
                    database[winner]['coins'] += price
                    write_db(database)
                    await message.channel.send(f'Generating winner......')
                    create_gif(winner, price, jellys = jell, special = True, filename = gif_name)
                    await message.channel.send(file=discord.File(f'{gif_name}.gif'))
                else:
                    await message.channel.send(f'There must be more than three users in voice chats to start event!')
            else:
                    await message.channel.send(f'{message.author.name} You need to be admin or mod to start this event!')
            
            EVENT_IN_PROGRESS = False
        else:
            await message.channel.send(f'An event is already in progress!')




    # if message.content.startswith('!bite'):
    #     str_split = message.content.split(' ')
    #     if len(str_split) > 2 or len(str_split) < 2:
    #         await message.channel.send(f'Too many or few arguments. Use !bite <target>')

    #     else:
    #         # database = read_db()
    #         target = str_split[1]
    #         channel = client.get_channel(867753681301929994)

    #         if target in database:
    #             if database[message.author.name]['cumww']:

    #                 if 'cumww' not in database[target]:
    #                     database[target]['cumww'] = False
    #                 if 'bitten' not in database[target]:
    #                     database[user]['bitten'] = False

    #                 if database[target]['bitten'] != True and message.author.name != target:
    #                     await message.channel.send(f'You have bitten {target}, he now bleed coins to you!')
    #                     database[target]['bitten'] = True
    #                     write_db(database)
    #                     await channel.send(f'{target} got bit by the cum werewolf and is now bleeding coins!')
    #                 else:
    #                     await message.channel.send(f'User is already bitten or you are trying to bite yourself! Try again!')
    #             else:
    #                 pass
    #         else:
    #             await message.channel.send(f'{target} does not exist!')
    #     try:
    #         pass
    #         # await client.delete_message(message)
    #     except:
    #         print('msg sent private')



    # if message.content.startswith('!cumresign'):
    #     channel = client.get_channel(867753681301929994)
    #     if database[message.author.name]['cumww']:

    #         await channel.send(f'The cum werewolf "{message.author.name}" resigned, a new cum werewolf is chosen!')
    #         # database = read_db()
    #         rand_cumwolf = np.random.choice(list(database.keys()))
    #         members = client.get_all_members()
    #         for user in database:
    #             database[user]['cumww'] = False
    #             database[user]['guesswolf'] = True
    #             database[user]['bitten'] = False
    #             database[user]["totalcoinsbitten"] = 0
    #         for member in members:
    #             if member.name == rand_cumwolf:
    #                 print(rand_cumwolf)
    #                 await member.send('You are now the cum werewolf, bite users to drain their coins! !bite <user>. New werewolf will be assigned in 24 hours! NB! You should send the command directly to this bot so no one sees it! If you do not want to be cum werewolf write !cumresign.')
    #                 await channel.send(f'A new cum werewolf has been chosen! Try to guess who before he/she steals all your coins!')
    #                 database[rand_cumwolf]['cumww'] = True
    #         write_db(database)
    


    # if message.content.startswith('!guess'):
    #     str_split = message.content.split(' ')
    #     if len(str_split) > 2 or len(str_split) < 2:
    #         await message.channel.send(f'Too many or few arguments. Use !guess <target>')        
        
    #     else:
    #         # database = read_db()
    #         target = str_split[1]
    #         if target in database:
    #             channel = client.get_channel(867753681301929994)
    #             target = str_split[1]
    #             if 'guesswolf' not in database[message.author.name]:
    #                 database[message.author.name]['guesswolf'] = True

    #             if target != message.author.name:
    #                 if database[message.author.name]['guesswolf']:
    #                     database[message.author.name]['guesswolf'] = False
    #                     if 'cumww' not in database[target]:
    #                         database[user]['cumww'] = False
    #                     if database[target]['cumww']:
    #                         await message.channel.send(f'{message.author.name} guessed correctly, cum werewolf ({target}) has been found, good job! 5000 <:CBCcoin:831506214659293214> has been credited to your account!')
    #                         database[message.author.name]['coins'] += 5000
    #                         await channel.send(f'The werewolf ({target}) has been found. This cum loving werewolf stole a total of {database[target]["totalcoinsbitten"]} CBC!')
    #                         database[target]['cumww'] = False
    #                         database[target]["totalcoinsbitten"] = 0
    #                         for user in database:
    #                             database[user]['bitten'] = False
    #                     else:
    #                         await message.channel.send(f'{target} is not the cum werewolf!')
    #                 else:
    #                     await message.channel.send(f"{message.author.name} can't guess more than once per day.")
    #             else:
    #                 await message.channel.send(f"{message.author.name} can't guess him/herself.")
    #         else:
    #             await message.channel.send(f'{target} does not exist!')
    #         write_db(database)
    
    write_db(database)


client.run(k)