
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

# client = commands.Bot(command_prefix='!')

#https://discordapp.com/developers




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
            if members not in users:
                users[members] = {'Coins': 25, 'Tickets': 1, 'Timer': 0, 'BoostTimer': 0, 'Boosters': 0, 'Actives': [], 'Active': '0'}
                users[members]['Actives'] = []

            state = self.coin_aggregation_members[members]
            channel_state = str(state.channel)
            stream_state = state.self_stream

            if channel_state in self.boosted_channels:
                if 'Boosted' not in users[members]['Actives']:
                    users[members]['Actives'].append('Boosted')
                else:
                    pass
                print(f'{members} is boosted')
            else:
                users[members]['Actives'] = []

            if channel_state != 'None':
                if stream_state:
                    if 'Boosted' in users[members]['Actives']:
                        users[members]['Coins'] = round(users[members]['Coins'] + 1*3, 2)
                    else:
                        users[members]['Coins'] = round(users[members]['Coins'] + 1, 2)

                    print(f'Stream activity: {members}')
                else:
                    if 'Boosted' in users[members]['Actives']:
                        users[members]['Coins'] = round(users[members]['Coins'] + 0.33*3, 2)
                    else:
                        users[members]['Coins'] = round(users[members]['Coins'] + 0.33, 2)

                print(f'Coins to : {members}')

        self.db.write(users)
        # return users


class LootBox:
    def __init__(self):
        self.coins = np.random.randint(0, 50)
        self.boosters = np.random.randint(0, 3)
        self.tickets = np.random.randint(0, 2)


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

    @tasks.loop(seconds=30) # task runs every 60 seconds
    async def add_coins_after_time(self):
        events_handler.coin_aggregation()
        users = events_handler.db.read()
        print('Coins distributed!')

        members = self.get_all_members()

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

        members = self.get_all_members()
        for key in users:
            if 'BoostTimer' in users[key]:
                if users[key]['BoostTimer'] > 0:
                    users[key]['BoostTimer'] -= 30
                else:
                    users[key]['BoostTimer'] = 0
                    users[key]['Active'] = '0'
                    # next(user for user in client.users if user.name == key)
                    for member in members:
                        if member.name == key:
                            role_names = [role.name for role in member.roles]
                            if 'Booster' in role_names:
                                print('Removing booster role')
                                role = get(member.guild.roles, name='Booster')
                                await member.remove_roles(role)
        events_handler.db.write(users)
            

                #803982821923356773
        print(probability)
        if probability >= 995:
            channel = client.get_channel(803982821923356773)
            events_handler.lootbox = LootBox()
            embed = discord.Embed(title=f"Lootbox drop! :toolbox:", description=f"Lootbox just dropped! The first one to add ticket will get the lootbox! You can retrieve lootbox by typing !grabbox") #,color=Hex code
            embed.set_image(url="https://raw.githubusercontent.com/MartinRovang/CrazyBlazin/main/images/lootcrate.png")
            await channel.send(embed=embed)

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

    members = client.get_all_members()
    users = events_handler.db.read()

    events_handler.boosted_channels = []

    for mem in members:
        if str(mem.name) in users:
            if 'Active' in users[str(mem.name)]:
                if users[str(mem.name)]['Active'] == 'Booster':
                    if mem.voice not in events_handler.boosted_channels:
                        if str(mem.voice) != 'None':
                            events_handler.boosted_channels.append(str(mem.voice.channel))

    members = client.get_all_members()
    for mem in members:
        if str(mem.voice) != 'None':
            if str(mem.voice.channel) in events_handler.boosted_channels:
                role = get(mem.guild.roles, name='Boosted')
                await mem.add_roles(role)
            else:
                role = get(mem.guild.roles, name='Boosted')
                await mem.remove_roles(role)
        else:
            role = get(mem.guild.roles, name='Boosted')
            await mem.remove_roles(role)
    
    events_handler.db.write(users)
    


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    with open('crazy_blazin_database.txt', 'r') as f:
        users = eval(f.read())


    if 'Boosters' not in users[message.author.name]:
        users[message.author.name]['Boosters'] = 0

    if 'Actives' not in users[message.author.name]:
        users[message.author.name]['Actives'] = []

    if 'Active' not in users[message.author.name]:
        users[message.author.name]['Active'] = '0'


    if message.author.name not in users:
        users[message.author.name] = {'Coins': 25, 'Tickets': 1, 'Timer': 0, 'BoostTimer': 0, 'Boosters': 0, 'Actives': []}

        with open('crazy_blazin_database.txt', 'w') as f:
            f.write(str(users))


    if message.content.startswith('!bal'):
        value = users[message.author.name]['Coins']
        ticket = users[message.author.name]['Tickets']
        boosts = users[message.author.name]['Boosters']
        embed = discord.Embed(title=f"Balance", description=f"{message.author.name} current balance") #,color=Hex code

        embed.add_field(name=f"<:CBCcoin:831506214659293214> (CBC)", value=f'{value}')
        embed.add_field(name=f":tickets: (tickets)", value=f'{ticket}')
        embed.add_field(name=f":pill: (boosts)", value=f'{boosts}')
        await message.channel.send(embed=embed)



    if message.content.startswith('!top'):
        index = 1
        with open('crazy_blazin_database.txt', 'r') as f:
            users = eval(f.read())

        embed = discord.Embed(title="Top wealth", description="Top owners of Crazy Blazin Coins") #,color=Hex code
            
        temp_stats = {}
        for key_user in users:
            temp_stats[key_user] = users[key_user]['Coins']
        for key in sorted(temp_stats, key=temp_stats.get, reverse=True):
            if (index < 11):
                embed.add_field(name=f"{index}. {key}", value=f'{users[key]["Coins"]} <:CBCcoin:831506214659293214>')
            else: 
                await message.channel.send(embed=embed)
                return
            index += 1

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
            with open('crazy_blazin_database.txt', 'w') as f:
                f.write(str(users))


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


