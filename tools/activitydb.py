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
            self.db['Time'].append(str(datetime.datetime.now().strftime('%H')))
        
        for data_point_key in set(self.db['Activity']):
            if data_point_key not in data:
                self.db['Activity'].append(data_point_key)
                self.db['Amount'].append(0)
                self.db['Time'].append(str(datetime.datetime.now().strftime('%H')))
        
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
        # pd.options.mode.chained_assignment = None  # default='warn'
        data=pd.DataFrame(self.db)
        fig, ax = plt.subplots(1, 1, figsize=(20,10), dpi=250)
        data['Timenew'] = data['Time'].astype(int).copy() - 7
        data['Timenew'][data['Timenew'] < 0] += 24
        sns.lineplot(x='Timenew', y='Amount', data=data, hue="Activity", style="Activity", alpha =.6, ax = ax, markers=True, dashes=False)
        plt.ylim([0, 6])
        # ['08', '09', '10', '11', '12', '13', '14','15', '16', '17', '18', '19', '20', '21', '22', '23', '00', '01', '02', '03', '04', '05', '06', '07']
        timetable  = np.array(['07','08', '09', '10', '11', '12', '13', '14','15', '16', '17', '18', '19', '20', '21', '22', '23', '00', '01', '02', '03', '04', '05', '06']).astype('int')
        plt.xticks(range(24), timetable, rotation = 45) # Rotates X-Axis Ticks by 45-degrees
        plt.legend(fontsize=10) # using a size in points
        plt.tight_layout()
        plt.title('Activity @ crazy blazin')
        plt.savefig('../activitydb.png')
        plt.close()

    
    



        
    
            