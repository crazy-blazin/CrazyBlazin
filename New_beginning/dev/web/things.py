
import uuid
import numpy as np
from collections import Counter

class Stonk:
    all_stonks = []
    def __init__(self, name, init_value = 5, meanval= 0,  variance = 5, drift = 1.1):
        self.id = str(uuid.uuid1())
        self.name = name
        self.variance = variance
        self.mean = meanval
        self.drift = drift
        self.current_price = init_value
        self.y = [init_value, init_value, init_value]
        self.x = [1]
        self.all_stonks.append(self)
        self.onehourdifference = 0
        self.time = 0


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
        if y <= 0:
            y = 1
        #y = round(self.drift*self.time + self.y[-1] + np.random.normal(self.mean, self.variance),2)
        self.time += 1
        if len(self.y) < 1800:
            onehourindex = 0
        else:
            onehourindex = -1800
        self.onehourdifference = round(((y - self.y[onehourindex])/( 0.000001 + self.y[onehourindex]))*100, 2)
        self.y.append(y)
        self.y = self.y[-3600:]
        self.x.append(self.x[-1]+1)
        self.x = self.x[-3600:]
        self.current_price = round(self.y[-1],2)

    @staticmethod
    def get_all_stonks_info():
        all_stonks_info = []
        for stonk in Stonk.all_stonks:
            all_stonks_info.append(stonk.get_info())
        return all_stonks_info

def sigmoid(x):
    return 1/(1 + np.exp(-x))

class Consumables:
    def __init__(self, name = 'Test'):
        pass


class Items:
    all_items_low = []
    all_items_med = []
    all_items_high = []
    all_items_shop = []
    def __init__(self, name,
                       health,
                       armor,
                       dmg,
                       coinpertick,
                       health_regen,
                       itemtype):
        self.name  = name
        self.health = health
        self.armor = armor
        self.dmg = dmg
        self.coinpertick = coinpertick
        self.health_regen = health_regen
        if itemtype == 'low':
            self.all_items_low.append(self)
        if itemtype == 'med':
            self.all_items_med.append(self)
        if itemtype == 'high':
            self.all_items_high.append(self)
        if itemtype == 'shop':
            self.all_items_shop.append(self)


    
    @staticmethod
    def get_item_sample(lootinfo):
        itemtype, amount = lootinfo[0], lootinfo[1]
        output = []
        if itemtype == 'low':
            tempoutput = np.random.choice(Items.all_items_low, size=amount, replace=True)
            for item in tempoutput:
                output.append(item.name)
            return output
        if itemtype == 'med':
            tempoutput = np.random.choice(Items.all_items_med, size=amount, replace=True)
            for item in tempoutput:
                output.append(item.name)
            return output
        if itemtype == 'high':
            tempoutput = np.random.choice(Items.all_items_high, size=amount, replace=True)
            for item in tempoutput:
                output.append(item.name)
            return output
        

    @staticmethod
    def init_items():
        with open('items_low.txt', 'r') as f:
            itemslist_low = eval(f.read())
        
        with open('items_med.txt', 'r') as f:
            itemslist_med = eval(f.read())

        with open('items_med.txt', 'r') as f:
            itemslist_high = eval(f.read())
        
        with open('items_shop.txt', 'r') as f:
            itemslist_shop = eval(f.read())

        for itemname in itemslist_low:
            Items(name = itemname, 
                  health = itemslist_low[itemname]['health'],
                  armor = itemslist_low[itemname]['armor'],
                  dmg = itemslist_low[itemname]['dmg'],
                  coinpertick = itemslist_low[itemname]['coinpertick'],
                  health_regen = itemslist_low[itemname]['health_regen'],
                  itemtype = 'low'
                  )
        
        for itemname in itemslist_med:
            Items(name = itemname, 
                  health = itemslist_med[itemname]['health'],
                  armor = itemslist_med[itemname]['armor'],
                  dmg = itemslist_med[itemname]['dmg'],
                  coinpertick = itemslist_med[itemname]['coinpertick'],
                  health_regen = itemslist_med[itemname]['health_regen'],
                  itemtype = 'med'
                  )

        for itemname in itemslist_high:
            Items(name = itemname, 
                  health = itemslist_high[itemname]['health'],
                  armor = itemslist_high[itemname]['armor'],
                  dmg = itemslist_high[itemname]['dmg'],
                  coinpertick = itemslist_high[itemname]['coinpertick'],
                  health_regen = itemslist_high[itemname]['health_regen'],
                  itemtype = 'high'
                  )
        
        for itemname in itemslist_shop:
            Items(name = itemname, 
                  health = itemslist_shop[itemname]['health'],
                  armor = itemslist_shop[itemname]['armor'],
                  dmg = itemslist_shop[itemname]['dmg'],
                  coinpertick = itemslist_shop[itemname]['coinpertick'],
                  health_regen = itemslist_shop[itemname]['health_regen'],
                  itemtype = 'shop'
                  )



