
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
import concurrent.futures
from skimage.morphology import disk
from skimage.filters.rank import mean
import requests
import base64
import io 

# client = commands.Bot(command_prefix='!')

#https://discordapp.com/developers



shop_items = {'Snake gun': [10, 100, 1, ':snake:'], 
                'Revolver': [24, 200, 2, ':gun:'], 
                'Acid dispenser': [38, 300, 3, ':leafy_green:'], 
                'Ak47': [173, 950, 4, '<:ak47_emo_:850128015837102112>'], 
                'Battlecruiser': [610 , 3100, 5, ':ship:'],
                'Ahegao Princess': [6100 , 25000, 6, '<:aegao:849030455189438485>']
                }

class Database:
    def __init__(self):
        self.dbName = 'crazy_blazin_database.txt' 
    def read(self):
        with open(self.dbName, 'r') as f:
            return eval(f.read())

    def write(self, users):
        with open(self.dbName, 'w') as f:
            f.write(str(users))




class EventHandler:
    def __init__(self):
        self.events = []
        self.coin_aggregation_members = {}
        self.db = Database()
        self.boosted_channels = []
        self.lootbox = ''
        self.imageofthedayunlocket = False
        self.imageunlocketby = ''
    
    def current_events(self):
        if len(self.events) < 1:
            return 'No events active'
        else:
            return self.events

    def add_event(self, ticket):
        self.events.append(ticket)

    def raffle_machine(self, event):
        winner = np.random.choice(event.participants, 1)
        return winner

    def coin_aggregation(self):
        users = self.db.read()

        for members in self.coin_aggregation_members:
        #     if members not in users:
        #         users[members] = {'Coins': 500, 'Tickets': 1, 'Timer': 0, 'BoostTimer': 0, 'Boosters': 0, 'Actives': [], 'weapons': {'Kick': [2, 1, ':foot:']}}
        #         users[members]['Actives'] = []

            state = self.coin_aggregation_members[members]
            channel_state = str(state.channel)
            stream_state = state.self_stream

            # if channel_state in self.boosted_channels:
            #     if 'Boosted' not in users[members]['Actives']:
            #         users[members]['Actives'].append('Boosted')
            #     else:
            #         pass
            #     print(f'{members} is boosted')
            # else:
            #     users[members]['Actives'] = []

            if channel_state != 'None':
                if stream_state:
                    try:
                        users[members]['Coins'] = round(users[members]['Coins'] + 1, 2)
                    except KeyError as msg:
                        print(msg)
                        pass
                    print(f'Stream activity: {members}')
                else:
                    try:
                        users[members]['Coins'] = round(users[members]['Coins'] + 0.33, 2)
                    except KeyError as msg:
                        print(msg)
                        pass
                print(f'Coins to : {members}')

        self.db.write(users)
        # return users


class Gullfugl:
    def __init__(self):
        self.dmglog = {}
        self.name_list = ['An armored gullfugl', 'A cute gullfugl', 'A rare gullfugl', 'A retarded gullfugl']
        self.name = np.random.choice(self.name_list, 1)[0]
        self.hp = np.random.randint(500,25000)
        self.drop = self.hp*0.1



class Stonks:
    ind = 0
    stonks = []
    def __init__(self, name = 'Cocaine', init_price = 53, drift = 0.002, mean = 0, variance = 1, include_order = True):
        self.price = [init_price]
        self.current_price = self.price[-1]
        self.name = name
        self.variance = variance
        self.mean = mean
        self.drift = drift
        self.include_order = include_order
        self.stonks.append(self)

    
    def move_price(self):
        if self.include_order:
            self.price.append(round(self.drift + self.price[-1] + np.random.normal(self.mean, self.variance), 2))
        else:
            self.price.append(round(self.drift + np.random.normal(self.mean, self.variance), 2))
        price_collapse = False
        if self.price[-1] <= 0:
            if self.include_order:
                self.price[-1] = 153
            else:
                self.price[-1] = 1
            price_collapse = True

        self.current_price = round(self.price[-1], 2)
        self.price_collaps = price_collapse
        return price_collapse

    @staticmethod
    def plot_results():
        Stonks.ind += 1
        fig, ax = plt.subplots(1, len(Stonks.stonks))
        colors = ['black', 'black']
        color_tip = ['red', 'blue']
        volatility = ['Small', 'Large']
        two_stonks = []
        for i, stonk in enumerate(Stonks.stonks):
            two_stonks.append(stonk.price[-1000:])
            ax[i].plot(stonk.price[-1000:], linewidth = 1, color = colors[i])
            ax[i].plot(len(stonk.price[-1000:])-1, stonk.current_price, 'o', color = color_tip[i])
            if stonk.price_collaps:
                ax[i].plot(len(stonk.price[-1000:])-1, stonk.current_price, 'x', color = 'red', fillstyle = 'none', markersize = 15)
            else:
                ax[i].plot(len(stonk.price[-1000:])-1, stonk.current_price, 'o', color = color_tip[i], fillstyle = 'none', markersize = 10)
                ax[i].plot(len(stonk.price[-1000:])-1, stonk.current_price, 'o', color = color_tip[i], fillstyle = 'none', markersize = 15)
            ax[i].set_title(f'{i+1}. {stonk.name} \n price: {stonk.current_price} \n Volatility: {volatility[i]}')
            ax[i].set_ylabel('Crazy blazin coins')
            ax[i].set_xlabel('Time')
        plt.tight_layout()
        plt.savefig('stonk.jpg')
        plt.close()

        x_vals = [x for x in range(0, len(two_stonks[0]))]
        sio.emit('msg', {'x': x_vals, 'y1': two_stonks[0], 'y2': two_stonks[1]})



