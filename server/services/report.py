from datetime import datetime, timezone
from server.database.database_manager import DatabaseManager
from server.models.ingredient_item import IngredientItem
from server.models.recipe_item import RecipeItem
from server.models.event_item import EventItem

import pandas as pd

class Report:
    def __init__(self, total_delivery_cost=0, total_revenue=0, total_inventory_value=0, total_waste_cost=0):

        self.total_delivery_cost = total_delivery_cost
        self.total_revenue = total_revenue
        self.total_inventory_value = total_inventory_value
        self.total_waste_cost = total_waste_cost

    
    def calculate_total_delivery_cost(self):

        event_list = EventItem.get_all_events()
        event_df = pd.DataFrame([obj.__dict__ for obj in event_list])
        filtered_df = event_df.loc[event_df['event'] == 'accept.delivery'][['ingredient_id', 'change']]

        inventory_list = IngredientItem.get_all_ingredients()
        inventory_df = pd.DataFrame([obj.__dict__ for obj in inventory_list])[['ing_id', 'cost']]
  
        joined_df = pd.merge(filtered_df, inventory_df, left_on=['ingredient_id'], right_on=['ing_id'], how = 'left')
        delivery_cost = (joined_df['change'] * joined_df['cost']).sum()

        self.total_delivery_cost = round(delivery_cost, 2)


    def calculate_total_revenue(self):
        event_list = EventItem.get_all_events()
        event_df = pd.DataFrame([obj.__dict__ for obj in event_list])
        filtered_df = event_df.loc[event_df['event'] == 'sell.item'][['timestamp', 'recipe_id']].drop_duplicates()

        db_manager = DatabaseManager()
        query = "SELECT recipe_id, price FROM menus" # Menus model could be implemented in future
        res = db_manager.execute_query(query)
        pricing_df = pd.DataFrame(res["data"], columns=['recipe_id', 'price'])

        joined_df = pd.merge(filtered_df, pricing_df, left_on=['recipe_id'], right_on=['recipe_id'], how = 'left')
        total_revenue = joined_df['price'].sum()

        self.total_revenue = round(total_revenue, 2)


    def calculate_total_inventory_value(self):

        inventory_list = IngredientItem.get_all_ingredients()
        inventory_df = pd.DataFrame([obj.__dict__ for obj in inventory_list])
        inventory_value = (inventory_df['cost'] * inventory_df['quantity']).sum()

        self.total_inventory_value = round(inventory_value, 2)


    def calculate_total_waste_cost(self):

        event_list = EventItem.get_all_events()
        event_df = pd.DataFrame([obj.__dict__ for obj in event_list])
        filtered_df = event_df[(event_df['event'] == 'take.stock') & (event_df['change'] < 0 )][['ingredient_id', 'change']]
        print(filtered_df)

        inventory_list = IngredientItem.get_all_ingredients()
        inventory_df = pd.DataFrame([obj.__dict__ for obj in inventory_list])[['ing_id', 'cost']]
  
        joined_df = pd.merge(filtered_df, inventory_df, left_on=['ingredient_id'], right_on=['ing_id'], how = 'left')
        waste_cost = (joined_df['change'] * joined_df['cost']).sum()

        self.total_waste_cost = round((-1*waste_cost), 2)
        

