import pandas as pd
import numpy as np
import seaborn as sns
import os
import datetime
import matplotlib.pyplot as plt

class ActivityDB:

    def __init__(self):
        if os.path.exists('../activitydb.txt'):
            with open('../activitydb.txt', 'r') as f:
                self.db = eval(f.read())
        else:
            self.db = {'Activity': [], 'Amount': [], 'Time': []}
            with open('../activitydb.txt', 'w') as f:
                f.write(str(self.db))
    
    def update_stats(self, data):
        for data_point_key in data:
            self.db['Activity'].append(data_point_key)
            self.db['Amount'].append(data[data_point_key])
            self.db['Time'].append(str(datetime.datetime.now().strftime('%H:%M:%S')))
        
        for data_point_key in set(self.db['Activity']):
            if data_point_key not in data:
                self.db['Activity'].append(data_point_key)
                self.db['Amount'].append(0)
                self.db['Time'].append(str(datetime.datetime.now().strftime('%H:%M:%S')))

        self.write_data()
    
    def write_data(self):
        with open('../activitydb.txt', 'w') as f:
            f.write(str(self.db))

    def read_data(self):
        with open('../activitydb.txt', 'r') as f:
            self.db = eval(f.read())
    
    def reset_db(self):
        self.db = {}
        with open('../activitydb.txt', 'r') as f:
            f.write(str(self.db))


    def plot_data(self):
        plt.rcParams["xtick.labelsize"] = 7
        fig, ax = plt.subplots(1, 1, figsize=(15,10))
        sns.lineplot(x='Time', y='Amount', data=pd.DataFrame(self.db), hue="Activity", style="Activity", alpha =.6, ax = ax, markers=True, dashes=False)
        plt.ylim([0, 10])
        plt.legend(fontsize=10) # using a size in points
        plt.tight_layout()
        plt.title('Activity @ crazy blazin')
        plt.savefig('../activitydb.png')
        plt.close()

    
    



        
    
            