cocaine = Stonks(name = 'Cocaine', init_price = 1, drift = 0, mean = 3, variance = 2, include_order = False)
Ingamersh = Stonks(name = 'Ingamersh verksted', init_price = 128.8, drift = 0.15, variance = 50)


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # an attribute we can access from our task
        self.counter = 0
        # start the task to run in the background
        self.add_coins_after_time.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        users = events_handler.db.read()

        members = self.get_all_members()
        for member in members:
            if member.name not in users:
                users[member.name] = {'Coins': 500, 'Tickets': 1, 'Timer': 0, 'BoostTimer': 0, 'Boosters': 0, 'Actives': [], 'weapons': {'Kick': [2, 1, ':foot:']}}
            if 'cocaine' not in users[member.name]:
                users[member.name]['cocaine'] = 0
            if 'ingamersh' not in users[member.name]:
                users[member.name]['ingamersh'] = 0
            


        members = self.get_all_members()
        for member in members:
            role_names = [role.name for role in member.roles]
            if 'Bots' in role_names:
                 users.pop(member.name, None)
        events_handler.db.write(users)



    @tasks.loop(seconds=30) # task runs every 60 seconds
    async def add_coins_after_time(self):
        events_handler.coin_aggregation()
        users = events_handler.db.read()
        print('Coins distributed!')

        for key in users:
            tot_dmg = 0
            for weapon in users[key]['weapons']:
                tot_dmg += users[key]['weapons'][weapon][0]*users[key]['weapons'][weapon][1]
            users[key]['tot_dmg'] = tot_dmg

        members = self.get_all_members()
        for member in members:
            role_names = [role.name for role in member.roles]
            if 'Bots' in role_names:
                 users.pop(member.name, None)

        for member in members:
            if member.name not in users:
                users[member.name] = {'Coins': 500, 'Tickets': 1, 'Timer': 0, 'BoostTimer': 0, 'Boosters': 0, 'Actives': [], 'weapons': {'Kick': [2, 1, ':foot:']}}
            if 'cocaine' not in users[member.name]:
                users[member.name]['cocaine'] = 0
            if 'ingamersh' not in users[member.name]:
                users[member.name]['ingamersh'] = 0
            if 'rank' not in users[member.name]:
                users[member.name]['rank'] = 100
            

        probability = np.random.randint(1, 1001)
        for key in users:
            if 'Timer' in users[key]:
                if users[key]['Timer'] > 0:
                    users[key]['Timer'] -= 30
                else:
                    print(key, users[key]['Timer'])
                    users[key]['Timer'] = 0
                    # next(user for user in client.users if user.name == key)
                    for member in members:
                        if member.name == key:
                            role_names = [role.name for role in member.roles]
                            if 'Crazy Blazin Gold' in role_names:
                                role = get(member.guild.roles, name='Crazy Blazin Gold')
                                await member.remove_roles(role)
        events_handler.db.write(users)

        # members = self.get_all_members()
        # for key in users:
        #     if 'BoostTimer' in users[key]:
        #         if users[key]['BoostTimer'] > 0:
        #             users[key]['BoostTimer'] -= 30
        #         else:
        #             users[key]['BoostTimer'] = 0
        #             users[key]['Active'] = '0'
        #             # next(user for user in client.users if user.name == key)
        #             for member in members:
        #                 if member.name == key:
        #                     role_names = [role.name for role in member.roles]
        #                     if 'Booster' in role_names:
        #                         print('Removing booster role')
        #                         role = get(member.guild.roles, name='Booster')
        #                         await member.remove_roles(role)
            
        print(probability)
        if probability >= 995:
            channel = client.get_channel(849752403687374899)
            # channel = client.get_channel(734481490431443068)
            events_handler.gullfugl = Gullfugl()

            event = []
            shuffled_users = []

            lock = True
            for key in users:
                shuffled_users.append(key)
            np.random.shuffle(shuffled_users)
            print(shuffled_users)
            super_tot_dmg = 0
            for key in shuffled_users:
                tot_dmg = 0
                for weapon in users[key]['weapons']:
                    dmg = users[key]['weapons'][weapon][0]
                    amount = users[key]['weapons'][weapon][1]
                    tot_dmg += dmg*amount
                super_tot_dmg += tot_dmg
                events_handler.gullfugl.hp -= tot_dmg

                if events_handler.gullfugl.hp <= 0 and lock:
                    lock = False
                    winner = key
                    users[key]['Coins'] += events_handler.gullfugl.drop
                    users[key]['Coins'] = round(users[key]['Coins'],2)
                    event.append([key, tot_dmg, ':crossed_swords: :boom:'])
                else:
                    event.append([key, tot_dmg, ':crossed_swords:'])
            if lock:
                embed = discord.Embed(title=f"Gullfugl event! :baby_chick: Health left: {events_handler.gullfugl.hp}| Total damage dealt: {super_tot_dmg}", description=f"{events_handler.gullfugl.name} :baby_chick: has been observed, but no one managed to shoot it!") #,color=Hex code
            else:
                embed = discord.Embed(title=f"Gullfugl event! :baby_chick: Health left: {events_handler.gullfugl.hp}| Total damage dealt: {super_tot_dmg}", description=f"{events_handler.gullfugl.name} appeared, {winner} shot :baby_chick: and looted {events_handler.gullfugl.drop} <:CBCcoin:831506214659293214>! ") #,color=Hex code
            for ev in event:
                embed.add_field(name=f"{ev[0]}: ", value=f'{ev[1]} {ev[2]}')
            await channel.send(embed=embed)


        channel = client.get_channel(803982821923356773)
        # channel = client.get_channel(795738540251545620)
        bankrupcy_lock = False
        for key in users:
            if users[key]['cocaine'] > 0:
                bankrupcy_lock = True
                break
            
        for stonk in Stonks.stonks:
            price_collapse = stonk.move_price() # move cocaine price
            if price_collapse: # Remove all if price collapse
                for key in users:
                    if stonk.name == 'Ingamersh verksted':
                        users[key]['ingamersh'] = 0
                        if bankrupcy_lock:
                            embed = discord.Embed(title=f"Bankrupt!", description=f"We are sorry, but {stonk.name} is bankrupt and everyone lost all their shares!") #,color=Hex code
                            embed.set_image(url="https://media.giphy.com/media/3oriO5t2QB4IPKgxHi/giphy.gif")
                            await channel.send(embed=embed)
                    if stonk.name == 'Cocaine':
                        if bankrupcy_lock:
                            embed = discord.Embed(title=f"Police raid!", description=f"Police have found every owner of cocaine. Everyone lost their cocaine!") #,color=Hex code
                            embed.set_image(url="https://media.giphy.com/media/7wouU3i8xWB0I/giphy.gif")
                            await channel.send(embed=embed)
                        users[key]['cocaine'] = 0
    
        Stonks.plot_results()


        index = 0
        temp_stats = {}
        for key_user in users:
            if 'tot_dmg' not in users[key_user]:
                pass
            else:
                temp_stats[key_user] = users[key_user]['tot_dmg']
        for key in sorted(temp_stats, key=temp_stats.get, reverse=True):
            if (index < 5):
                index += 1
                users[key]['rank'] = index
            else:
                break
        
        events_handler.db.write(users)
        return users
                        # To force voice state changes for instant changes in boosting roles

    @add_coins_after_time.after_loop
    async def after_my_task(self):
        print('help im being violated')
        if (self.add_coins_after_time.is_being_cancelled()):
            print('cancelled')

    @add_coins_after_time.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in


