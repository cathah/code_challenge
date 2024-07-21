import requests
import json
import pandas as pd

pd.set_option("max_columns", None) 
pd.set_option("max_colwidth", None) 
pd.set_option("max_rows", None) 

def main():

    print("Hello! This is the client!")


    home_menu = '''
------- Welcome to the Inventory Management System! -------
Please select your action from the list below by entering the corresponding number:
1. Hello World
2. List all inventory
3. List inventory by ingredient ID
4. List inventory by ingredient name
5. List event log
6. Accept delivery
7. Sell item
8. Take stock
9. Generate report
'''


    print(home_menu)

    home_input = int(input())
    selected_function = select_home_function(home_input)
    selected_function()



def select_home_function(i):
    switcher = {
            1: lambda: hello_world,
            2: lambda: list_all_inventory,
            3: lambda: list_inventory_by_id,
            4: lambda: list_inventory_by_name,
            5: lambda: list_all_events,
            6: lambda: accept_delivery,
            7: lambda: sell_item,
            8: lambda: take_stock,
            9: lambda: generate_report
    }
    func = switcher.get(i, lambda: 'Invalid Choice')
    return func()





def hello_world():
    print('Hello World!')
    response_object = requests.get("http://127.0.0.1:5000/")
    print(response_object.json())

def list_all_inventory():
    response_object = requests.get("http://127.0.0.1:5000/list_inventory/all")
    inventory_df = pd.read_json(response_object.text)[['name', 'ingredient_id', 'quantity', 'unit']]
    print(inventory_df.sort_values('name').to_string(index=False))

def list_inventory_by_id():

    print('Please enter the ingredient ID: ')
    ing_id = input()
    response_object = requests.get(f"http://127.0.0.1:5000/list_inventory/{ing_id}")
    inventory_df = pd.DataFrame(json.loads(response_object.text), index=[0])[['name', 'ingredient_id', 'quantity', 'unit']]
    print(inventory_df.to_string(index=False))

def list_inventory_by_name():

    print('Please enter the ingredient name: ')
    ing_name = input()
    response_object = requests.get(f"http://127.0.0.1:5000/list_inventory/name/{ing_name}")
    inventory_df = pd.DataFrame(json.loads(response_object.text), index=[0])[['name', 'ingredient_id', 'quantity', 'unit']]
    print(inventory_df.to_string(index=False))








def list_all_events():
    response_object = requests.get("http://127.0.0.1:5000/list_events/all")
    print(response_object.json())

def accept_delivery():
    response_object = requests.get("http://127.0.0.1:5000/accept_delivery")
    print(response_object.json())

def sell_item():
    response_object = requests.get("http://127.0.0.1:5000/sell_item")
    print(response_object.json())

def take_stock():
    response_object = requests.get("http://127.0.0.1:5000/take_stock")
    print(response_object.json())

def generate_report():
    response_object = requests.get("http://127.0.0.1:5000/generate_report")
    print(response_object.json())



if __name__ == "__main__":
    main()
