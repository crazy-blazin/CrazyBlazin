# Mafia RPG SQL Queries

# Initialize the database
INIT_MAFIA_DB = '''
CREATE TABLE IF NOT EXISTS mafia_players (
    player_id INTEGER PRIMARY KEY,
    username TEXT,
    cash INTEGER,
    influence INTEGER
);
CREATE TABLE IF NOT EXISTS mafia_towns (
    player_id INTEGER PRIMARY KEY,
    drug_lab_level INTEGER,
    weapons_warehouse_level INTEGER,
    gang_hideout_level INTEGER,
    FOREIGN KEY (player_id) REFERENCES mafia_players(player_id)
);
CREATE TABLE IF NOT EXISTS mafia_resources (
    player_id INTEGER PRIMARY KEY,
    drugs INTEGER,
    weapons INTEGER,
    gang_members INTEGER,
    FOREIGN KEY (player_id) REFERENCES mafia_players(player_id)
);
'''

# Queries to add or update player data
ADD_MAFIA_PLAYER = '''INSERT INTO mafia_players (player_id, username, cash, influence) VALUES (?, ?, ?, ?)'''
UPDATE_PLAYER_CASH = '''UPDATE mafia_players SET cash=? WHERE player_id=?'''
GET_PLAYER_INFO = '''SELECT * FROM mafia_players WHERE player_id=?'''

# Town and resource queries
UPDATE_TOWN_FACILITY = '''UPDATE mafia_towns SET {facility}_level=? WHERE player_id=?'''
GET_TOWN_INFO = '''SELECT * FROM mafia_towns WHERE player_id=?'''

UPDATE_RESOURCES = '''UPDATE mafia_resources SET {resource}=? WHERE player_id=?'''
GET_RESOURCES = '''SELECT * FROM mafia_resources WHERE player_id=?'''