class User:
    all_users = []
    def __init__(self, name = '', 
                        basemaxhealth = 150,  
                        maxtickets = 30, 
                        health_regen_base = 1, 
                        health_regen = 1,
                        health = 0,
                        maxhealth = 0,
                        armor = 0, 
                        dmg = 0, 
                        faction = '',
                        coinpertick_base = 2,
                        total_income = 0,
                        tickets = 30,
                        itemsDB = [],
                        coins = 10,
                        stonks = [],
                        stonksDB = {}) -> None:
        self.name = name
        self.basemaxhealth = basemaxhealth
        self.maxhealth = maxhealth
        self.maxtickets = maxtickets
        self.health_regen_base = health_regen_base
        self.health = health
        self.health_regen = health_regen
        self.armor = armor
        self.dmg = dmg
        self.coins = coins
        self.total_income = total_income
        self.faction = faction
        self.coinpertick_base = coinpertick_base
        self.coinpertick = 0
        self.itemsDB = itemsDB
        self.items = []
        self.tickets = tickets
        self.stonks = stonks
        self.stonksDB = stonksDB
        self.all_users.append(self)


    def add_stonks(self, stonkname = '', amount = 1):
        for real_stonk in Stonk.all_stonks:
            if real_stonk.name == stonkname:
                if stonkname in self.stonksDB:
                    self.stonksDB[stonkname] += amount
                else:
                    self.stonks.append(real_stonk)
                    self.stonksDB[stonkname] = amount


    def add_item(self, itemname = '', amount = 1):
        

        if itemname in Items.all_items_low:
            if itemname in self.itemsDB:
                self.itemsDB[itemname] += amount
            else:
                self.items.append(Items.all_items_low[itemname])
                self.itemsDB[itemname] = amount
            
        if itemname in Items.all_items_high:
            if itemname in self.itemsDB:
                self.itemsDB[itemname] += amount
            else:
                self.items.append(Items.all_items_high[itemname])
                self.itemsDB[itemname] = amount
        
        if itemname in Items.all_items_med:
            if itemname in self.itemsDB:
                self.itemsDB[itemname] += amount
            else:
                self.items.append(Items.all_items_med[itemname])
                self.itemsDB[itemname] = amount

        if itemname in Items.all_items_shop:
            if itemname in self.itemsDB:
                self.itemsDB[itemname] += amount
            else:
                self.items.append(Items.all_items_shop[itemname])
                self.itemsDB[itemname] = amount

    @staticmethod
    def update():
        for user in User.all_users:
            user.items = []
            user.stonks = []
            
            for item in user.itemsDB:
                for real_item in Items.all_items_low:
                    if real_item.name == item:
                        user.items.append(real_item)
                
                for real_item in Items.all_items_med:
                    if real_item.name == item:
                        user.items.append(real_item)
                
                for real_item in Items.all_items_high:
                    if real_item.name == item:
                        user.items.append(real_item)
                
                for real_item in Items.all_items_shop:
                    if real_item.name == item:
                        user.items.append(real_item)

            for stonk in user.stonksDB:
                for real_stonk in Stonk.all_stonks:
                    if real_stonk.name == stonk:
                        user.stonks.append(real_stonk)

            user.coinpertick = 0
            user.health_regen = user.health_regen_base
            user.armor = 0
            user.total_income = user.coinpertick_base
            user.maxhealth = user.basemaxhealth
            user.dmg[0] = 0
            user.dmg[1] = 0
            if user.health < 0:
                user.health = 0
            for item in user.items:
                multiplier = user.itemsDB[item.name]
                user.maxhealth += item.health*multiplier
                user.total_income += item.coinpertick*multiplier
                user.health_regen += item.health_regen*multiplier
                user.dmg[0] += item.dmg[0]*multiplier
                user.dmg[1] += item.dmg[1]*multiplier
                user.armor += item.armor*multiplier
            
    @staticmethod
    def tick():
        for user in User.all_users:
            user.coins += user.total_income
            
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
    
    @staticmethod
    def writetodb():
        with open('database.txt', 'w') as f:
            data = {}
            for user in User.all_users:
                data[user.name] = {'basemaxhealth': user.basemaxhealth,
                                    'maxhealth': user.maxhealth,
                                    'maxtickets':user.maxtickets,
                                    'health_regen_base': user.health_regen_base,
                                    'health_regen': user.health_regen,
                                    'health': user.health,
                                    'armor': user.armor,
                                    'dmg': user.dmg,
                                    'coins': user.coins,
                                    'itemsDB': user.itemsDB,
                                    'total_income': user.total_income,
                                    'faction': user.faction,
                                    'stonksDB' : user.stonksDB,
                                    'coinpertick_base': user.coinpertick_base,
                                    'tickets': user.tickets
                                   }
            f.write(str(data))

    
    @staticmethod
    def readdb():
        with open('database.txt', 'r') as f:
            database = eval(f.read())

        if len(User.all_users) == 0:
            for key in database:
                User(name = key,
                    basemaxhealth = database[key]['basemaxhealth'],
                    maxtickets = database[key]['maxtickets'],
                    health_regen_base = database[key]['health_regen_base'],
                    health_regen = database[key]['health_regen'],
                    maxhealth = database[key]['maxhealth'],
                    health = database[key]['health'],
                    armor = database[key]['armor'],
                    dmg = database[key]['dmg'],
                    itemsDB = database[key]['itemsDB'],
                    coins = database[key]['coins'],
                    total_income = database[key]['total_income'],
                    faction = database[key]['faction'],
                    coinpertick_base = database[key]['coinpertick_base'],
                    tickets = database[key]['tickets'],
                    stonksDB = database[key]['stonksDB'],
                    )

        for userdb in database:
            for user in User.all_users:
                if userdb == user.name:
                    user.basemaxhealth = database[userdb]['basemaxhealth']
                    user.maxtickets = database[userdb]['maxtickets']
                    user.health_regen_base = database[userdb]['health_regen_base']
                    user.health_regen = database[userdb]['health_regen']
                    user.maxhealth = database[userdb]['maxhealth']
                    user.health = database[userdb]['health']
                    user.armor = database[userdb]['armor']
                    user.coins = database[userdb]['coins']
                    user.itemsDB = database[userdb]['itemsDB']
                    user.total_income = database[userdb]['total_income']
                    user.faction = database[userdb]['faction']
                    user.coinpertick_base = database[userdb]['coinpertick_base']
                    user.tickets = database[userdb]['tickets']

    @staticmethod
    def makeuser(
            name, 
            basemaxhealth = 100,
            maxtickets = 30,
            health_regen_base = 2,
            health_regen = 2,
            health = 100,
            maxhealth = 0,
            armor = 0,
            dmg = [0, 0],
            itemsDB = {'Simple knife': 1},
            coins = 100,
            total_income = 5,
            faction = None,
            coinpertick_base = 5,
            tickets = 30,
            stonksDB = {}
    ):
        User(name = name,
            basemaxhealth = basemaxhealth,
            maxtickets = maxtickets,
            health_regen_base = health_regen_base,
            health_regen = health_regen,
            health = health,
            armor = armor,
            dmg = dmg,
            itemsDB = itemsDB,
            coins = coins,
            total_income = total_income,
            faction = faction,
            coinpertick_base = coinpertick_base,
            tickets = tickets,
            stonksDB = stonksDB,
                    )
    




