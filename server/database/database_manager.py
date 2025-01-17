import sqlite3
import pandas as pd

class DatabaseManager:
    DATABASE_NAME = "inventory_management.db"

    def __init__(self):
        pass

    def __get_connection(self):
        return sqlite3.connect(DatabaseManager.DATABASE_NAME)
    
    def execute_query(self, query_string, query_parameters=[]):
        conn = self.__get_connection()
        cursor = conn.cursor()

        res = {"success":None, "msg":None, "data":None}        
        try:
            cursor.execute(query_string, query_parameters)
            conn.commit()
        
            res["success"] = True
            res["msg"] = "Success"
            res["data"]  = cursor.fetchall()
        except sqlite3.OperationalError as err:
            res["success"] = False
            res["msg"] = str(err)
        finally:
            conn.close()
        
        return res


    def create_tables(self, location_id):

        conn = self.__get_connection()
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS events
            (timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, staff_id INT, event TEXT, ingredient_id INT, 
                       change REAL, recipe_id INT)''')

        locations_df = pd.read_csv("server/csvs/locations.csv")
        locations_df.to_sql("locations", conn, if_exists="replace", index=False)

        all_staff_df = pd.read_csv("server/csvs/staff.csv")
        staff_df = all_staff_df[all_staff_df.location_id == location_id].drop(['location_id'], axis=1)
        staff_df.to_sql("staff", conn, if_exists="replace", index=False)

        modifiers_df = pd.read_csv("server/csvs/modifiers.csv")
        modifiers_df.to_sql("modifiers", conn, if_exists="replace", index=False)

        all_menus_df = pd.read_csv("server/csvs/menus.csv")
        menus_df = all_menus_df[all_menus_df.location_id == location_id].drop(['location_id'], axis=1)
        menus_df.to_sql("menus", conn, if_exists="replace", index=False)

        all_recipes_df = pd.read_csv("server/csvs/recipes.csv")
        recipes_df = all_recipes_df[all_recipes_df.recipe_id.isin(menus_df.recipe_id)]
        recipes_df.to_sql("recipes", conn, if_exists="replace", index=False)

        all_ingredients_df = pd.read_csv("server/csvs/ingredients.csv")
        ingredients_df = all_ingredients_df[all_ingredients_df.ingredient_id.isin(recipes_df.ingredient_id)].assign(quantity=0.0)
        ingredients_df.to_sql("ingredients", conn, if_exists="replace", index=False)

        conn.commit()
        conn.close()




