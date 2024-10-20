import sqlite3
from dataclasses import dataclass

from beartype import beartype
from beartype.typing import Tuple, Union
from loguru import logger

import utils.queries as queries
from config import config


@dataclass
class DataBaseHandler:
    db_name: str = config.DB_NAME

    @beartype
    def _get_connection(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        """Establish and return a database connection and cursor."""
        conn = sqlite3.connect(self.db_name, check_same_thread=False)  # Thread-safe connection
        return conn, conn.cursor()

    @beartype
    def __post_init__(self) -> None:
        """Initialize the database tables."""
        conn, c = self._get_connection()
        c.execute(queries.INIT_DB_TABLE)
        c.execute(queries.INIT_LOTTO_TABLE)
        c.execute(queries.INIT_LOTTO_SUM_TABLE)
        conn.commit()
        conn.close()

    @beartype
    def add_coins(self, user_id: int, username: str, amount: int) -> None:
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

    @beartype
    def run_query(self, query: str, params: tuple) -> sqlite3.Cursor:
        """Execute a generic query with parameters and return the cursor."""
        conn, c = self._get_connection()
        c.execute(query, params)
        conn.commit()
        conn.close()
        return c

    @beartype
    def update_coins(self, user_id: int, amount: int) -> None:
        """Update the amount of coins for a specific user."""
        conn, c = self._get_connection()
        c.execute(queries.UPDATE_COINS, (amount, user_id))
        conn.commit()
        conn.close()

    @beartype
    def get_coins(self, user_id: int) -> Union[None, Tuple[int]]:
        """Retrieve the number of coins for a specific user."""
        conn, c = self._get_connection()
        c.execute(queries.GET_COINS, (user_id,))
        result = c.fetchone()
        conn.close()
        return result

    @beartype
    def reset_coins(self, user_id: int) -> None:
        """Reset the number of coins for a specific user."""
        conn, c = self._get_connection()
        c.execute(queries.RESET_COINS, (user_id,))
        conn.commit()
        conn.close()

    @beartype
    def get_top_users(self, limit: int) -> list:
        """Retrieve the top users with the most coins."""
        conn, c = self._get_connection()
        c.execute(f'SELECT * FROM users ORDER BY coins DESC LIMIT {limit}')
        result = c.fetchall()
        conn.close()
        return result

    @beartype
    def add_lotto_ticket(self, user_id: int, ticket_number: int) -> None:
        """Add a lotto ticket for the user."""
        logger.info('Adding lotto ticket...')
        conn, c = self._get_connection()
        c.execute('INSERT INTO lotto (user_id, ticket_number) VALUES (?, ?)', (user_id, ticket_number))
        conn.commit()
        conn.close()
    
    @beartype
    def add_lotto_sum(self, added_value: int) -> None:
        """Add a lotto ticket for the user."""
        logger.info('Adding lotto sum...')
        conn, c = self._get_connection()
        c.execute('SELECT total_sum FROM lotto_sum')
        result = c.fetchone()
        if result is None:
            c.execute('INSERT INTO lotto_sum (total_sum) VALUES (?)', (added_value,))
        else:
            new_value = result[0] + added_value
            c.execute('UPDATE lotto_sum SET total_sum = ?', (new_value,))
        conn.commit()
        conn.close()
    

    @beartype
    def get_lotto_sum(self) -> int:
        """Get the total sum of the lotto."""
        logger.info('Getting total lotto sum...')
        conn, c = self._get_connection()
        c.execute('SELECT total_sum FROM lotto_sum')
        result = c.fetchone()
        conn.close()
        return result[0] if result else 0

    @beartype
    def reset_lotto_tickets(self) -> None:
        """Reset all lotto tickets."""
        logger.info('Resetting lotto tickets...')
        conn, c = self._get_connection()
        c.execute('DELETE FROM lotto')
        c.execute('DELETE FROM lotto_sum')
        c.execute(f'INSERT INTO lotto_sum (total_sum) VALUES ({config.LOTTO_BASELINE})')
        conn.commit()
        conn.close()
    
    @beartype
    def find_finner(self, winning_ticket: int) -> int:
        """Find the winner of the lotto."""
        conn, c = self._get_connection()
        c.execute('SELECT user_id FROM lotto WHERE ticket_number = ?', (winning_ticket,))
        # fetch all winners
        result = c.fetchall()
        conn.close()
        return result