events_handler = EventHandler()
intents = discord.Intents.default()
intents.members = True
client = MyClient(intents = intents)
sio = socketio.Client()

import threading

def run():
    sio.connect('http://127.0.0.1:5000')
    sio.wait()

t = threading.Thread(target=run)
t.daemon = True
t.start()

class Ticket:
    def __init__(self, description, id, creator):
        self.description = description
        self.id = id
        self.participants = []
        self.creator = creator


@client.event
async def on_voice_state_update(member, before, after):
    member = str(member).split("#")[0]
    print('Changed state: ' + member)
    events_handler.coin_aggregation_members[member] = after

    users = events_handler.db.read()

    # events_handler.boosted_channels = []

    # for mem in members:
    #     if str(mem.name) in users:
    #         if 'Active' in users[str(mem.name)]:
    #             if users[str(mem.name)]['Active'] == 'Booster':
    #                 if mem.voice not in events_handler.boosted_channels:
    #                     if str(mem.voice) != 'None':
    #                         events_handler.boosted_channels.append(str(mem.voice.channel))

    # members = client.get_all_members()
    # for mem in members:
    #     if str(mem.voice) != 'None':
    #         if str(mem.voice.channel) in events_handler.boosted_channels:
    #             role = get(mem.guild.roles, name='Boosted')
    #             await mem.add_roles(role)
    #         else:
    #             role = get(mem.guild.roles, name='Boosted')
    #             await mem.remove_roles(role)
    #     else:
    #         role = get(mem.guild.roles, name='Boosted')
    #         await mem.remove_roles(role)
    
    events_handler.db.write(users)
    


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    users = events_handler.db.read()
    try:
        if users[message.author.name]['rank'] == 1:
            await message.add_reaction('🥇')

        if users[message.author.name]['rank'] == 2:
            await message.add_reaction('🥈')

        if users[message.author.name]['rank'] == 3:
            await message.add_reaction('🥉')
    except KeyError as msg:
        print(msg)


    if message.content.startswith('!bal'):
        users = events_handler.db.read()
        value = users[message.author.name]['Coins']
        ticket = users[message.author.name]['Tickets']
        cocaine_wealth = users[message.author.name]['cocaine']
        ingamersh_wealth = users[message.author.name]['ingamersh']
        embed = discord.Embed(title=f"Balance", description=f"{message.author.name} current balance") #,color=Hex code

        embed.add_field(name=f"<:CBCcoin:831506214659293214> (CBC)", value=f'{round(value,2)}')
        embed.add_field(name=f":tickets: (tickets)", value=f'{ticket}')
        embed.add_field(name=f":salt: (cocaine)", value=f'{cocaine_wealth} worth: {round(cocaine_wealth*cocaine.current_price,2)} <:CBCcoin:831506214659293214>')
        embed.add_field(name=f":house_with_garden:  (Ingamersh verksted)", value=f'{ingamersh_wealth} worth: {round(ingamersh_wealth*Ingamersh.current_price,2)} <:CBCcoin:831506214659293214>')
        tot_dmg = 0
        for weapon in users[message.author.name]['weapons']:
            # [shop_items[weapon][1], amount]
            if len(users[message.author.name]['weapons'][weapon]) < 3:
                embed.add_field(name=f"{weapon} :foot: :", value=f"{users[message.author.name]['weapons'][weapon][1]}")
            else:
                embed.add_field(name=f"{weapon} {users[message.author.name]['weapons'][weapon][2]}:", value=f"{users[message.author.name]['weapons'][weapon][1]}")
            tot_dmg += users[message.author.name]['weapons'][weapon][0]*users[message.author.name]['weapons'][weapon][1]
        embed.add_field(name=f"Total damage: ", value=f"{tot_dmg} :crossed_swords:")
        # embed.add_field(name=f":pill: (boosts)", value=f'{boosts}')
        await message.channel.send(embed=embed)



    if message.content.startswith('!top'):
        users = events_handler.db.read()
        index = 1
        embed = discord.Embed(title="Top damage dealers", description="Users with highest damage") #,color=Hex code
        medaljonger = [':first_place:', ':second_place:', ':third_place:']
        temp_stats = {}
        for key_user in users:
            temp_stats[key_user] = users[key_user]['tot_dmg']
        for key in sorted(temp_stats, key=temp_stats.get, reverse=True):
            if (index < 11):
                if index < 4:
                    embed.add_field(name=f"{index}{medaljonger[index-1]}. {key}", value=f'{users[key]["tot_dmg"]} :crossed_swords:')
                else:
                    embed.add_field(name=f"{index}. {key}", value=f'{users[key]["tot_dmg"]} :crossed_swords:')
            else:
                await message.channel.send(embed=embed)
                return
            index += 1


    if message.content.startswith('!relief'):
        str_split = message.content.split(' ')
        amount = int(str_split[1])
        role_names = [role.name for role in message.author.roles]
        if 'Admin' in role_names:
            users = events_handler.db.read()
            for key_user in users:
                users[key_user]['Coins'] += amount
            events_handler.db.write(users)
            await message.channel.send(f'The resistance has delived {amount} <:CBCcoin:831506214659293214> to the poor.')
        else:
            await message.channel.send(f'You need to be admin for this command!')


    if message.content.startswith('!raffle'):
        str_split = message.content.split(' ')
        if len(str_split) < 2:
            await message.channel.send(f'Few arguments. Use !raffle description')

        description = ''
        for idx in range(1, len(str_split)):
            description += str_split[idx] + ' '

        role_names = [role.name for role in message.author.roles]
        if 'SOMEROLE' in role_names or 'Admin' in role_names:
            ticket = Ticket(description, len(events_handler.events)+1, message.author.name)
            embed = discord.Embed(title=f"Raffle ----Raffle startet! [ID {ticket.id}]----", description=f"{description}") #,color=Hex code
            events_handler.add_event(ticket)
            embed.add_field(name=f"Info: ", value=f"""
            1. You need at least 1 :tickets: to join, but adding more ticket increases chance to win.
            2. To join raffle use !join raffleID amount
            """)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(f'You need to have admin role to start raffles!')

    if message.content.startswith('!events'):
        with open('crazy_blazin_database.txt', 'r') as f:
            users = eval(f.read())
        for i, event in enumerate(events_handler.events):
            await message.channel.send(f'EventID: {i+1}, Price: {event.price} :tickets:,  Description: {event.description}')
        if len(events_handler.events) < 1:
            await message.channel.send(f'No events active.')
    
    if message.content.startswith('!join'):
        str_split = message.content.split(' ')
        if len(str_split) > 3 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !join raffleID ticket_amount')
        try:
            id = int(str_split[1])
            tickets = int(str_split[2])
        except ValueError:
            await message.channel.send(f'ID needs to be integer!')
        
        EVENT_FOUND = True
        for event in events_handler.events:
            if event.id == id:
                EVENT_FOUND = False
                if tickets <= users[message.author.name]['Tickets']:

                    users[message.author.name]['Tickets'] -= tickets
                    with open('crazy_blazin_database.txt', 'w') as f:
                        f.write(str(users))
                    if message.author.name in event.participants:
                        await message.channel.send(f'{message.author.name} added {tickets} :tickets: to the raffle!')
                    else:
                        await message.channel.send(f'{message.author.name} joined the raffle with {tickets} :tickets:')
                    for i in range(tickets):
                        event.participants.append(message.author.name)
                else:
                    await message.channel.send(f'You do not have enough :tickets: to join raffle!')
        
            counted_tickets = Counter(event.participants)

            embed = discord.Embed(title=f"Raffle {id}", description=f"{event.description}") #,color=Hex code
            for i, key in enumerate(sorted(counted_tickets, key=counted_tickets.get, reverse=True)):
                embed.add_field(name=f"{1+i} {key}", value=f'{counted_tickets[key]} :tickets: ')
            await message.channel.send(embed=embed)
            
        if EVENT_FOUND:
            await message.channel.send(f'This event does not exist!')

    if message.content.startswith('!startraffle'):
        str_split = message.content.split(' ')
        if len(str_split) > 2 or len(str_split) <= 1:
            await message.channel.send(f'Too many or few arguments. Use !startraffle ID')
        try:
            id = int(str_split[1])
        except ValueError:
            await message.channel.send(f'ID needs to be integer!')
        role_names = [role.name for role in message.author.roles]
        for event in events_handler.events:
            if event.id == id:
                if message.author.name in event.creator or 'Admin' in role_names:
                    await message.channel.send(f':giraffe: :giraffe: Raffle has begun!:giraffe: :giraffe: ')
                    time.sleep(3)
                    await message.channel.send(f':eye: :eye: READY!??:eye: :eye: ')
                    winner = events_handler.raffle_machine(event)
                    time.sleep(3)
                    await message.channel.send(f':partying_face:  :partying_face: WINNER IS: {winner[0]}! :partying_face:  :partying_face: ')
                    events_handler.events.remove(event)
                else:
                    await message.channel.send(f'You are not the raffle creator!')
        events_handler.db.write(users)


    if message.content.startswith('!buy tickets'):
        str_split = message.content.split(' ')
        if len(str_split) > 3 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !buy tickets amount')
        try:
            amount = int(str_split[2])
        except ValueError:
            await message.channel.send(f'amount needs to be integer!')

        if 100*amount <= users[message.author.name]['Coins']:

            users[message.author.name]['Tickets'] += amount
            users[message.author.name]['Coins'] -= 100*amount
            with open('crazy_blazin_database.txt', 'w') as f:
                f.write(str(users))
            await message.channel.send(f'{message.author.name} Bought {amount} :tickets: (tickets)')
            

        else:
            await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC) to buy {amount} :tickets:!')
            await message.channel.send(f'Price: <:CBCcoin:831506214659293214> (CBC) per :tickets: .')

        events_handler.db.write(users)


    if message.content.startswith('!buy CBG'):
        str_split = message.content.split(' ')
        if len(str_split) > 2 or len(str_split) < 1:
            await message.channel.send(f'Too many or few arguments. Use !buy CBCGold')

        if 1000 <= users[message.author.name]['Coins']:
            users[message.author.name]['Coins'] -= 1000

            member = message.author
            role = get(member.guild.roles, name='Crazy Blazin Gold')
            await member.add_roles(role)
            # await bot.remove_roles(user, 'member')
            await message.channel.send(f'{message.author.name} Bought Crazy Blazin Gold Role for one month!')

            users[message.author.name]['Timer'] = 2592000
            with open('crazy_blazin_database.txt', 'w') as f:
                f.write(str(users))

        else:
            await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC) to buy Crazy Blazin Gold!')
            await message.channel.send(f' Price: 500 <:CBCcoin:831506214659293214> (CBC).')
            
        events_handler.db.write(users)


    if message.content.startswith('!help'):
        await message.channel.send(f' See commands channel for help!')



    
    if message.content.startswith('!shop'):

        embed = discord.Embed(title=f"Weapon Shop", description=f"Weapons for damaging the gullfugl! To buy item use !buy weapons <index> <amount>") #,color=Hex code
        for weapon in shop_items:
            dmg = shop_items[weapon][0]
            cost = shop_items[weapon][1]
            index = shop_items[weapon][2]
            item_icon = shop_items[weapon][3]
            embed.add_field(name=f"{index}. {weapon} {item_icon}", value=f'Damage: {dmg} | Cost: {cost} <:CBCcoin:831506214659293214>')
        await message.channel.send(embed=embed)
        events_handler.db.write(users)

    if message.content.startswith('!buy weapons '):
        users = events_handler.db.read()
        str_split = message.content.split(' ')
        if len(str_split) > 4 or len(str_split) < 4:
            await message.channel.send(f'Too many or few arguments. Use !buy weapons <index> <amount>')
        else:
            index = int(str_split[2])*np.sign(int(str_split[2]))
            amount = int(str_split[-1])*np.sign(int(str_split[-1]))

            for weapon in shop_items:
                if shop_items[weapon][2] == index:
                    if shop_items[weapon][1]*amount <= users[message.author.name]['Coins']:
                        users[message.author.name]['Coins'] -= shop_items[weapon][1]*amount
                        await message.channel.send(f'{message.author.name} bought {amount} {weapon}{shop_items[weapon][3]} for {shop_items[weapon][1]*amount} <:CBCcoin:831506214659293214>')
                        if weapon not in users[message.author.name]['weapons']:
                            users[message.author.name]['weapons'][weapon] = [shop_items[weapon][0], amount, shop_items[weapon][3]]
                        else:
                            users[message.author.name]['weapons'][weapon][1] += amount
                            users[message.author.name]['weapons'][weapon][2] == shop_items[weapon][3]
                    else:
                        await message.channel.send(f'{message.author.name} can not afford this!')
        events_handler.db.write(users)


    if message.content.startswith('!stonks'):
        embed = discord.Embed(title=f"Stonks", description=f"Historical and current price of stonks. Buy item use !buy stonks <index> <amount> and !sell stonks <index> <amount>. You can view stonks in real time at http://5eb1bcab2782.ngrok.io/stonks") #,color=Hex code
        file = discord.File("stonk.jpg", filename="stonk.jpg")
        await message.channel.send(file = file, embed=embed)



    if message.content.startswith('!buy stonks'):
        users = events_handler.db.read()
        str_split = message.content.split(' ')
        if len(str_split) > 4 or len(str_split) < 4:
            await message.channel.send(f'Too many or few arguments. Use !buy stonks <index> <amount>')
        else:
            amount = int(str_split[3])*np.sign(int(str_split[3]))
            index = int(str_split[2])*np.sign(int(str_split[2]))
            if index == 1:
                if (users[message.author.name]['cocaine']+amount) <= 50:
                    price = round(cocaine.current_price*amount,2)
                    if price <= users[message.author.name]['Coins']:
                        price = round(cocaine.current_price*amount,2)
                        users[message.author.name]['cocaine'] += amount
                        users[message.author.name]['Coins'] -= price
                        await message.channel.send(f'{message.author.name} bought {amount} cocaine :salt: for {price} <:CBCcoin:831506214659293214> @ {round(cocaine.current_price,2)} per cocaine.')
                    else:
                        await message.channel.send(f'{message.author.name} can not afford this much cocaine!')
                else:
                    await message.channel.send(f'{message.author.name} The resistance does not want to make you an monopoly. You can hold max 50 cocaine!')
                
            if index == 2:
                price = round(Ingamersh.current_price*amount,2)
                if price <= users[message.author.name]['Coins']:
                    price = round(Ingamersh.current_price*amount,2)
                    users[message.author.name]['ingamersh'] += amount
                    users[message.author.name]['Coins'] -= price
                    await message.channel.send(f'{message.author.name} bought {amount} Ingamersh verksted :house_with_garden: for {price} <:CBCcoin:831506214659293214> @ {round(Ingamersh.current_price,2)} per Ingamersh verksted.')
                else:
                    await message.channel.send(f'{message.author.name} can not afford this much Ingamersh verksted!')

        events_handler.db.write(users)


    if message.content.startswith('!sell stonks'):
        users = events_handler.db.read()
        str_split = message.content.split(' ')
        if len(str_split) > 4 or len(str_split) < 4:
            await message.channel.send(f'Too many or few arguments. Use !sell stonks <index> <amount>')
        else:
            amount = int(str_split[3])*np.sign(int(str_split[3]))
            index = int(str_split[2])*np.sign(int(str_split[2]))
            if index == 1:
                price = round(cocaine.current_price*amount,2)
                if amount <= users[message.author.name]['cocaine']:
                    users[message.author.name]['cocaine'] -= amount
                    users[message.author.name]['Coins'] += price
                    await message.channel.send(f'{message.author.name} sold {amount} cocaine :salt: for {price} <:CBCcoin:831506214659293214> @ {round(cocaine.current_price,2)} per cocaine.')
                else:
                    await message.channel.send(f'{message.author.name} does not own this much cocaine!')
            if index == 2:
                price = round(Ingamersh.current_price*amount,2)
                if amount <= users[message.author.name]['ingamersh']:
                    price = round(Ingamersh.current_price*amount,2)
                    users[message.author.name]['ingamersh'] -= amount
                    users[message.author.name]['Coins'] += price
                    await message.channel.send(f'{message.author.name} sold {amount} Ingamers verksted :house_with_garden: for {price} <:CBCcoin:831506214659293214> @ {round(Ingamersh.current_price,2)} per Ingamersh verksted.')
                else:
                    await message.channel.send(f'{message.author.name} does not own this much Ingamers verksted!')

        events_handler.db.write(users)



    if message.content.startswith('!giveCBG'):
        members = client.get_all_members()
        str_split = message.content.split(' ')
        if len(str_split) > 2 or len(str_split) < 1:
            await message.channel.send(f'Too many or few arguments. Use !giveCBC username amount')
        try:
            user = str(str_split[1])
        except ValueError:
            await message.channel.send(f'value needs to be str!')
    
        role_names = [role.name for role in message.author.roles]
        if 'Admin' in role_names:
            for member in members:
                if member.name == user:
                    role = get(member.guild.roles, name='Crazy Blazin Gold')
                    await member.add_roles(role)
                    await message.channel.send(f'{member.name} recieved Crazy Blazin Gold Role for one month!')
                    users[member.name]['Timer'] = 2592000
        else:
            await message.channel.send('You need to be admin for this command')
        events_handler.db.write(users)


    if message.content.startswith('!giveCBC'):
        str_split = message.content.split(' ')
        print(str_split)
        print(len(str_split))
        if len(str_split) > 3 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !giveCBC username amount')
        try:
            amount = int(str_split[2])
        except ValueError:
            await message.channel.send(f'value needs to be integer!')

        role_names = [role.name for role in message.author.roles]
        reciever_user = str_split[1]
        if 'Admin' in role_names:
            for user in users:
                if user == reciever_user:
                    users[user]['Coins'] += amount
            await message.channel.send(f'{reciever_user} recieved {amount} <:CBCcoin:831506214659293214> (CBC)')
            with open('crazy_blazin_database.txt', 'w') as f:
                f.write(str(users))
        else:
            await message.channel.send('You need to be admin for this command')
        events_handler.db.write(users)
    
    if message.content.startswith('!givetickets'):
        str_split = message.content.split(' ')
        if len(str_split) > 3 or len(str_split) < 1:
            await message.channel.send(f'Too many or few arguments. Use !givetickets username amount')
        try:
            amount = int(str_split[2])
        except ValueError:
            await message.channel.send(f'value needs to be integer!')

        role_names = [role.name for role in message.author.roles]
        reciever_user = str_split[1]
        if 'Admin' in role_names:
            for user in users:
                if user == reciever_user:
                    users[user]['Tickets'] += amount
            await message.channel.send(f'{reciever_user} recieved {amount} :tickets: (tickets)')
        events_handler.db.write(users)


    if message.content.startswith('!donate'):
        str_split = message.content.split(' ')
        if len(str_split) > 3 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !donate target amount')
        else:
            amount = int(str_split[2])
            if amount >= 0:
                target = str(str_split[1])
                if users[message.author.name]['Coins'] >= amount:
                    for member in users:
                        if target == 'Carbonade' or target == 'Foxxravin':
                            users[member]['Coins'] += amount*0.80
                            users[message.author.name]['Coins'] -= amount
                            name = message.author.name
                            sio.emit('msg', {'name': name, 'amount': amount, 'img': "https://raw.githubusercontent.com/MartinRovang/CrazyBlazin/main/images/kris_slave.gif"})
                            await message.channel.send(f'{message.author.name} donated {amount} <:CBCcoin:831506214659293214> (CBC) to {member}')
                            break
                else:
                    await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC).')
        events_handler.db.write(users)

    
    if message.content.startswith('!imageoftheday'):

        if events_handler.imageofthedayunlocket:
            users[message.author.name]['Coins'] -= 100
            embed = discord.Embed(title=f"IMAGE OF THE DAY", description=f"Unlocked by: {events_handler.imageunlocketby}") #,color=Hex code
            embed.add_field(name=f"Add your own: ", value=f'You can add your own image of the day with command: !addimageoftheday <link> price: 400 <:CBCcoin:831506214659293214> (CBC)')
            file = discord.File("imgoftheday.jpg", filename="imgoftheday.jpg")
            await message.channel.send(file = file, embed=embed)
        else:
            embed = discord.Embed(title=f"IMAGE OF THE DAY", description=f"Unlock image of the day for 100 <:CBCcoin:831506214659293214> (CBC). ") #,color=Hex code
            embed.add_field(name=f"Command: ", value=f'!unlock imageoftheday')
            embed.add_field(name=f"Add your own: ", value=f'You can add your own image of the day with command: !addimageoftheday <link> price: 400 <:CBCcoin:831506214659293214> (CBC)')
            file = discord.File("imgoftheday_blurred.jpg", filename="imgoftheday_blurred.jpg")
            await message.channel.send(file = file, embed=embed)
        events_handler.db.write(users)




    if message.content.startswith('!unlock imageoftheday'):

        if 100 <= users[message.author.name]['Coins']:
            users[message.author.name]['Coins'] -= 100
            events_handler.imageofthedayunlocket = True
            events_handler.imageunlocketby = message.author.name
            embed = discord.Embed(title=f"IMAGE OF THE DAY", description=f"Unlocked by: {events_handler.imageunlocketby}") #,color=Hex code
            file = discord.File("imgoftheday.jpg", filename="imgoftheday.jpg")
            await message.channel.send(file = file, embed=embed)
        else:
            await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC).')
        events_handler.db.write(users)

    if message.content.startswith('!addimageoftheday'):
        str_split = message.content.split(' ')
        await message.delete()
        if len(str_split) > 2 or len(str_split) < 1:
            await message.channel.send(f'Too many or few arguments. Use !addimageoftheday <link>')
        else:
            if 400 <= users[message.author.name]['Coins']:
                events_handler.imageofthedayunlocket = False
                users[message.author.name]['Coins'] -= 400
                response = requests.get(str_split[1])
                if response.status_code == 200:
                    with open("imgoftheday.jpg", 'wb') as f:
                        f.write(response.content)

                img = plt.imread('imgoftheday.jpg')
                height, width, nbands = img.shape
                dpi = 80
                # What size does the figure need to be in inches to fit the image?
                figsize = width / float(dpi), height / float(dpi)

                # Create a figure of the right size with one axes that takes up the full figure
                fig = plt.figure(figsize=figsize)
                ax = fig.add_axes([0, 0, 1, 1])

                # Hide spines, ticks, etc.
                ax.axis('off')

                if nbands > 0:
                    img_avg_1 = mean(img[:, :, 0], disk(int(0.1*width + height*0.1)))
                    img_avg_2 = mean(img[:, :, 1], disk(int(0.1*width + height*0.1)))
                    img_avg_3 = mean(img[:, :, 2], disk(int(0.1*width + height*0.1)))
                    
                    img_avg = np.zeros((height, width, nbands))
                    img_avg[:, :, 0] = img_avg_1
                    img_avg[:, :, 1] = img_avg_2
                    img_avg[:, :, 2] = img_avg_3
                img_avg = img_avg.astype('int')

                ax.imshow(img_avg)
                ax.set(xlim=[-0.5, width - 0.5], ylim=[height - 0.5, -0.5], aspect=1)
                fig.savefig('imgoftheday_blurred.jpg', dpi=dpi)
                plt.close()
                await message.channel.send(f'Image added.')
            else:
                client.delete_message(message)
                await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC).')
        events_handler.db.write(users)


    if message.content.startswith('!adminaddimageoftheday'):
        str_split = message.content.split(' ')
        await message.delete()
        if len(str_split) > 2 or len(str_split) < 1:
            await message.channel.send(f'Too many or few arguments. Use !adminaddimageoftheday <link>')
        else:
            response = requests.get(str_split[1])
            if response.status_code == 200:
                with open("imgoftheday.jpg", 'wb') as f:
                    f.write(response.content)

            events_handler.imageofthedayunlocket = False
            img = plt.imread('imgoftheday.jpg')
            height, width, nbands = img.shape
            dpi = 80
            # What size does the figure need to be in inches to fit the image?
            figsize = width / float(dpi), height / float(dpi)

            # Create a figure of the right size with one axes that takes up the full figure
            fig = plt.figure(figsize=figsize)
            ax = fig.add_axes([0, 0, 1, 1])

            # Hide spines, ticks, etc.
            ax.axis('off')

            if nbands > 0:
                img_avg_1 = mean(img[:, :, 0], disk(50))
                img_avg_2 = mean(img[:, :, 1], disk(50))
                img_avg_3 = mean(img[:, :, 2], disk(50))
                
                img_avg = np.zeros((height, width, nbands))
                img_avg[:, :, 0] = img_avg_1
                img_avg[:, :, 1] = img_avg_2
                img_avg[:, :, 2] = img_avg_3
            img_avg = img_avg.astype('int')

            ax.imshow(img_avg)
            ax.set(xlim=[-0.5, width - 0.5], ylim=[height - 0.5, -0.5], aspect=1)
            fig.savefig('imgoftheday_blurred.jpg', dpi=dpi)
            plt.close()
            await message.channel.send(f'Image added.')
        events_handler.db.write(users)


        #current_time = datetime.datetime.now()
        #body = name + '\n' + current_time

        # # dd/mm/YY H:M:S
        # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        # print("date and time =", dt_string)




    # if message.content.startswith('!buy boost'):
    #     str_split = message.content.split(' ')
    #     print(str_split)
    #     print(len(str_split))
    #     if len(str_split) > 3 or len(str_split) < 2:
    #         await message.channel.send(f'Too many or few arguments. Use !buy boost amount')
    #     try:
    #         amount = int(str_split[2])
    #     except ValueError:
    #         await message.channel.send(f'value needs to be integer!')


    #     if 300*amount <= users[message.author.name]['Coins']:
    #         if 'Boosters' in users[message.author.name]:
    #             users[message.author.name]['Boosters'] += amount
    #         else:
    #             users[message.author.name]['Boosters'] = amount
    #         users[message.author.name]['Coins'] -= amount*300
    #         await message.channel.send(f'{message.author.name} bought {amount} :pill: boosts!')
    #     else:
    #         await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC) to buy :pill: boosters!')
    #         await message.channel.send(f' Price: 300 <:CBCcoin:831506214659293214> (CBC).')
    #     events_handler.db.write(users)


    # if message.content.startswith('!buy mute'):
    #         str_split = message.content.split(' ')
    #         print(str_split)
    #         print(len(str_split))
    #         if len(str_split) > 3 or len(str_split) < 2:
    #             await message.channel.send(f'Too many or few arguments. Use !buy mute target')
    #         try:
    #             target = str(str_split[2])
    #         except ValueError:
    #             await message.channel.send(f'value needs to be integer!')


    #         if 150 <= users[message.author.name]['Coins']:
    #             members = client.get_all_members()
    #             # Mute target
    #             if target in users:
    #                 users[message.author.name]['Coins'] -= 150
    #                 await message.channel.send(f'{message.author.name} bought mute :mute: targeting {target} ')
    #                 for member in members:
    #                     if member.name == target:
    #                         users[target]['mutetimer'] = 30
    #                         await member.edit(mute = True)
    #                     else:
    #                         await message.channel.send(f'Target not found.')
    #                         users[message.author.name]['Coins'] += 150
    #             else:
    #                 await message.channel.send(f'{target} does not exist. ')

    #         else:
    #             await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC) to buy mute :mute:')
    #             await message.channel.send(f' Price: 150 <:CBCcoin:831506214659293214> (CBC).')
    #         events_handler.db.write(users)



    if message.content.startswith('!transferCBC'):
        str_split = message.content.split(' ')
        print(str_split)
        print(len(str_split))
        if len(str_split) > 3 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !transferCBC target amount')
        else:
            TARGET_FOUND = False
            amount = int(str_split[2])
            if amount >= 0:
                target = str(str_split[1])
                if users[message.author.name]['Coins'] >= amount:
                    for member in users:
                        if target == member:
                            users[member]['Coins'] += amount
                            users[message.author.name]['Coins'] -= amount
                            await message.channel.send(f'{message.author.name} transfered {amount} <:CBCcoin:831506214659293214> (CBC) to {member}')
                            TARGET_FOUND = True
                            break
                        
                else:
                    if TARGET_FOUND:
                        await message.channel.send(f'{message.author.name} does not have enough <:CBCcoin:831506214659293214> (CBC).')
                    else:
                        await message.channel.send(f'{target} does not exist.')
        events_handler.db.write(users)


    # if message.content.startswith('!spray'):
    #     #embed = discord.Embed(title=f"", description=f"Lootbox just dropped! The first one to add ticket will get the lootbox! You can retrieve lootbox by typing !grabbox") #,color=Hex code
    #     embed.set_image(url="https://raw.githubusercontent.com/MartinRovang/CrazyBlazin/main/images/lootcrate.png")
    #     await message.channel.send(embed=embed)

    if message.content.startswith('!buy spray '):
        str_split = message.content.split(' ')
        if len(str_split) > 3 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !buy spray id')
        else:
            pass
        events_handler.db.write(users)




    if message.content.startswith('!grabbox'):
        if events_handler.lootbox != '':

            embed = discord.Embed(title=f"Loot box event :toolbox:", description=f"{message.author.name} grabbed the lootbox and got the following items: ") #,color=Hex code

            embed.add_field(name=f"<:CBCcoin:831506214659293214>", value=f'{events_handler.lootbox.coins}')
            embed.add_field(name=f":pill:", value=f'{events_handler.lootbox.boosters}')
            embed.add_field(name=f":tickets:", value=f'{events_handler.lootbox.tickets}')
            await message.channel.send(embed=embed)

            users[message.author.name]['Coins'] += events_handler.lootbox.coins
            users[message.author.name]['Boosters'] += events_handler.lootbox.boosters
            users[message.author.name]['Tickets'] += events_handler.lootbox.tickets
            events_handler.lootbox = ''
            
        else:
            await message.channel.send(f'No lootbox have dropped!')
        events_handler.db.write(users)



    if message.content.startswith('!web'):
        with open('webpage.txt', 'r') as f:
            webpage = f.read()
        await message.channel.send(f'Webpage is: {webpage}')


    if message.content.startswith('!use boost'):
        str_split = message.content.split(' ')
        print(str_split)
        print(len(str_split))
        if len(str_split) > 2 or len(str_split) < 1:
            await message.channel.send(f'Too many or few arguments. Use !buy boost amount')
        
        else:
            if 'Boosters' not in users[message.author.name]:
                    users[message.author.name]['Boosters'] = 0

            if users[message.author.name]['Boosters'] < 1:
                await message.channel.send(f'{message.author.name} does not have any boosters!')
            else:
                users[message.author.name]['Boosters'] -= 1
                users[message.author.name]['Active'] = 'Booster'
                users[message.author.name]['BoostTimer'] = 1800
                member = message.author
                role = get(member.guild.roles, name='Booster')
                await member.add_roles(role)
                await message.channel.send(f'{message.author.name} used a :pill: boost!, the user will be boosted for 30 minutes.')

                events_handler.db.write(users)
                # To force voice state changes for instant changes in boosting roles
                await member.edit(mute = True)
                await member.edit(mute = False)


        events_handler.db.write(users)

        
client.run(k)


# fig, ax = plt.subplots(1, 3)
# ax[0].imshow(input_image_)
# ax[1].imshow(input_image_masked)
# ax[2].imshow(r)
# plt.show()


