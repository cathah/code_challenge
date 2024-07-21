from flask import Flask, jsonify

from server.models.ingredient_item import IngredientItem


app = Flask(__name__)

def main():
    print("Hello, this is the server! To activate, please run the following command: ")
    print("FLASK_APP=server/main flask run")


@app.route("/")
def index():
    return jsonify(
        hello = "World!!"
    )

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
    

@app.route("/list_events/all")
def get_all_events():
    return jsonify(
        get = "all events"
    )

@app.route("/accept_delivery/")
def accept_delivery():
    return jsonify(
        event = "accept delivery"
    )

@app.route("/sell_item/")
def sell_item():
    return jsonify(
        event = "sell item"
    )

@app.route("/take_stock/")
def take_stock():

    return jsonify(
        event = "take_stock"
    )

@app.route("/generate_report/")
def generate_report():
    return jsonify(
        event = "generate_report"
    )

