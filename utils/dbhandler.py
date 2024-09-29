import sqlite3
from dataclasses import dataclass
import utils.queries as queries
from config import config


@dataclass
class DataBaseHandler:
    db_name: str = config.DB_NAME

    def _get_connection(self):
        """Establish and return a database connection and cursor."""
        conn = sqlite3.connect(self.db_name, check_same_thread=False)  # Thread-safe connection
        return conn, conn.cursor()

    def __post_init__(self):
        """Initialize the database tables."""
        conn, c = self._get_connection()
        c.execute(queries.INIT_DB_TABLE)
        conn.commit()
        conn.close()

    def add_coins(self, user_id, username, amount):
        """Add coins to a user or create a new user entry if they don't exist."""
        conn, c = self._get_connection()
        c.execute(queries.GET_COINS, (user_id,))
        result = c.fetchone()
        if result is None:
            # User not in database, add them
            c.execute(queries.ADD_COINS, (user_id, username, amount))
        else:
            # Update coins for existing user
            new_amount = result[0] + amount
            c.execute(queries.UPDATE_COINS, (new_amount, user_id))
        conn.commit()
        conn.close()

    def run_query(self, query, params):
        """Execute a generic query with parameters and return the cursor."""
        conn, c = self._get_connection()
        c.execute(query, params)
        conn.commit()
        conn.close()
        return c

    def update_coins(self, user_id, amount):
        """Update the amount of coins for a specific user."""
        conn, c = self._get_connection()
        c.execute(queries.UPDATE_COINS, (amount, user_id))
        conn.commit()
        conn.close()

    def get_coins(self, user_id):
        """Retrieve the number of coins for a specific user."""
        conn, c = self._get_connection()
        c.execute(queries.GET_COINS, (user_id,))
        result = c.fetchone()
        conn.close()
        return result

    def reset_coins(self, user_id):
        """Reset the number of coins for a specific user."""
        conn, c = self._get_connection()
        c.execute(queries.RESET_COINS, (user_id,))
        conn.commit()
        conn.close()