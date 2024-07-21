import requests
import json
import pandas as pd

pd.set_option("max_columns", None) 
pd.set_option("max_colwidth", None) 
pd.set_option("max_rows", None) 

def main():

    print("Hello! This is the client!")


    home_menu = '''
\n
------- Welcome to the Inventory Management System! -------
Please select your action from the list below by entering the corresponding number:
1. Hello World
2. List all inventory
3. List inventory by ingredient ID
4. List inventory by ingredient name
5. List all recipes
6. List recipe by recipe ID
7. List recipe by recipe name
8. List event log
9. Accept delivery
10. Sell item
11. Take stock
12. Generate report
\n\n\n
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
            5: lambda: list_all_recipes,
            6: lambda: list_recipe_by_id,
            7: lambda: list_recipe_by_name,
            8: lambda: list_all_events,
            9: lambda: accept_delivery,
            10: lambda: sell_item,
            11: lambda: take_stock,
            12: lambda: generate_report
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



def list_all_recipes():
    response_object = requests.get("http://127.0.0.1:5000/list_recipes/all")
    recipe_df = pd.read_json(response_object.text, precise_float=True)[['recipe_id', 'name', 'ing_dict']]
    print(recipe_df.sort_values('name').to_string(index=False))

def list_recipe_by_id():

    print('Please enter the recipe ID: ')
    recipe_id = input()
    response_object = requests.get(f"http://127.0.0.1:5000/list_recipes/{recipe_id}")
    recipe_df = pd.DataFrame(json.loads(response_object.text), index=[0])[['recipe_id', 'name', 'ing_dict']]
    print(recipe_df.to_string(index=False))

def list_recipe_by_name():

    print('Please enter the recipe name: ')
    recipe_name = input()
    response_object = requests.get(f"http://127.0.0.1:5000/list_recipes/name/{recipe_name}")
    recipe_df = pd.DataFrame(json.loads(response_object.text), index=[0])[['recipe_id', 'name', 'ing_dict']]
    print(recipe_df.to_string(index=False))





def list_all_events():
    response_object = requests.get("http://127.0.0.1:5000/list_events/all")
    print(response_object.json())









def accept_delivery():

    print("\nPlease enter the ingredient id of the delivery item you wish to update, followed by an equals")
    print("sign to indicate the quantity you are adding. Then hit ENTER. You may enter multiple items by typing an entry per line.")
    print("Hit enter once more on an empty line to submit your items.")
    print("\n id=quantity  eg. 77=6.5 \n\n")

    stock_dictionary = accept_input_dict()
    response_object = requests.post("http://127.0.0.1:5000/accept_delivery", json=stock_dictionary)
    
    print(response_object.json())

def sell_item():
    # response_object = requests.get("http://127.0.0.1:5000/sell_item")
    # print(response_object.json())

    print("\nPlease enter the recipe id of the menu item you wish to sell, then hit ENTER. You may enter multiple items by typing an entry per line.")
    print("Hit enter once more on an empty line to submit your items.")
    print("\n recipe_id  eg. 17 \n\n")

    input_list = []
    while True:
        line = input()
        if line:
            input_list.append(line)
        else:
            break

    print(input_list)
    
    json_recipes = json.dumps(input_list)


    # stock_dictionary = accept_input_dict()
    response_object = requests.post("http://127.0.0.1:5000/sell_item", json=json_recipes)
    
    print(response_object.json())







def take_stock():

    print("\nPlease enter the ingredient id of the item you wish to update, followed by an equals")
    print("sign to indicate the quantity. Then hit ENTER. You may enter multiple items by typing an entry per line.")
    print("Hit enter once more on an empty line to submit your items.")
    print("\n id=quantity  eg. 77=6.5 \n\n")

    stock_dictionary = accept_input_dict()
    response_object = requests.post("http://127.0.0.1:5000/take_stock", json=stock_dictionary)
    
    print(response_object.json())





def generate_report():
    response_object = requests.get("http://127.0.0.1:5000/generate_report")
    print(response_object.json())





def accept_input_dict():

    input_list = []
    while True:
        line = input()
        if line:
            input_list.append(line)
        else:
            break

    input_dictionary = {}
    try:
        for pair in input_list:
            key, value = pair.split("=")
            input_dictionary[key] = value
    except ValueError: 
        print("The values you have entered contain an invalid format. All values have been disregarded after: ")
        print(pair)
        print('Please try again for any values entered after this. Continuing with values before this point...')

    return input_dictionary


if __name__ == "__main__":
    main()
