from flask import Flask, render_template, url_for
import pickle
from datetime import datetime, time
import numpy as np
import io
from PIL import Image
import matplotlib.pyplot as plt
import json
import jsonpickle

# START_TIME = time(hour=9)
# END_TIME = time(hour=12)  # Can also use something like timedelta
# if START_TIME <= now.time() <= END_TIME:    
from flask import Flask, render_template, url_for, request, Response, send_file
import http.client
from datetime import datetime, time
from matplotlib import image
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from pathlib import Path
import uuid
import glob
import shutil

from werkzeug.datastructures import FileStorage
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename

app = Flask(__name__)
api = Api(app)


class Database:
    def __init__(self):
        self.dbName = '../crazy_blazin_database.txt' 
    def read(self):
        with open(self.dbName, 'r') as f:
            return eval(f.read())

    def write(self, users):
        with open(self.dbName, 'w') as f:
            f.write(str(users))


db = Database()


@app.route("/")
def front():
    users = db.read()
    temp_dict = {}
    for user in users:
        temp_dict[user] = users[user]['Coins']
        # print(users[user]['Coins'])
    sorted_users = sorted(temp_dict.items(),  key=lambda x: x[1], reverse=True)

    for user in users:
        if 'Timer' not in users[user]:
            users[user]['Timer'] = 0
    #users -> key, users[key] -> {'Coins' : 499, .....}

    return render_template('frontpage.html', users = sorted_users, users_all = users)  


@app.route("/commands")
def coms():
    
    return render_template('commands.html')  

@app.route("/db")
def get_db():
    users = db.read()
    return users


class AddWebpage(Resource):
    def post(self, link):
    
        with open('../webpage.txt', 'w') as f:
            f.write(str(link))
        return {'Response': 'Complete'}, http.client.OK


class EventUI:
    def __init__(self, text, color, size):
        self.text = text
        self.color = color
        self.size = size

class Monster:
    monsterevents = []
    def __init__(self, id, name = 'GOBLIN FAMILY', health = 100, atk = 100, armor = 1, img = ''):
        self.id = id
        self.name = name
        self.health = health
        self.atk = atk
        self.armor = armor
        self.img = 'https://raw.githubusercontent.com/MartinRovang/CrazyBlazin/main/images/mobs/goblin_familiy.png'
        self.eventlogs = [] #{'textevents': ["DWNDJWND", "DWNDJWND22"], 'color': ["red", "blue"], 'size': ["30", "10"]}
        self.monsterevents.append(self)
        # self.doevent('Foxxravin')

    def doevent(self, target):
        #EventUI("MONSTER HIT PAUL FOR 10 DMG", "red", "30")
        # CALCULATE EVENT
        users = db.read()
        # users[target]['rpg'] = {}
        # users[target]['rpg']['health'] = 100
        # users[target]['rpg']['atk'] = 100
        # users[target]['rpg']['armor'] = 2
        for user in users:
            i = 0
            if user == target:
                while users[target]['rpg']['health'] > 0 and self.health > 0:
                    if i%2 == 0:
                        user_atk = np.random.randint(0, users[target]['rpg']['atk'])
                        dmg_dealt = round(user_atk/self.armor, 2)
                        self.health -= dmg_dealt
                        event = EventUI(f"{user} hit {self.name} for {dmg_dealt} damage!, {self.name} has {self.health} HP left.", "green", "30")
                        self.eventlogs.append(event)
                    else:
                        monster_atk = np.random.randint(0, self.atk)
                        dmg_dealt = round(monster_atk/users[target]['rpg']['armor'], 2)
                        users[target]['rpg']['health'] -= dmg_dealt
                        health_left = users[target]['rpg']['health']
                        event = EventUI(f"{self.name} hit {user} for {dmg_dealt} damage!, {user} has {health_left} HP left.", "red", "30")
                        self.eventlogs.append(event)
                    
                    i += 1
                
                if self.health <= 0:
                    event = EventUI(f"{target} WON!", "green", "30")
                    coindrop = np.random.randint(0, 1000)
                    tickets = np.random.randint(0, 10)
                    boosts = np.random.randint(0, 10)
                    event = EventUI(f"COINS DROPPED: {coindrop}", "black", "20")
                    self.eventlogs.append(event)
                    event = EventUI(f"BOOSTS DROPPED: {boosts}", "black", "20")
                    self.eventlogs.append(event)
                    event = EventUI(f"TICKETS DROPPED: {tickets}", "black", "20")
                    self.eventlogs.append(event)
                    # GIVE LOOT

                if users[target]['rpg']['health'] <= 0:
                    event = EventUI(f"{target} Lost!", "red", "30")
                    self.eventlogs.append(event)


#ed0ce8c7-a4fe-11eb-badb-40167e77d41a

class MonsterEventHandler(Resource):
    def post(self):
        id = str(uuid.uuid1())
        Monster.monsterevents.append(Monster(id = id, health = 100))
        return {'id': f'{id}'}, http.client.OK


@app.route("/events/<eventid>")
def event(eventid):
    for monsterevent in Monster.monsterevents:
        if eventid == monsterevent.id:
            return render_template('event.html', eventlogs = jsonpickle.encode(monsterevent.eventlogs), mobimg = monsterevent.img)
    
    return {'Response': 'Event does not exist'}, http.client.NOT_FOUND

api.add_resource(MonsterEventHandler, '/api/event/generate')


#curl -X POST localhost:5000/api/files/<id>/predict

if __name__ == "__main__":
    app.run(debug=True)