class Faction:
    all_factions = []
    factioncounter = 0
    def __init__(self, name = 'Test'):
        Faction.factioncounter += 1
        self.factionID = Faction.factioncounter
        self.name = name
        self.health = 0
        self.tickets = 30
        self.maxtickets = 30
        self.armor = 0
        self.maxhp = 0
        self.coins = 0
        self.dmg = 0
        self.maxhp = 0
        self.members = []
        self.health_regen = 0
        self.all_factions.append(self)
    
    @staticmethod
    def update():
        for faction in Faction.all_factions:
            faction.maxhp = 0
            faction.armor = 0
            faction.health_regen = 0
            faction.dmg[0] = 0
            faction.dmg[1] = 0
            for user in faction.members:
                faction.maxhp += user.maxhealth
                faction.armor += user.armor
                faction.dmg[0] += user.dmg[0]
                faction.dmg[1] += user.dmg[1]
                faction.health_regen += user.health_regen

    @staticmethod
    def tick():
        for faction in Faction.all_factions:

            tickets = faction.tickets + 1
            if tickets >= faction.maxtickets:
                faction.tickets = faction.maxtickets
            else:
                faction.tickets += 1
            
            health = faction.health + faction.health_regen

            if health >= faction.maxhp:
                faction.health = faction.maxhp
            else:
                faction.health += faction.health_regen


    @staticmethod
    def writetodb():
        with open('factions.txt', 'w') as f:
            data = {}
            for faction in Faction.all_factions:
                data[faction.name] = {'current_health': faction.health,
                                      'maxtickets': faction.maxtickets,
                                      'tickets': faction.tickets,
                                      'armor': faction.armor,
                                      'maxhp': faction.maxhp,
                                      'health_regen': faction.health_regen,
                                      'dmg': faction.dmg

                                   }
            f.write(str(data))

    
    @staticmethod
    def readdb():
        with open('factions.txt', 'r') as f:
            database = eval(f.read())

        for factiondb in database:
            for faction in Faction.all_factions:
                if faction.name == factiondb:
                    faction.health = database[factiondb]['current_health']
                    faction.maxtickets = database[factiondb]['maxtickets']
                    faction.tickets = database[factiondb]['tickets']
                    faction.armor = database[factiondb]['armor']
                    faction.maxhp = database[factiondb]['maxhp']
                    faction.health_regen = database[factiondb]['health_regen']
                    faction.dmg = database[factiondb]['dmg']

    @staticmethod
    def init_members():
        for faction in Faction.all_factions:
            for user in User.all_users:
                if user.faction == faction.name:
                    faction.add_members(user)

    def add_members(self, member):
        self.members.append(member)
        self.maxhp += member.maxhealth
        self.health += member.maxhealth


