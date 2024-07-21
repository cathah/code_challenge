from flask import Flask, jsonify, request
from server.models.ingredient_item import IngredientItem
from server.models.recipe_item import RecipeItem

import json


app = Flask(__name__)

def main():
    print("Hello, this is the server! To activate, please run the following command: ")
    print("FLASK_APP=server/main flask run")


@app.route("/")
def index():
    return jsonify(
        hello = "World!!"
    )

### View Data Endpoints

@app.route("/list_inventory/all")
def get_all_inventory():
    inventory_list = IngredientItem.get_all_ingredients()
    resp = []
    for item in inventory_list:
        resp.append({
            "ingredient_id": item.ing_id,
            "name": item.name,
            "quantity": item.quantity,
            "unit": item.unit
        })
    return jsonify(resp)

@app.route("/list_inventory/<ing_id>")
def get_inventory_by_ingredient_id(ing_id):
    ingredient = IngredientItem.get_ingredient_by_id(ing_id)
    if ingredient:
        return jsonify({ 
            "ingredient_id": ingredient.ing_id,
            "name": ingredient.name,
            "quantity": ingredient.quantity,
            "unit": ingredient.unit
        })
    else:
        return jsonify({})

@app.route("/list_inventory/name/<ing_name>")
def get_inventory_by_ingredient_name(ing_name):
    ingredient = IngredientItem.get_ingredient_by_name(ing_name)
    if ingredient:
        return jsonify({ 
            "ingredient_id": ingredient.ing_id,
            "name": ingredient.name,
            "quantity": ingredient.quantity,
            "unit": ingredient.unit
        })
    else:
        return jsonify({})

@app.route("/list_recipes/all")
def get_all_recipes():
    recipe_df = RecipeItem.get_all_recipes()
    all_recipes_json = recipe_df.to_json(orient='records')
    return(all_recipes_json)

@app.route("/list_recipes/<recipe_id>")
def get_recipe_by_id(recipe_id):
    recipe = RecipeItem.get_recipe_by_id(recipe_id)
    if recipe:
        return jsonify({ 
            "recipe_id": int(recipe.recipe_id),
            "name": recipe.name,
            "ing_dict": str(recipe.ing_dict)
        })
    else:
        return jsonify({})

@app.route("/list_recipes/name/<recipe_name>")
def get_recipe_by_name(recipe_name):
    recipe = RecipeItem.get_recipe_by_name(recipe_name)
    if recipe:
        return jsonify({ 
            "recipe_id": int(recipe.recipe_id),
            "name": recipe.name,
            "ing_dict": str(recipe.ing_dict)
        })
    else:
        return jsonify({})
    

@app.route("/list_events/all")
def get_all_events():
    return jsonify(
        get = "all events"
    )




### Event Endpoints

@app.route("/accept_delivery/", methods=["POST"])
def accept_delivery():

    request_data = request.get_json()

    all_items_saved = True
    error_ids = []
    for key, value in request_data.items():
        try:
            ingredient = IngredientItem.get_ingredient_by_id(key)
            ingredient.quantity += float(value)
            ingredient.save()
        
        except AttributeError:
            all_items_saved = False
            error_ids.append(key)
        
    if all_items_saved:
        return jsonify(code=200, msg="Success")
    else:
        return jsonify(code=400, msg=f"Error saving some results. Please refer to inventory IDs and try again if needed. Invalid Ids: {error_ids}")


@app.route("/sell_item/", methods=["POST"])
def sell_item():
    request_data = json.loads(request.get_json())

    all_recipes_saved = True
    error_recipes = []
    error_msg = ''
    for recipe_id in request_data:
        try:
            recipe = RecipeItem.get_recipe_by_id(recipe_id)
            ing_ids = recipe.get_ingredients()
        except AttributeError:
            error_msg = ('Invalid recipe entered. Please check inventory as update may not occur for: ' + str(recipe_id))
            all_recipes_saved = False
            continue

        sufficient_quantity = True
        ing_list = []
        for id in ing_ids:
            ingredient = IngredientItem.get_ingredient_by_id(id)
            ing_list.append(ingredient)
        
            sale_quantity = recipe.ing_dict[id]
            if ingredient.quantity < sale_quantity:
                sufficient_quantity = False

        if sufficient_quantity:
            for ingredient in ing_list:
                ingredient.quantity -= float(recipe.ing_dict[ingredient.ing_id])
                ingredient.save()
        else:
            all_recipes_saved = False
            error_recipes.append(recipe_id)

    if all_recipes_saved:
        return jsonify(code=200, msg="Success")
    elif len(error_recipes)>0:
        return jsonify(code=500, msg=f"Error saving some results due to insufficient inventory. Unable to sell recipes: {error_recipes} " + error_msg)
    else:
        return jsonify(code=400, msg=f"Error saving some results due to poor request. Please check inventory and try again if needed. " + error_msg)


@app.route("/take_stock/", methods=["POST"])
def take_stock():

    request_data = request.get_json()

    all_items_saved = True
    error_ids = []
    for key, value in request_data.items():
        try:
            ingredient = IngredientItem.get_ingredient_by_id(key)
            ingredient.quantity = value
            ingredient.save()
        
        except AttributeError:
            all_items_saved = False
            error_ids.append(key)
        
    if all_items_saved:
        return jsonify(code=200, msg="Success")
    else:
        return jsonify(code=400, msg=f"Error saving some results. Please refer to inventory IDs and try again if needed. Invalid Ids: {error_ids}")



@app.route("/generate_report/")
def generate_report():
    return jsonify(
        event = "generate_report"
    )

