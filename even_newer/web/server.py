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



def read_db():
    try:
        with open('../database.txt', 'r') as f:
            database = eval(f.read())
        return database
    except:
        print('read error')

@app.route("/")
def frontpage():
    return 'frontpage'

@app.route("/admin/userinfo")
def userinfo():
    database = read_db()
    return database


@app.route("/test")
def test():
    return render_template('lootcrate.html')



if __name__ == "__main__":
    # socketio.run(app, debug=True)
    app.run(debug=True)