class EventUI:
    def __init__(self, text, color, size):
        self.text = text
        self.color = color
        self.size = size

class Mob:
    mobevents = []
    def __init__(self, username, mobtype = 1, id = ''):
        with open('mobs.txt', 'r') as f:
            mobslist = eval(f.read())

        for i, mobname in enumerate(mobslist):
            i += 1
            if int(mobtype) == i:
                self.username = username
                self.mobtype = mobtype
                self.id = id
                self.name = mobname
                self.health = mobslist[mobname]['health']
                self.armor = mobslist[mobname]['armor']
                self.dmg = mobslist[mobname]['dmg']
                self.img = mobslist[mobname]['img']
                self.loot = mobslist[mobname]['loot']
                self.lootdrops = Items.get_item_sample(self.loot)
                self.ticketcost = mobslist[mobname]['ticketcost']
                self.eventlogs = []
                self.mobevents.append(self)

    def doevent(self):
        for user in User.all_users:
            if self.username == user.name:
                while user.health > 0 and self.health > 0:
                    user_atk = np.random.randint(user.dmg[0], user.dmg[1])
                    dmg_dealt = round(user_atk - (sigmoid(self.armor*0.01)  - sigmoid(self.armor*0.01)/3 )*user_atk, 2)
                    self.health -= dmg_dealt
                    self.health = round(self.health,2)
                    event = EventUI(f"{user.name} hit {self.name} for {dmg_dealt} damage!, {self.name} has {self.health} HP left.", "green", "30")
                    self.eventlogs.append(event)

                    if self.health <= 0:
                        event = EventUI(f"{user.name} WON!", "green", "30")
                        self.eventlogs.append(event)
                        lootmsg = ""
                        count = Counter(self.lootdrops)
                        for itm in count:
                            lootmsg += f"{itm}: {count[itm]}, "
                        event = EventUI(f"LOOT:  {lootmsg}", "black", "30")
                        self.eventlogs.append(event)
                        for itm in count:
                            user.add_item(itemname = itm, amount = count[itm])
                        
                        return {'info': True, 'battlereport': f'{user.name} Won! loot: {lootmsg}'}
                    else:
                        monster_atk = round(np.random.randint(self.dmg[0], self.dmg[1]),2)
                        dmg_dealt = round(monster_atk - (sigmoid(user.armor*0.01)  - sigmoid(user.armor*0.01)/3 )*monster_atk, 2)
                        user.health -= dmg_dealt
                        user.health = round(user.health,2)
                        event = EventUI(f"{self.name} hit {user.name} for {dmg_dealt} damage!, {user.name} has {user.health} HP left.", "red", "30")
                        self.eventlogs.append(event)

                if user.health <= 0:
                    user.health = 0
                    event = EventUI(f"{user.name} Lost!", "red", "30")
                    self.eventlogs.append(event)
                    return {'info': True, 'battlereport': f'{user.name} Lost!'}
    
    def check_if_possible(self):
        for user in User.all_users:
            if self.username == user.name:
                if user.tickets >= self.ticketcost and user.health > 0:
                    user.tickets -= self.ticketcost
                    return True
                else:
                    return False
        return False



