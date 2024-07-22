import requests
import json
import pandas as pd

pd.set_option("max_columns", None) 
pd.set_option("max_colwidth", None) 
pd.set_option("max_rows", None) 

def main():

    stay_in_app=True
    home_menu = ("\n----------------- Welcome to the Inventory Management System! -----------------\n"
                    "Please select your action from the list below by entering the corresponding number:\n\n"
                    "\t------ACTIONS------\n\n"
                    "\t1. Accept delivery\n"
                    "\t2. Sell item\n"
                    "\t3. Take stock\n"
                    "\t4. Generate report\n\n"
                    "\t--------VIEW--------\n\n"
                    "\t5. List event log\n"
                    "\t6. List all inventory\n"
                    "\t7. List all recipes\n\n"
                    "\t-------CONTROL-------\n\n"
                    "\tEnter any other key to QUIT\n\n"
    )
    
    while stay_in_app:
        print(home_menu)

        try:
            home_input = int(input())
            if not(home_input > 0 and home_input <8):
                break
        except ValueError:
            break

        selected_function = select_home_function(home_input)
        selected_function()

        print('\n\nWould you like to perform another action? (y/n)')
        navigation_input = (input())
        if (navigation_input == 'n'):
            stay_in_app=False


### List API calls    

def list_all_inventory():
    response_object = requests.get("http://127.0.0.1:5000/list_inventory/all")
    inventory_df = pd.read_json(response_object.text, precise_float=True)[['name', 'ingredient_id', 'quantity', 'unit']]
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
    event_df = pd.read_json(response_object.text, precise_float=True)[['timestamp', 'event', 'ingredient_id', 'change', 'recipe_id', 'staff_id']]
    print(event_df.sort_values('timestamp').to_string(index=False))


### Event API calls

def accept_delivery():

    print("\nPlease enter the ingredient id of the delivery item you wish to update, followed by an equals")
    print("sign to indicate the quantity you are adding. Then hit ENTER. You may enter multiple items by typing an entry per line.")
    print("Hit enter once more on an empty line to submit your items.")
    print("\n id=quantity  eg. 77=6.5 \n\n")

    stock_dictionary = accept_input_dict()
    response_object = requests.post("http://127.0.0.1:5000/accept_delivery", json=stock_dictionary)
    print(response_object.json())

def sell_item():

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
    
    json_recipes = json.dumps(input_list)
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


### Misc funcs
    
def select_home_function(i):
    switcher = {
            1: lambda: accept_delivery,
            2: lambda: sell_item,
            3: lambda: take_stock,
            4: lambda: generate_report,
            5: lambda: list_all_events,
            6: lambda: list_all_inventory,
            7: lambda: list_all_recipes,
    }
    func = switcher.get(i, lambda: 'Invalid Choice')
    return func()

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
