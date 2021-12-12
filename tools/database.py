import psycopg2
import pandas as pd
from datetime import datetime, time
import numpy as np


class database_system:
    def __init__(self):
        with open('../../db.conf') as f:
            data = eval(f.read())
            print('Connecting to database...')
        self.conn = psycopg2.connect(
            host=data['host'],
            port = data['port'],
            database=data['database'],
            user=data['user'],
            password=data['password'])
        self.cur = self.conn.cursor()

    def add_table(self, nameof, columns):
        self.cur.execute(
        f"""
        CREATE TABLE {nameof} ({columns});""")
        self.conn.commit()
        print(f'Table {nameof} added!')
    
    def remove_table(self, nameof):
        self.cur.execute(
        f"""
        DROP TABLE {nameof};""")
        self.conn.commit()
        print(f'Table {nameof} removed!')

    def remove_user(self, tablename, name):
        self.cur.execute(
        f"""
        DELETE FROM {tablename}
        WHERE name = '{name}';""")
        self.conn.commit()
        print(f'User {name} removed!')
    
    def add_user(self, name, coins = 100, valtype = 'coins', dbname = 'users'):
        self.cur.execute(
        f"""
        INSERT INTO {dbname}(
        name,
        {valtype})
        VALUES ('{name}', {coins});""")
        self.conn.commit()
        print(f'User {name} added!')
    
    def change_val(self, name, newval, valtype = 'coins' , dbname = 'users'):
        self.cur.execute(
        f"""
        UPDATE {dbname}
        SET {valtype} = {newval}
        WHERE name = '{name}';""")
        self.conn.commit()
        print(f'User {name} got changed values!')

    def add_tickcoins(self, names  = ['penisman', 'somenewperson'], newval = 1, valtype = 'coins', dbname = 'users'):
        for user in names:
            self.cur.execute(
            f"""
            UPDATE {dbname}
            SET {valtype} = {valtype} + {newval}
            WHERE name = '{user}';""")
        self.conn.commit()
        print(f'Tick coins added')

    def fetch_user_data(self, name, datatype = 'coins', dbname = 'users'):
        self.cur.execute(
        f"""
        SELECT {datatype} FROM {dbname} WHERE name = '{name}';
        """)
        data = self.cur.fetchall()[0]
        return data
    
    def fetch_all(self, dbname = 'users'):
        self.cur.execute(
        f"""
        SELECT * FROM {dbname};
        """)
        columns = [x[0] for x in self.cur.description]
        tmp = self.cur.fetchall()
        data = pd.DataFrame(tmp, columns=columns)
        return data
    

    def add_gaming(self, game, extra = None, dbname = 'gaminglist'):
        self.cur.execute(
        f"""
        INSERT INTO {dbname}(
        whatgame,
        extra)
        VALUES ('{game}',  '{extra}');""")
        self.conn.commit()
        print(f'Game info added!')
    

    def setup_dbs(self):
        self.cur.execute(
        f"""
        CREATE TABLE gaminglist (whatgame INTEGER, created_at timestamptz NOT NULL DEFAULT now(), extra VARCHAR(500) );""")
        self.cur.execute(
        f"""
        CREATE TABLE users (username VARCHAR(50), coins INTEGER, extra VARCHAR(500) );""")
        self.conn.commit()
        print(f'Table SETUP FINISHED!')


db = database_system()
# db.remove_table('users')
# db.remove_table('gaminglist')
# db.setup_dbs()
db.add_gaming(np.random.randint(1, 100))
# db.add_tickcoins()
# db.remove_user('users', 'penisman')
# db.add_table('gaminglist',
#  """
#     horse VARCHAR(50),
#     price INTEGER,
#     amount INTEGER
#   """)

# db.change_val('penisman', 100)
# db.add_user('penisman', 100)
# data = db.fetch_all()
# print(db.fetch_user_data('penisman', 'coins', dbname = 'users'))