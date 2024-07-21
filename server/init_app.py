from server.database.database_manager import DatabaseManager

def db_setup():

    print('Please enter your location ID. (This can be found in server/csvs/staff.csv)')
    location_id = int(input())

    db_manager = DatabaseManager()
    db_manager.create_tables(location_id) 


db_setup()