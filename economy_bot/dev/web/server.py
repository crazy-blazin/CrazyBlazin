from flask import Flask, render_template, url_for
import pickle
from datetime import datetime, time
import numpy as np
import io
from PIL import Image
import matplotlib.pyplot as plt
import json
import jsonpickle
import random
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

from flask_socketio import SocketIO

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('msg')
def msg(msg):
    print(msg)
    socketio.emit('clientMsg', msg, broadcast=True, include_self=False)

@socketio.on('connect')
def test_connect():
    print('Client connected')
    socketio.emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

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
        temp_dict[user] = users[user]['tot_dmg']
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
    def __init__(self, 
    id, 
    name = 'GOBLIN FAMILY', 
    health = 100, 
    atk = 100, 
    armor = 1, 
    img = '',
    loot_table = ["🐱", "🐥", "🏰" ],
    loot_chance = [0.2, 0.3, 0.01], 
    loot_drop_size = 5):
        self.id = id
        self.name = name
        self.health = health
        self.atk = atk
        self.armor = armor
        self.img = 'https://raw.githubusercontent.com/MartinRovang/CrazyBlazin/main/images/mobs/ararajuba--guaruba-guarouba------golden-parakeet-158698703-5b5a6e67c9e77c0050187aec.jpg'
        self.eventlogs = [] #{'textevents': ["DWNDJWND", "DWNDJWND22"], 'color': ["red", "blue"], 'size': ["30", "10"]}
        self.loot_table = loot_table
        self.loot_chance = loot_chance
        self.loot_drop_size = loot_drop_size
        # https://apps.timwhitlock.info/emoji/tables/unicode

        self.loot = random.choices(self.loot_table, self.loot_chance, k = self.loot_drop_size)
        self.monsterevents.append(self)

    def doevent(self, target):
        #EventUI("MONSTER HIT PAUL FOR 10 DMG", "red", "30")
        # CALCULATE EVENT
        users = db.read()
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
                    self.eventlogs.append(event)
                    event = EventUI(f"LOOT:  {self.loot}", "black", "30")
                    self.eventlogs.append(event)

                if users[target]['rpg']['health'] <= 0:
                    event = EventUI(f"{target} Lost!", "red", "30")
                    self.eventlogs.append(event)
                    
        users = db.write(users)


#ed0ce8c7-a4fe-11eb-badb-40167e77d41a

class MonsterEventHandler(Resource):
    def post(self):
        id = str(uuid.uuid1())
        Monster.monsterevents.append(Monster(id = id, name= "Gobling family"))
        return {'id': f'{id}'}, http.client.OK


@app.route("/events/<eventid>")
def event(eventid):
    for monsterevent in Monster.monsterevents:
        if eventid == monsterevent.id:
            monsterevent.doevent('Foxxravin')
            return render_template('event.html', eventlogs = jsonpickle.encode(monsterevent.eventlogs), mobimg = monsterevent.img)
    
    return {'Response': 'Event does not exist'}, http.client.NOT_FOUND


api.add_resource(MonsterEventHandler, '/api/event/generate')
api.add_resource(AddWebpage, '/web/<link>')



@app.route("/obs_gif")
def obs_gif():
    return render_template('obs_gif.html')


@app.route("/obs_donation")
def obs_donation():
    return render_template('obs_donation.html')


@app.route("/stonk")
def stonk():
    return render_template('stonk.html')

#curl -X POST localhost:5000/api/files/<id>/predict

if __name__ == "__main__":
    socketio.run(app, debug=True)