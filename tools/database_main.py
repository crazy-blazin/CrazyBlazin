import pandas as pd
import numpy as np
import seaborn as sns
import os
import datetime
import matplotlib.pyplot as plt

class Database:

    def __init__(self):
        if os.path.exists('../database.txt'):
            with open('../database.txt', 'r') as f:
                self.db = eval(f.read())
        else:
            self.db = {'users': {}}
            with open('../database.txt', 'w') as f:
                f.write(str(self.db))

    def create_channel_for_user(self, username, channel_name):
        if username not in self.db['users']:
            self.db['users'][username] = {'channels_owned': [channel_name], 'coins': 0, 'channels_permission': []}
        else:
            self.db['users'][username]['channels_owned'].append(channel_name)
        self.write_data()

    def update_rights(self, username, channel_name, type = 'give'):
        if type == 'give':
            self.db['users'][username]['channels_permission'].append(channel_name)
        else:
            self.db['users'][username]['channels_permission'].remove(channel_name)
        self.write_data()
        
    def write_data(self):
        with open('../database.txt', 'w') as f:
            f.write(str(self.db))

    def read_data(self):
        with open('../database.txt', 'r') as f:
            self.db = eval(f.read())
    
    def reset_db(self):
        self.db = {}
        with open('../database.txt', 'r') as f:
            f.write(str(self.db))


    



        
    
            