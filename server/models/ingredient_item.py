from server.database.database_manager import DatabaseManager

class IngredientItem:
    
    def __init__(self, ing_id, name, unit, cost, quantity):
        self.ing_id = ing_id
        self.name = name
        self.unit = unit
        self.cost = cost
        self.quantity = quantity

    def save(self):
        db_manager = DatabaseManager()
        query_string = """  UPDATE ingredients 
                            SET ingredient_id = ?, name = ?, unit = ?, cost = ?, quantity =? 
                            WHERE ingredient_id = ?;"""
        res = db_manager.execute_query(query_string, [self.ing_id, self.name, self.unit, self.cost, self.quantity, self.ing_id])    
        if res["success"]:
            self.saved = True
            return True
        return False

    @staticmethod
    def get_all_ingredients():
        db_manager = DatabaseManager()
        query = "SELECT ingredient_id, name, unit, cost, quantity FROM ingredients"
        res = db_manager.execute_query(query)

        ingredient_list = (list(map(lambda row: IngredientItem(row[0], row[1], row[2], row[3], row[4]), res["data"])))        
        return ingredient_list
    

    @staticmethod
    def get_ingredient_by_id(ing_id):
        db_manager = DatabaseManager()
        query = "SELECT ingredient_id, name, unit, cost, quantity FROM ingredients WHERE ingredient_id = ?"
        res = db_manager.execute_query(query, [ing_id])

        ingredient = None
        if res["data"]:
            row = res["data"][0]
            ingredient = IngredientItem(row[0], row[1], row[2], row[3], row[4])
        return ingredient
    
    @staticmethod
    def get_ingredient_by_name(name):
        db_manager = DatabaseManager()
        query = "SELECT ingredient_id, name, unit, cost, quantity FROM ingredients WHERE name = ?"
        res = db_manager.execute_query(query, [name])

        ingredient = None
        if res["data"]:
            row = res["data"][0]
            ingredient = IngredientItem(row[0], row[1], row[2], row[3], row[4])
        return ingredient
        