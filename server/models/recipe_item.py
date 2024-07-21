from server.database.database_manager import DatabaseManager
import pandas as pd

pd.set_option("max_columns", None) 
pd.set_option("max_colwidth", None) 
pd.set_option("max_rows", None) 

class RecipeItem:
    
    def __init__(self, recipe_id, name, ing_dict):
        self.recipe_id = recipe_id
        self.name = name
        self.ing_dict = ing_dict

    def get_ingredients(self):
        return list(self.ing_dict.keys())

    @staticmethod
    def get_all_recipes():
        db_manager = DatabaseManager()
        query = "SELECT recipe_id, name, quantity, ingredient_id FROM recipes"
        res = db_manager.execute_query(query)
        recipe_df = convert_query_results_to_dict_df_format(res["data"])
        return recipe_df

    @staticmethod
    def get_recipe_by_id(recipe_id):
        db_manager = DatabaseManager()
        query = "SELECT recipe_id, name, quantity, ingredient_id FROM recipes WHERE recipe_id = ?"
        res = db_manager.execute_query(query, [recipe_id])

        recipe = None
        if res["data"]:
            recipe_df = convert_query_results_to_dict_df_format(res["data"])
            row = recipe_df.iloc[0]
            recipe = RecipeItem(row[0], row[1], explode_list_of_dict_entries(row[2]))
        return recipe

    @staticmethod
    def get_recipe_by_name(recipe_name):
        db_manager = DatabaseManager()
        query = "SELECT recipe_id, name, quantity, ingredient_id FROM recipes WHERE name = ?"
        res = db_manager.execute_query(query, [recipe_name])

        recipe = None
        if res["data"]:
            recipe_df = convert_query_results_to_dict_df_format(res["data"])
            row = recipe_df.iloc[0]
            recipe = RecipeItem(row[0], row[1], explode_list_of_dict_entries(row[2]))
        return recipe


    def __str__(self):
            return f'The recipe is:\n\tid: {self.recipe_id}\n\tname: {self.name}\n\tingredient dict: {self.ing_dict}\n'
    

def convert_query_results_to_dict_df_format(query_result):
    raw_recipe_df = pd.DataFrame(query_result, columns=['recipe_id', 'name', 'quantity', 'ingredient_id'])
    raw_recipe_df['ing_dict'] = raw_recipe_df.apply(lambda row: {row['ingredient_id']:row['quantity']}, axis=1)
    recipe_df = (raw_recipe_df.groupby('recipe_id')
                                .agg({'recipe_id': 'first',
                                        'name': 'first',
                                        'ing_dict': list
                                }))
    return recipe_df

def explode_list_of_dict_entries(dct_list):
    dct = {}
    for sub_dict in dct_list:
        dct.update(sub_dict)
    return dct
