
from asyncio.tasks import wait
import os
from web.things import *
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
import jsonpickle



stonklist = ['Weapon Factory', 'Real estate GRUNMORS', 'Spellfrik', 'Minekartellet uftevik', 'Bommulsprodusenten Øldal']

for stonkname in stonklist:
    drift = 0
    var = np.random.randn()
    var = var*np.sign(var)
    Stonk(stonkname, init_value = np.random.randint(1, 15), meanval = 0,  variance = var, drift = drift)


logging.basicConfig(filename='main.log', level=logging.DEBUG)

sio = socketio.Client(logger=logging)



def run():
    sio.connect('http://127.0.0.1:5000', wait = True)
    while True:
        for stonk in Stonk.all_stonks:
            stonk.move_stonks()
        sio.emit('stonk_values', Stonk.get_all_stonks_info())
        sio.sleep(2)

sio.start_background_task(target = run)



def ticksystem():
    x = requests.get('http://localhost:5000/api/admin/performtick')
    time.sleep(1800)
    ticksystem()

t = threading.Thread(target=ticksystem)
t.daemon = True
t.start()



class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        members = self.get_all_members()
        with open('web/database.txt', 'r') as f:
            database = eval(f.read())
        for member in members:
            role_names = [role.name for role in member.roles]
            if member.name not in database:
                role_names = [role.name for role in member.roles]
                if 'Bots' in role_names:
                    pass
                else:
                    url = f'http://localhost:5000/api/admin/createuser/{member.name}'
                    requests.get(url)




intents = discord.Intents.default()
intents.members = True
client = MyClient(intents = intents)


