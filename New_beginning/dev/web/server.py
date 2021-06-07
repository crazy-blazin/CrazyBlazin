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
    socketio.emit('clientMsg', msg, broadcast=True, include_self=False)

@socketio.on('stonk_values')
def stonk_values(stonk_values):
    socketio.emit('clientMsg', stonk_values, broadcast=True, include_self=False)

@socketio.on('connect')
def test_connect():
    print('Client connected')
    socketio.emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@app.route("/stonks/<stonkid>")
def stonks(stonkid):

    return render_template('stonk.html', stonkid = stonkid)

@app.route("/stonks")
def front():
    return render_template('stonks.html')

@app.route("/factions")
def factions():
    return render_template('factions.html')

@app.route("/bosses")
def bosses():
    return render_template('bosses.html')

@app.route("/mobs")
def mobs():
    return render_template('mobs.html')



@app.route("/")
def frontpage():
    return render_template('frontpage.html')



class EventUI:
    def __init__(self, text, color, size):
        self.text = text
        self.color = color
        self.size = size

class Mob:
    mobevents = []
    def __init__(self, id = 0, name = 'Test1', dmg = 10, armor = 5, health = 100, img = 'bosses_legend_of_the_sea.png', loot = []):
        self.id = id
        self.name = name
        self.health = health
        self.armor = armor
        self.dmg = dmg
        self.img = img
        self.loot = loot
        self.eventlogs = []
        
    def doevent(self):
        user = {}
        target = 'FOXX'
        user['health'] = 100
        user['dmg'] = 10
        user['armor'] = 2
        i = 1
        while user['health'] > 0 and self.health > 0:
            if i%2 == 0:
                user_atk = np.random.randint(0, user['dmg'])
                dmg_dealt = round(user_atk/self.armor, 2)
                self.health -= dmg_dealt
                event = EventUI(f"{target} hit {self.name} for {dmg_dealt} damage!, {self.name} has {self.health} HP left.", "green", "30")
                self.eventlogs.append(event)
            else:
                monster_atk = np.random.randint(0, self.dmg)
                dmg_dealt = round(monster_atk/user['armor'], 2)
                user['health'] -= dmg_dealt
                health_left = user['health']
                event = EventUI(f"{self.name} hit {target} for {dmg_dealt} damage!, {target} has {health_left} HP left.", "red", "30")
                self.eventlogs.append(event)
            i += 1
        
        if self.health <= 0:
            event = EventUI(f"{target} WON!", "green", "30")
            self.eventlogs.append(event)
            event = EventUI(f"LOOT:  {self.loot}", "black", "30")
            self.eventlogs.append(event)

        if user['health'] <= 0:
            event = EventUI(f"{target} Lost!", "red", "30")
            self.eventlogs.append(event)
                    

#ed0ce8c7-a4fe-11eb-badb-40167e77d41a

class MonsterEventHandler(Resource):
    def get(self):
        id = str(uuid.uuid1())
        Mob.mobevents.append(Mob(id = id))
        return {'id': f'{id}'}, http.client.OK


@app.route("/events/<eventid>")
def event(eventid):
    for mobevent in Mob.mobevents:
        if eventid == mobevent.id:
            mobevent.doevent()
            return render_template('event.html', eventlogs = jsonpickle.encode(mobevent.eventlogs), mobimg = mobevent.img)
    return {'Response': 'Event does not exist'}, http.client.NOT_FOUND

api.add_resource(MonsterEventHandler, '/api/event/generate')


if __name__ == "__main__":
    socketio.run(app, debug=True)