class Boss:
    bossevents = []
    def __init__(self, factionid, bosstype = 1, id = ''):
        with open('bosses.txt', 'r') as f:
            bosslist = eval(f.read())

        for i, bossname in enumerate(bosslist):
            i += 1
            if int(bosstype) == i:
                self.factionid = int(factionid)
                self.bosstype = bosstype
                self.id = id
                self.name = bossname
                self.health = bosslist[bossname]['health']
                self.armor = bosslist[bossname]['armor']
                self.dmg = bosslist[bossname]['dmg']
                self.img = bosslist[bossname]['img']
                self.ticketcost = bosslist[bossname]['ticketcost']
                self.loot = bosslist[bossname]['loot']
                self.lootdrops = Items.get_item_sample(self.loot)
                self.eventlogs = []
                self.bossevents.append(self)

    def doevent(self):
        for faction in Faction.all_factions:
            if self.factionid == faction.factionID:
                while faction.health > 0 and self.health > 0:
                    for member in faction.members:
                        user_atk = np.random.randint(member.dmg[0], member.dmg[1])
                        dmg_dealt = round(user_atk - (sigmoid(self.armor*0.01)  - sigmoid(self.armor*0.01)/3 )*user_atk, 2)
                        self.health -= dmg_dealt
                        self.health = round(self.health,2)
                        event = EventUI(f"{member.name} hit {self.name} for {dmg_dealt} damage!, {self.name} has {self.health} HP left.", "green", "30")
                        self.eventlogs.append(event)
                
                if self.health <= 0:
                    event = EventUI(f"{faction.name} WON!", "green", "30")
                    self.eventlogs.append(event)
                    count = Counter(self.lootdrops)
                    lootmsg = ""
                    for itm in count:
                        lootmsg += f"{itm}: {count[itm]}, "
                    event = EventUI(f"LOOT:  {lootmsg}", "black", "30")
                    self.eventlogs.append(event)
                    for member in faction.members:
                        for itm in count:
                            member.add_item(itemname = itm, amount = count[itm])
                    return {'info': True, 'battlereport': f'{faction.name} Won! loot: {lootmsg}'}
                else:
                    monster_atk = round(np.random.randint(self.dmg[0], self.dmg[1]),2)
                    dmg_dealt = round(monster_atk - (sigmoid(faction.armor*0.01)  - sigmoid(faction.armor*0.01)/3 )*monster_atk, 2)
                    faction.health -= dmg_dealt
                    faction.health = round(faction.health,2)
                    event = EventUI(f"{self.name} hit {faction.name} for {dmg_dealt} damage!, {faction.name} has {faction.health} HP left.", "red", "30")
                    self.eventlogs.append(event)

                if faction.health <= 0:
                    faction.health = 0
                    event = EventUI(f"{faction.name} Lost!", "red", "30")
                    self.eventlogs.append(event)
                    return {'info': True, 'battlereport': f'{faction.name} Lost!'}
    
    def check_if_possible(self):
        for faction in Faction.all_factions:
            if self.factionid == faction.factionID:
                if faction.tickets >= self.ticketcost and faction.health >= 0:
                    faction.tickets -= self.ticketcost
                    return True
                else:
                    return False
        return False