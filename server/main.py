from flask import Flask, jsonify


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
    return jsonify(
        get = "all inventory"
    )

@app.route("/list_inventory/<ing_id>")
def get_inventory_by_ingredient(ing_id):
    return jsonify(
        get = "inventory by id"
    )

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