@client.event
async def on_voice_state_update(member, before, after):
    print('Changed state: ' + member.name)
    # events_handler.coin_aggregation_members[member] = after

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    # if users[message.author.name]['rank'] == 1:
    #     await message.add_reaction('🥇')

    # if users[message.author.name]['rank'] == 2:
    #     await message.add_reaction('🥈')

    # if users[message.author.name]['rank'] == 3:
    #     await message.add_reaction('🥉')



    if message.content.startswith('!stats'):
        url = 'http://localhost:5000/api/admin/getinfo'
        users = requests.get(url).json()
        # url = 'http://localhost:5000/api/admin/writeinfouser'
        # x = requests.post(url, json = x)
        health = users[message.author.name]['health']
        dmg = users[message.author.name]['dmg']
        armor = users[message.author.name]['armor']
        value = users[message.author.name]['coins']
        ticket = users[message.author.name]['tickets']
        stonksDB = users[message.author.name]['stonksDB']
        health_regen = users[message.author.name]['health_regen']
        total_income = users[message.author.name]['total_income']
        maxtickets = users[message.author.name]['maxtickets']
        embed = discord.Embed(title=f"Balance", description=f"{message.author.name} current stats") #,color=Hex code

        embed.add_field(name=f"Current Health :heart:", value=f'{[round(health,2), health]}')
        embed.add_field(name=f"Coins: <:CBCcoin:831506214659293214> | <:CBCcoin:831506214659293214> :clock1:", value=f'{round(value,2)} | {total_income}]')
        embed.add_field(name=f"Max tickets :tickets ", value=f'{maxtickets} ')
        embed.add_field(name=f"Tickets :ticket", value=f'{ticket}')
        embed.add_field(name=f"Attack damage :crossed_swords: ", value=f'{dmg}')
        embed.add_field(name=f"Armor :shield: ", value=f'{armor}')
        embed.add_field(name=f"Health Regeneration :herb:", value=f'{health_regen}')

        stonks_msg = ""
        for stonk in stonksDB:
            for st in Stonk.all_stonks:
                if stonk == st.name:
                    stonks_msg += f" {stonk}: {stonksDB[stonk]} [{round(st.current_price*stonksDB[stonk],2)} <:CBCcoin:831506214659293214>] |"
        embed.add_field(name=f"Stonks", value=f'{stonks_msg} .')
        await message.channel.send(embed=embed)


    if message.content.startswith('!factionstats'):
        with open('web/factions.txt', 'r') as f:
            database = eval(f.read())
        url = 'http://localhost:5000/api/admin/getinfo'
        users = requests.get(url).json()
        # url = 'http://localhost:5000/api/admin/writeinfouser'
        # x = requests.post(url, json = x)

        if users[message.author.name]['faction'] == None:
            await message.channel.send(f'You are not part of a faction!')
        else:
            
            current_health = database[users[message.author.name]['faction']]['current_health']
            maxtickets = database[users[message.author.name]['faction']]['maxtickets']
            tickets = database[users[message.author.name]['faction']]['tickets']
            armor = database[users[message.author.name]['faction']]['armor']
            maxhp = database[users[message.author.name]['faction']]['maxhp']
            health_regen = database[users[message.author.name]['faction']]['health_regen']
            dmg = database[users[message.author.name]['faction']]['dmg']


            embed = discord.Embed(title=f"Balance", description=f"{users[message.author.name]['faction']} current stats") #,color=Hex code
            
            embed.add_field(name=f"Current Health", value=f'{[round(current_health,2), maxhp]} :heart:')
            embed.add_field(name=f"Max Tickets", value=f'{maxtickets} :tickets: ')
            embed.add_field(name=f"Tickets: ", value=f'{tickets} :ticket:')
            embed.add_field(name=f"Armor: ", value=f'{armor} :shield:')
            embed.add_field(name=f"Health Regenation: ", value=f'{health_regen} :herb:')
            embed.add_field(name=f"Damage: ", value=f'{dmg} :crossed_swords:')
            await message.channel.send(embed=embed)


    if message.content.startswith('!attack'):
        msgsplit = message.content.split(' ')
        atknumber = int(msgsplit[1])
        if len(msgsplit) > 2 or len(msgsplit) < 2:
            await message.channel.send(f'Too many or few arguments. Use !attack <index>')
        else:
            with open('web/website.txt', 'r') as f:
                web = f.read() 
            url = f'http://localhost:5000/api/mob/generate/{message.author.name}/{atknumber}'
            response = requests.get(url).json()
            if response['info'] == True:
                battleid = response['id']
                embed = discord.Embed(title=f"Attack message", description=f"{message.author.name} attacked {response['name']} {response['battlereport']} | {web}/mob/{battleid}") #,color=Hex code
                file = discord.File(f"web/static/{response['img']}", filename=f"web/static/{response['img']}")
                await message.channel.send(file = file, embed=embed)
            else:
                await message.channel.send(f'{message.author.name} does not have enough hp or tickets.')


    if message.content.startswith('!raid'):
        msgsplit = message.content.split(' ')
        atknumber = int(msgsplit[1])
        if len(msgsplit) > 2 or len(msgsplit) < 2:
            await message.channel.send(f'Too many or few arguments. Use !raid <index>')
        else:
            with open('web/website.txt', 'r') as f:
                web = f.read() 
            url = 'http://localhost:5000/api/admin/getinfo'
            users = requests.get(url).json()
            if users[message.author.name]['faction'] == None:
                await message.channel.send(f'{message.author.name} need to be a member of a faction to perform raids!')
            else:
                if users[message.author.name]['faction'] == 'The Resistance':
                    url = f'http://localhost:5000/api/boss/generate/1/{atknumber}'
                else:
                    url = f'http://localhost:5000/api/boss/generate/2/{atknumber}'
                response = requests.get(url).json()
                if response['info'] == True:
                    battleid = response['id']
                    embed = discord.Embed(title=f"Raid message", description=f"{users[message.author.name]['faction']} raided {response['name']} | {response['battlereport']} {web}/boss/{battleid}") #,color=Hex code
                    file = discord.File(f"web/static/{response['img']}", filename=f"web/static/{response['img']}")
                    await message.channel.send(file = file, embed=embed)
                else:
                    await message.channel.send(f'{message.author.name} does not have enough hp or tickets.')

    
    if message.content.startswith('!join'):
        msgsplit = message.content.split(' ')
        if len(msgsplit) > 2 or len(msgsplit) < 2:
            await message.channel.send(f'Too many or few arguments. Use !join <faction> | resistance/council')
        else:
            url = 'http://localhost:5000/api/admin/getinfo'
            users = requests.get(url).json()
            faction = msgsplit[1]
            if faction == 'resistance' or faction == 'council':
                if users[message.author.name]['faction'] == None:
                    if faction == 'resistance':
                        embed = discord.Embed(title=f"Faction message", description=f"{message.author.name} joined The Resistance!") #,color=Hex code
                        users[message.author.name]['faction'] = 'The Resistance'
                        file = discord.File("web/static/faction_resistance.png", filename="web/static/faction_resistance.png")
                        await message.channel.send(file = file, embed=embed)
                        url = 'http://localhost:5000/api/admin/writeinfouser'
                        requests.post(url, json = users)
                    if faction == 'council':
                        embed = discord.Embed(title=f"Faction message", description=f"{message.author.name} joined The High Council!") #,color=Hex code
                        users[message.author.name]['faction'] = 'The High Council'
                        file = discord.File("web/static/faction_high_council.png", filename="web/static/faction_high_council.png")
                        await message.channel.send(file = file, embed=embed)
                        url = 'http://localhost:5000/api/admin/writeinfouser'
                        requests.post(url, json = users)
                else:
                    await message.channel.send(f'You are already part of a faction!')
            else:
                await message.channel.send(f'This faction does not exist!, use !join resistance or !join council')


    if message.content.startswith('!top'):
        url = 'http://localhost:5000/api/admin/getinfo'
        users = requests.get(url).json()
        temp_stats  = {}
        for user in users:
            power = users[user]['health'] + users[user]['maxhealth'] + users[user]['armor'] + users[user]['dmg'][0] + users[user]['dmg'][1] + users[user]['health_regen'] + users[user]['coins']
            tot_stonksval = 0
            for stonk in users[user]['stonksDB']:
                for st in Stonk.all_stonks:
                    if stonk == st.name:
                        tot_stonksval += round(st.current_price*users[user]['stonksDB'][st.name],2)
            temp_stats[user] = power + tot_stonksval

        index = 1
        embed = discord.Embed(title="Top players", description="Users with most power") #,color=Hex code
        medaljonger = [':first_place:', ':second_place:', ':third_place:']
        for key in sorted(temp_stats, key=temp_stats.get, reverse=True):
            if (index < 11):
                if index < 4:
                    embed.add_field(name=f"{index}{medaljonger[index-1]}. {key}", value=f'{temp_stats[key]} :zap:')
                else:
                    embed.add_field(name=f"{index}. {key}", value=f'{temp_stats[key]} :zap:')
            else:
                await message.channel.send(embed=embed)
                return
            index += 1

    
    if message.content.startswith('!shop'):
        embed = discord.Embed(title="Shop items", description="Current items in the shop") #,color=Hex code
        with open('web/items_shop.txt', 'r') as f:
            shopitems = eval(f.read())
        
        for index, item in enumerate(shopitems):
            embed.add_field(name=f"{index+1}. {item} | Cost: {shopitems[item]['cost']} <:CBCcoin:831506214659293214>", value=f'{shopitems[item]["health"]} :heart: | {shopitems[item]["dmg"]} :crossed_swords: | {shopitems[item]["armor"]} :shield: | {shopitems[item]["coinpertick"]} :clock1: | {shopitems[item]["health_regen"]} :herb: ')
        
        await message.channel.send(embed=embed)



    if message.content.startswith('!buy'):
        msgsplit = message.content.split(' ')
        if len(msgsplit) > 3 or len(msgsplit) < 3:
            await message.channel.send(f'Too many or few arguments. Use !buy <index> <amount>')
        else:
            choosenitem = int(msgsplit[1])*np.sign(int(msgsplit[1]))
            amount = int(msgsplit[2])*np.sign(int(msgsplit[2]))
            with open('web/items_shop.txt', 'r') as f:
                shopitems = eval(f.read())
            
            for index, item in enumerate(shopitems):
                index += 1
                if index == choosenitem:
                    url = 'http://localhost:5000/api/admin/getinfo'
                    users = requests.get(url).json()
                    user_current_money = users[message.author.name]['coins']
                    if (shopitems[item]['cost']*amount) <= user_current_money:
                        users[message.author.name]['coins'] -= float(round((shopitems[item]['cost']*amount),2))

                        if item in users[message.author.name]['itemsDB']:
                            users[message.author.name]['itemsDB'][item] += int(amount)
                        else:
                            users[message.author.name]['itemsDB'][item] = int(amount)
                        
                        url = 'http://localhost:5000/api/admin/writeinfouser'
                        requests.post(url, json = users)
                        await message.channel.send(f'{message.author.name} bought {amount} {item} for {round(float(shopitems[item]["cost"]*amount),2)} <:CBCcoin:831506214659293214>.')
                        return
                        
                    else:
                        await message.channel.send(f'{message.author.name} does not have coins <:CBCcoin:831506214659293214>.')
                        return
        await message.channel.send(f'Item does not exist, retard.')
            

    if message.content.startswith('!items'):

        with open('web/items_low.txt', 'r') as f:
            itemslist_low = eval(f.read())
        
        with open('web/items_med.txt', 'r') as f:
            itemslist_med = eval(f.read())

        with open('web/items_med.txt', 'r') as f:
            itemslist_high = eval(f.read())
        
        with open('web/items_shop.txt', 'r') as f:
            itemslist_shop = eval(f.read())

        url = 'http://localhost:5000/api/admin/getinfo'
        users = requests.get(url).json()

        itemlist = users[message.author.name]['itemsDB']

        embed = discord.Embed(title=f"Item list", description=f"{message.author.name} current items.") #,color=Hex code
        for item in itemlist:
            if item in itemslist_low:
                health = itemslist_low[item]['health']
                dmg = itemslist_low[item]['dmg']
                armor = itemslist_low[item]['armor']
                coinpertick = itemslist_low[item]['coinpertick']
                health_regen = itemslist_low[item]['health_regen']
                embed.add_field(name=f"{item} {itemlist[item]}", value=f'{health} :heart:| {dmg} :crossed_swords: | {armor} :shield: | {coinpertick} :clock1:| {health_regen} :herb:')
            if item in itemslist_med:
                health = itemslist_med[item]['health']
                dmg = itemslist_med[item]['dmg']
                armor = itemslist_med[item]['armor']
                coinpertick = itemslist_med[item]['coinpertick']
                health_regen = itemslist_med[item]['health_regen']
                embed.add_field(name=f"{item} {itemlist[item]}", value=f'{health} :heart:| {dmg} :crossed_swords: | {armor} :shield: | {coinpertick} :clock1:| {health_regen} :herb:')
            if item in itemslist_high:
                health = itemslist_high[item]['health']
                dmg = itemslist_high[item]['dmg']
                armor = itemslist_high[item]['armor']
                coinpertick = itemslist_high[item]['coinpertick']
                health_regen = itemslist_high[item]['health_regen']
                embed.add_field(name=f"{item} {itemlist[item]}", value=f'{health} :heart: | {dmg} :crossed_swords: | {armor} :shield: | {coinpertick} :clock1:| {health_regen} :herb:')
            if item in itemslist_shop:
                health = itemslist_shop[item]['health']
                dmg = itemslist_shop[item]['dmg']
                armor = itemslist_shop[item]['armor']
                coinpertick = itemslist_shop[item]['coinpertick']
                health_regen = itemslist_shop[item]['health_regen']
                embed.add_field(name=f"{item} {itemlist[item]}", value=f'{health} :heart: | {dmg} :crossed_swords: | {armor} :shield: | {coinpertick} :clock1:| {health_regen} :herb:')
        await message.channel.send(embed=embed)

    
    if message.content.startswith('!stonkbuy'):
        msgsplit = message.content.split(' ')
        if len(msgsplit) > 3 or len(msgsplit) < 3:
            await message.channel.send(f'Too many or few arguments. Use !stonkbuy <index> <amount>')
        else:
            choosenitem = int(msgsplit[1])*np.sign(int(msgsplit[1]))
            amount = int(msgsplit[2])*np.sign(int(msgsplit[2]))
            
            for index, item in enumerate(Stonk.all_stonks):
                index += 1
                if index == choosenitem:
                    url = 'http://localhost:5000/api/admin/getinfo'
                    users = requests.get(url).json()
                    user_current_money = users[message.author.name]['coins']
                    price = float(round((item.current_price*amount),2))
                    if (item.current_price*amount) <= user_current_money:
                        users[message.author.name]['coins'] -= price

                        if item in users[message.author.name]['itemsDB']:
                            users[message.author.name]['stonksDB'][item.name] += int(amount)
                        else:
                            users[message.author.name]['stonksDB'][item.name] = int(amount)
                        
                        url = 'http://localhost:5000/api/admin/writeinfouser'
                        requests.post(url, json = users)
                        await message.channel.send(f'{message.author.name} bought {amount} {item.name} for {price} <:CBCcoin:831506214659293214>.')
                        return
                        
                    else:
                        await message.channel.send(f'{message.author.name} does not have coins <:CBCcoin:831506214659293214>.')
                        return
        await message.channel.send(f'Item does not exist, retard.')


    if message.content.startswith('!stonksell'):
        msgsplit = message.content.split(' ')
        if len(msgsplit) > 3 or len(msgsplit) < 3:
            await message.channel.send(f'Too many or few arguments. Use !stonksell <index> <amount>')
        else:
            choosenitem = int(msgsplit[1])*np.sign(int(msgsplit[1]))
            amount = int(msgsplit[2])*np.sign(int(msgsplit[2]))
            
            for index, item in enumerate(Stonk.all_stonks):
                index += 1
                if index == choosenitem:
                    url = 'http://localhost:5000/api/admin/getinfo'
                    users = requests.get(url).json()
                    user_current_amount = users[message.author.name]['stonksDB'][item.name]
                    price = float(round((item.current_price*amount),2))
                    if amount <= user_current_amount:
                        users[message.author.name]['coins'] += price
                        users[message.author.name]['stonksDB'][item.name] -= int(amount)

                        url = 'http://localhost:5000/api/admin/writeinfouser'
                        requests.post(url, json = users)
                        await message.channel.send(f'{message.author.name} sold {amount} {item.name} for {price} <:CBCcoin:831506214659293214>.')
                        return
                        
                    else:
                        await message.channel.send(f'{message.author.name} does not have coins <:CBCcoin:831506214659293214>.')
                        return
        await message.channel.send(f'Item does not exist, retard.')


    if message.content.startswith('!web'):
        website = ""
        await message.channel.send(website)
    


client.run(k)

# print('wdwd')

# url = 'http://localhost:5000/api/admin/getinfo'

# x = requests.get(url).json()

# url = 'http://localhost:5000/api/admin/writeinfouser'

# x = requests.post(url, json = x)

# print(x)

# for stonk in Stonk.all_stonks:
#     stonk.move_stonks()
#     sio.emit('stonk_values', Stonk.get_all_stonks_info())


# sio.emit('stonk_values', 'test')

# def ticksystem():
#     x = requests.get('http://localhost:5000/api/admin/performtick')
#     time.sleep(5)
#     ticksystem()


