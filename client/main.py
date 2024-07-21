import requests

def main():

    print("Hello! This is the client!")


    home_menu = '''
------- Welcome to the Inventory Management System! -------
Please select your action from the list below by entering the corresponding number:
1. Hello World
2. List all inventory
3. List inventory by ID
4. List event log
5. Accept delivery
6. Sell item
7. Take stock
8. Generate report
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
            4: lambda: list_all_events,
            5: lambda: accept_delivery,
            6: lambda: sell_item,
            7: lambda: take_stock,
            8: lambda: generate_report,

    }
    func = switcher.get(i, lambda: 'Invalid Choice')
    return func()





def hello_world():
    print('Hello World!')
    response_object = requests.get("http://127.0.0.1:5000/")
    print(response_object.json())

def list_all_inventory():
    response_object = requests.get("http://127.0.0.1:5000/list_inventory/all")
    print(response_object.json())

def list_inventory_by_id():
    response_object = requests.get("http://127.0.0.1:5000/list_inventory/<ing_id>")
    print(response_object.json())

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
