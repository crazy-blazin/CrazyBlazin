from flask import Flask, render_template, url_for
import pickle
from datetime import datetime, time
import numpy as np
app = Flask(__name__)
import io
from PIL import Image
import matplotlib.pyplot as plt
# START_TIME = time(hour=9)
# END_TIME = time(hour=12)  # Can also use something like timedelta
# if START_TIME <= now.time() <= END_TIME:    


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


if __name__ == "__main__":
    app.run(debug=True)