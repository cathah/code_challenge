# Code for initialising db etc, based on location
from server.database.database_manager import DatabaseManager

def db_setup():

    db_manager = DatabaseManager()
    db_manager.create_tables()


db_setup()