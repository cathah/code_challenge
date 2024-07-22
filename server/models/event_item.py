from server.database.database_manager import DatabaseManager

class EventItem:
    
    def __init__(self, timestamp, event, ingredient_id, change, recipe_id, staff_id=0):
        self.timestamp = timestamp
        self.event = event
        self.ingredient_id = ingredient_id
        self.change = change
        self.recipe_id = recipe_id
        self.staff_id = staff_id # Defaults to 0 as staff tracking is not prioritised in this iteration


    def save(self):
        db_manager = DatabaseManager()
        query_string = "INSERT INTO events (timestamp, staff_id, event, ingredient_id, change, recipe_id) VALUES (?, ?, ?, ?, ?, ?)"
        res = db_manager.execute_query(query_string, [self.timestamp, self.staff_id, self.event, self.ingredient_id, self.change, self.recipe_id])    
        if res["success"]:
            self.saved = True
            return True
        return False

    @staticmethod
    def get_all_events():
        db_manager = DatabaseManager()
        query = "SELECT timestamp, event, ingredient_id, change, recipe_id, staff_id FROM events"
        res = db_manager.execute_query(query)

        event_list = (list(map(lambda row: EventItem(row[0], row[1], row[2], row[3], row[4], row[5]), res["data"])))        
        return event_list
    
    @staticmethod
    def get_events_by_date(start_date, end_date):
        db_manager = DatabaseManager()
        query = "SELECT timestamp, event, ingredient_id, change, recipe_id, staff_id FROM events WHERE timestamp >= ? AND timestamp < ?"
        res = db_manager.execute_query(query, [start_date, end_date])

        event_list = (list(map(lambda row: EventItem(row[0], row[1], row[2], row[3], row[4], row[5]), res["data"])))        
        return event_list
    

    def __str__(self):
        return f'The event is:\n\ttimestamp: {self.timestamp}\n\tstaff_id: {self.staff_id}\n\tevent: {self.event}\n\tingredient_id: {self.ingredient_id}\n\tchange: {self.change}\n\trecipe_id: {self.recipe_id}\n'
