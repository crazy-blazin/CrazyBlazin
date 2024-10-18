from beartype import beartype
from utils.dbhandler import DataBaseHandler

db_handler = DataBaseHandler()

@beartype
def add_coins(user_id: int, username: str, amount: int) -> None:
    print(f"Adding {amount} coins to {username} with user_id {user_id}")
    db_handler.add_coins(user_id=user_id, username=username, amount=amount)