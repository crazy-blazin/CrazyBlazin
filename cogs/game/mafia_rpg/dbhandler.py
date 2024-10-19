import sqlite3
from dataclasses import dataclass
from beartype import beartype
from beartype.typing import Tuple, Union
import utils.queries as queries
from cogs.game.mafia_rpg.mafia_config import config

@dataclass
class MafiaDBHandler:
    db_name: str = config.MAFIA_DB_NAME

    @beartype
    def _get_connection(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        """Establish and return a database connection and cursor."""
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        return conn, conn.cursor()

    def _execute_query(self, query, params=()):
        """General method to execute a query and handle connection."""
        conn, c = self._get_connection()
        c.execute(query, params)
        conn.commit()
        conn.close()

    def _fetch_query(self, query, params=()):
        """General method to fetch results from a query."""
        conn, c = self._get_connection()
        c.execute(query, params)
        result = c.fetchone()
        conn.close()
        return result

    def add_player(self, player_id: int, username: str) -> None:
        """Add a new player to the mafia game."""
        self._execute_query(queries.ADD_MAFIA_PLAYER, (player_id, username, 1000, 0))
        self._execute_query("INSERT INTO mafia_towns (player_id, drug_lab_level, weapons_warehouse_level, gang_hideout_level) VALUES (?, 1, 1, 1)", (player_id,))
        self._execute_query("INSERT INTO mafia_resources (player_id, drugs, weapons, gang_members) VALUES (?, 0, 0, 0)", (player_id,))

    def get_player_info(self, player_id: int) -> Union[None, Tuple]:
        """Get the player's mafia profile info."""
        return self._fetch_query(queries.GET_PLAYER_INFO, (player_id,))

    def update_cash(self, player_id: int, cash: int) -> None:
        """Update player's cash."""
        self._execute_query(queries.UPDATE_PLAYER_CASH, (cash, player_id))

    def get_town_info(self, player_id: int) -> Union[None, Tuple]:
        """Get town information for the player."""
        return self._fetch_query(queries.GET_TOWN_INFO, (player_id,))

    def update_facility(self, player_id: int, facility: str, level: int) -> None:
        """Update facility level for the player's town."""
        query = queries.UPDATE_TOWN_FACILITY.format(facility=facility)
        self._execute_query(query, (level, player_id))

    def get_resources(self, player_id: int) -> Union[None, Tuple]:
        """Get player's resources (drugs, weapons, gang members)."""
        return self._fetch_query(queries.GET_RESOURCES, (player_id,))

    def update_resource(self, player_id: int, resource: str, amount: int) -> None:
        """Update the amount of a specific resource for a player."""
        query = queries.UPDATE_RESOURCES.format(resource=resource)
        self._execute_query(query, (amount, player_id))
