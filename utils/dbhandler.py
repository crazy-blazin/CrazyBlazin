import sqlite3
from dataclasses import dataclass
import utils.queries as queries
from config import config


@dataclass
class DataBaseHandler:
    conn: sqlite3.Connection = sqlite3.connect(config.DB_NAME)
    c: sqlite3.Cursor = conn.cursor()

    def __post_init__(self):
        self.c.execute(queries.INIT_DB_TABLE)
        self.conn.commit()

    def add_coins(self, user_id, username, amount):
        self.c.execute(queries.GET_COINS, (user_id,))
        result = self.c.fetchone()
        if result is None:
            # User not in database, add them
            self.c.execute(queries.ADD_COINS, (user_id, username, amount))
        else:
            # Update coins for existing user
            new_amount = result[0] + amount
            self.c.execute(queries.UPDATE_COINS, (new_amount, user_id))
        self.conn.commit()

    def get_coins(self, user_id):
        self.c.execute(queries.GET_COINS, (user_id,))
        result = self.c.fetchone()
        return result

    def reset_coins(self, user_id):
        self.c.execute(queries.RESET_COINS, (user_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
