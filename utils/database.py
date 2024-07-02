from sqlalchemy import create_engine

STOCK_RETURNS_DB_URL = 'sqlite:///db/stock_returns.db'

class DB():
    def __init__(self):
        engine = create_engine(STOCK_RETURNS_DB_URL)
        