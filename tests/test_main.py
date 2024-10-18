@pytest.fixture
def mock_db_handler():
    db_handler.add_coins = MagicMock()
    db_handler.get_coins = MagicMock()
    db_handler.reset_coins = MagicMock()
    db_handler.get_top_users = MagicMock()
    return db_handler

@pytest.fixture
def mock_bot():