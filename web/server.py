# #!/usr/bin/env python
# from flask import Flask, render_template, url_for, request, jsonify
# import pickle
# from datetime import datetime, time
# import numpy as np
# import io
# from PIL import Image
# import matplotlib.pyplot as plt
# import json
# import jsonpickle
# import random
# from flask import Flask, render_template, url_for, request, Response, send_file
# import http.client
# from datetime import datetime, time
# from matplotlib import image
# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt
# import os
# from pathlib import Path
# import uuid
# import glob
# import shutil
# import logging
# from werkzeug.datastructures import FileStorage
# from flask_restful import Resource, Api, reqparse
# from werkzeug.utils import secure_filename

# from flask_socketio import SocketIO

# from things import *
# import requests
# from tqdm import tqdm
# from zipfile import ZipFile
# import os
# import shutil
# import subprocess
# import time


# with open('version.txt', 'r') as f:
#     version = float(f.read())

# app = Flask(__name__)
# api = Api(app)

# logging.basicConfig(filename='server.log', level=logging.DEBUG)
# socketio = SocketIO(app, cors_allowed_origins="*", logger = logging)

# @socketio.on('msg')
# def msg(msg):
#     socketio.emit('clientMsg', msg, broadcast=True, include_self=False)

# @socketio.on('connect')
# def test_connect():
#     socketio.emit('datainfo', {'data': 'Connected'})

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')

# @app.route("/stonks")
# def front():
#     return render_template('stonks.html')

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
import asyncio
import subprocess
import pickle 

app = Flask(__name__)
api = Api(app)


# with open('version.txt', 'r') as f:
#     version = float(f.read())


# def download_url(url, save_path, chunk_size=128**4):
#     r = requests.get(url, stream=True)
#     with open(save_path, 'wb') as fd:
#         for chunk in tqdm(r.iter_content(chunk_size=chunk_size)):
#             fd.write(chunk)



# def extract_files(version, zip_url):
#     download_url(zip_url, f'{version}.zip')
#     with ZipFile(f'{version}.zip', 'r') as zipObj:
#         folder_name = list(zipObj.namelist())[0].split('/')[0]
#         # Extract all the contents of zip file in current directory
#         zipObj.extractall(f'{version}')
#         return folder_name

# def get_version():
#     url = 'https://api.github.com/repos/martinrovang/CrazyBlazin/releases'
#     r = requests.get(url)

#     fetched = r.json()[0]

#     zip_url = fetched['zipball_url']
#     version = float(fetched['tag_name'])

#     return zip_url, version

# def check_version():
#     global version
#     with open('version.txt', 'r') as f:
#         ver = float(f.read())
#     if version < ver:
#         exit()

# all_gifts = []

# class Gift:
#     def __init__(self, id, username, amount):
#         self.amount = amount
#         self.username = username
#         self.id = id

# def read_db():
#     try:
#         with open('../../database.txt', 'r') as f:
#             database = eval(f.read())
#         return database
#     except:
#         print('read error')


# def write_db(database):
#     try:
#         with open('../database.txt', 'w', encoding='utf-8') as f:
#             f.write(str(database))
#     except:
#         print('write error')



# @app.route("/")
# def frontpage():
#     return 'frontpage'

# @app.route("/admin/userinfo")
# def userinfo():
#     database = read_db()
#     return database


data = {'data':{'points': [[],[]] }}



@app.route("/update")
def upd():
    global data
    data['data']['points'][0].append(random.randint(0, 100))
    data['data']['points'][1].append(datetime.now().strftime("%H:%M:%S"))
    return data
    # return render_template('lootcrate.html')



@app.route('/search', methods=['POST'])
def search():
  return jsonify(['my_series', 'another_series'])

@app.route('/')
def health_check():
  return 'This datasource is healthy.'



@app.route("/query")
def test():
    global data
    return jsonify(data)
    # return render_template('lootcrate.html')


# @app.route("/restart")
# def end():
#     subprocess.run("start restart.bat", shell=True, check=True)



# @app.route("/<id>/shop")
# def shop(id):
#     return render_template('cards.html')
    

# @app.route("/admin/api/gift_creation/<id>/<username>/<amount>")
# def create_gift(id, username, amount):
#     all_gifts.append(Gift(id, username, round(float(amount),2)))
#     return f'Gift created! -> {id}, {username}, {amount}'



# @app.route("/giftpage/<id>")
# def giftpage(id):
#     return render_template('get_gift.html')



# @app.route("/<id>/shop")
# def button_gift(id):
#     return render_template('get_gift.html')

    

# @app.route("/admin/api/gift_creation/<id>/<username>/<amount>")
# def create_gift(id, username, amount):
#     all_gifts.append(Gift(id, username, round(float(amount),2)))
#     return f'Gift created! -> {id}, {username}, {amount}'


# @app.route("/api/<id>")
# def redeem(id):
#     database = read_db()
#     lock = True
#     for gift in all_gifts:
#         if gift.id == id:
#             with open('giftcard.txt', 'a') as f:
#                 out = [gift.username, gift.amount]
#                 f.write(str(out)+'\n')
#             all_gifts.remove(gift)
#             lock = False
#     if lock:
#         return f'This gift code is no longer valid!'
#     else:
#         write_db(database)
#         return f'<h1>Gift redeemed! {gift.username} recieved {gift.amount} CBC!</h1>'
#     # return f'{gift.username} recieved {gift.amount}!'


print('Server running')

if __name__ == "__main__":
    # socketio.run(app, debug=True)
    app.run(debug=True)
