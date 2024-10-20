INIT_DB_TABLE = '''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, coins INTEGER)'''
ADD_COINS = '''INSERT INTO users (user_id, username, coins) VALUES (?, ?, ?)'''
UPDATE_COINS = '''UPDATE users SET coins=? WHERE user_id=?'''
GET_COINS = '''SELECT coins FROM users WHERE user_id=?'''
RESET_COINS = '''UPDATE users SET coins = 0 WHERE user_id = ?'''
INIT_LOTTO_TABLE = '''
CREATE TABLE IF NOT EXISTS lotto (
    user_id INTEGER,
    username TEXT,
    ticket_number INTEGER
);
'''

INIT_LOTTO_SUM_TABLE = '''
CREATE TABLE IF NOT EXISTS lotto_sum (
    total_sum INTEGER
);
'''