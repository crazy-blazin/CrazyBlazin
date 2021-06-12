from flask import Flask, render_template, url_for, request, jsonify
import pickle
from datetime import datetime, time
import numpy as np
import io
from PIL import Image
import matplotlib.pyplot as plt
import json
import jsonpickle
import random
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
import logging
from werkzeug.datastructures import FileStorage
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename

from flask_socketio import SocketIO

from things import *


app = Flask(__name__)
api = Api(app)

logging.basicConfig(filename='server.log', level=logging.DEBUG)
socketio = SocketIO(app, cors_allowed_origins="*", logger = logging)

@socketio.on('msg')
def msg(msg):
    socketio.emit('clientMsg', msg, broadcast=True, include_self=False)

@socketio.on('stonk_values')
def stonk_values(stonk_values):
    socketio.emit('clientMsg', stonk_values, broadcast=True, include_self=False)

@socketio.on('connect')
def test_connect():
    socketio.emit('datainfo', {'data': 'Connected'})

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
    
    with open('mobs.txt', 'r') as f:
        mobs = eval(f.read())
    return render_template('mobs.html', mobs = mobs)

@app.route("/")
def frontpage():
    return render_template('frontpage.html')

#ed0ce8c7-a4fe-11eb-badb-40167e77d41a

class MonsterEventHandler(Resource):
    def get(self, username, mobtype):
        id = str(uuid.uuid1())
        mobevent = Mob(username, mobtype, id = id)
        ticketcheck = mobevent.check_if_possible()
        if ticketcheck:
            User.update()
            feedback = mobevent.doevent()
            User.update()
            User.writetodb()
            Faction.update()
            Faction.writetodb()
            feedback['id'] = id
            feedback['img'] = mobevent.img
            feedback['name'] = mobevent.name
            return feedback, http.client.OK
        else:
            return {'info': False, 'id': f'{id}', 'img': f'{mobevent.img}', 'name': mobevent.name}, http.client.OK

class BossEventHandler(Resource):
    def get(self, factionid, bosstype):
        id = str(uuid.uuid1())
        bossevent = Boss(factionid, bosstype, id = id)
        ticketcheck = bossevent.check_if_possible()
        if ticketcheck:
            User.update()
            Faction.update()
            feedback = bossevent.doevent()
            User.update()
            Faction.update()
            User.writetodb()
            Faction.writetodb()
            feedback['id'] = id
            feedback['img'] = bossevent.img
            feedback['name'] = bossevent.name
            return feedback, http.client.OK
        else:
            return {'info': False, 'id': f'{id}', 'img': f'{bossevent.img}', 'name': bossevent.name}, http.client.OK


class Performtick(Resource):
    def get(self):
        # check = request.data['data']
        # print(check)
        Faction.update()
        User.update()
        User.tick()
        Faction.tick()
        User.writetodb()
        Faction.writetodb()
        return {'Info': 'Tick performed'}, http.client.OK
        # else:
        #     return {'Info': 'Not valid'}, http.client.OK


class CreateUser(Resource):
    def get(self, user):
        lock = True
        for username in User.all_users:
            if user == username.name:
                lock = False
        if lock:
            User.makeuser(user)
        User.update()
        User.writetodb()
        return {'Info': 'User created'}, http.client.OK
        # else:
        #     return {'Info': 'Not valid'}, http.client.OK


class Updateall(Resource):
    def get(self):
        # check = request.data['data']
        # print(check)
        Faction.update()
        User.update()
        User.writetodb()
        Faction.writetodb()
        return {'Info': 'Update performed!'}, http.client.OK
        # else:
        #     return {'Info': 'Not valid'}, http.client.OK


class GetInfo(Resource):
    def get(self):
        with open('database.txt', 'r') as f:
            database = eval(f.read())
        return database, http.client.OK

class BuyItem(Resource):
    def get(self, username, payment, itemname, amount):
        for user in User.all_users:
            if user.name == username:
                user.coins -= round(float(payment),2)
                user.coins = round(user.coins,2)
                user.add_item(itemname = itemname, amount = int(amount))
        return {'info': 'Item added.'}, http.client.OK


class WriteInfoUser(Resource):
    def post(self):
        data_incoming = request.get_json()
        for user in User.all_users:
            user.basemaxhealth = data_incoming[user.name]['basemaxhealth']
            user.maxtickets = data_incoming[user.name]['maxtickets']
            user.health_regen_base = data_incoming[user.name]['health_regen_base']
            user.health = data_incoming[user.name]['health']
            user.armor = data_incoming[user.name]['armor']
            user.dmg = data_incoming[user.name]['dmg']
            user.coins = data_incoming[user.name]['coins']
            user.itemsDB = data_incoming[user.name]['itemsDB']
            user.total_income = data_incoming[user.name]['total_income']
            user.faction = data_incoming[user.name]['faction']
            user.stonksDB = data_incoming[user.name]['stonksDB']
            user.coinpertick_base = data_incoming[user.name]['coinpertick_base']
            user.tickets = data_incoming[user.name]['tickets']

        User.update()
        User.writetodb()
        return {'Info': 'Update performed!'}, http.client.OK



@app.route("/mob/<eventid>")
def mobevent(eventid):
    for mobevent in Mob.mobevents:
        if eventid == mobevent.id:
            return render_template('event.html', eventlogs = jsonpickle.encode(mobevent.eventlogs), mobimg = mobevent.img)
        else:
            pass
    return {'Response': 'Event does not exist'}, http.client.NOT_FOUND

@app.route("/boss/<eventid>")
def bossevent(eventid):
    for bossevent in Boss.bossevents:
        if eventid == bossevent.id:
            return render_template('event.html', eventlogs = jsonpickle.encode(bossevent.eventlogs), mobimg = bossevent.img)
        else:
            pass
    return {'Response': 'Event does not exist'}, http.client.NOT_FOUND

api.add_resource(MonsterEventHandler, '/api/mob/generate/<username>/<mobtype>')
api.add_resource(BossEventHandler, '/api/boss/generate/<factionid>/<bosstype>')
api.add_resource(Performtick, '/api/admin/performtick')
api.add_resource(Updateall, '/api/admin/updateall')
api.add_resource(GetInfo, '/api/admin/getinfo')
api.add_resource(WriteInfoUser, '/api/admin/writeinfouser')
api.add_resource(CreateUser, '/api/admin/createuser/<user>')
api.add_resource(BuyItem, '/api/admin/items/<username>/<payment>/<itemname>/<amount>')


The_high_council = Faction(name = 'The High Council')
The_resistance = Faction(name = 'The Resistance')




User.readdb()
Faction.readdb()
Items.init_items()
Faction.init_members()
Faction.update()
User.update()



# if __name__ == "__main__":
socketio.run(app, debug=True)