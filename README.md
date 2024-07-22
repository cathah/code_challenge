# code_challenge

## Introduction

This repo contains code for a command line based inventory management system. It features a Flask server (with endpoints to update records, generate reports or list data) and a client (a simple command line app to interact with the endpoints).


## Installation & Running the App

* Please clone the repo. All commands in this README are run at the repo level and not within subfolders. If you are having issues with resolving paths/modules, you may update your pythonpath for the session using:

```sh
    export PYTHONPATH=.
```

* To load the project requirements, I recommend using venv. This project was built using Python 3.6.5. The project requirements are found in requirements.txt and can be loaded when inside of the environment. The file requirements_exact has also been included to show my exact libraries.

```sh
    python3 -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt (alternatively: python -m pip install -r requirements.txt)
```

* The app uses an SQLite database initialised based on the location of the restaurant. In order to create this database and populate the necessary tables, please use the init_app.py file. To do so, run the command below and follow the prompt to input the location_id of the restaurant. If you do not know the desired location id, a csv of all locations can be found in server/csvs/locations.csv. If you do not mind which location, you can enter 1.

```sh
    python server/init_app.py 
```
    

* I recommend opening two terminal windows, one for the server, and one for the client. To run the server please use the following command:

```sh
    FLASK_APP=server/main flask run
```
     
* To run the client, please run:

```sh
    python client/main.py 
```
    
* To verify the app is functioning correctly, the option to view specific tables has been included within the app through listing (eg. events, ingredients). Alternatively you may start up an interactive sqlite session where you can query the tables directly using the command:
```sh
    sqlite3
```

* Below you'll find some sample stock updates you may perform to help you test the app. These specific commands only work by choosing **location 1** when initialising your db.

```sh
    ACCEPT DELIVERY 
    (bulk updates quantity to 50 for all ingredients)

    121=50
    178=50
    223=50
    66=50
    415=50
    281=50
    278=50
    139=50
    6=50
    298=50
    81=50
    163=50
    159=50
    33=50
    167=50
    335=50
    181=50
    405=50
    395=50
    222=50
    338=50
    154=50
    447=50
    26=50
    352=50
    472=50
    221=50
    92=50
    80=50
    208=50
    315=50
    279=50
    245=50
    218=50
    465=50
    355=50
    267=50
    219=50
    17=50
    134=50
    380=50
    122=50
    11=50
    323=50
    172=50
    373=50
    319=50
    105=50
    15=50
    251=50
    310=50
    318=50
    348=50
    391=50
    416=50
    273=50
    336=50
    299=50
    236=50
    432=50
    185=50
    93=50
    64=50
    293=50
    442=50
    399=50
    343=50
    166=50
    413=50
    311=50
    268=50
    471=50
    116=50
    351=50
    291=50
    51=50
    317=50
    438=50
    322=50
    263=50
    190=50
    94=50
    232=50
    234=50
    4=50
    197=50
    108=50
    231=50
    115=50
    119=50
    452=50
    449=50
    464=50
    129=50
    182=50
    131=50
    204=50
    385=50
    426=50
    120=50
    113=50
    126=50
    347=50
    460=50
    82=50
    409=50
    99=50
    393=50
    76=50
    312=50
    60=50
    53=50
    250=50
    50=50
    203=50
    455=50
    233=50
    228=50
    79=50
    25=50
    175=50
    160=50
    407=50
    357=50
    463=50
    429=50
    459=50
    262=50
    240=50
    244=50
    437=50
    77=50
    436=50
    23=50
    266=50
    246=50
    308=50
    114=50
    332=50
    387=50
    434=50
    192=50
    320=50
    372=50
```

```sh
    TAKE STOCK
    (Allows us to record waste & have too few items to sell recipe later)  

    15=2
```

```sh
    SELL ITEM 
    (17 should fail due to lack of inventory 15 
    18 should succeed and decrement ingredients 6, 11, 108, 434)

    17 
    18
```


## Design Choices & Priorities

### Command Line Application

* The decision to create a command line application instead of using a browser as outlined in the challenge was largely due to my lack of experience with front end development as a machine learning engineer. I felt that time spent on ramping up on this would detract from the time I could spend implementing the back end logic for the inventory management itself. A command line app was suggested in my initial call with nory as an option, and I decided to try it out for this reason. This decision has some knock on effects in terms of the requirements. 
* This command line app works locally, on one machine only (a computer/laptop), as opposed to the mobile browser approach outlined in the challenge which would allow for multiple users on different devices. I did however set up my app in a server/client style with this in mind as a future requirement, using flask endpoints to showcase how the server side may be accessed by a more fleshed out front end. As only one user would be using the client at any one time in my current implementation, I didn't implement any threading/locking but that is something that could be included also for future iterations.
* The user experience of using a command line app would not be suitable for restaurant staff who may be non technical. It also wouldn't be suitable for the pace of a restaurant. Therefore the client side of this app is primarily to demonstrate the functionality of the back end. The lack of a UI means that data entry in this app relies on correctly typing values. For this reason I have chosen for the user to input ids rather than names for their desired inventory entry, with the option to list all ingredients, recipes etc to lookup ids if needed.

### Business Requirement Prioritisation

* My main priorities were the inventory management events (accepting deliveries, taking stock, selling items) as well as some basic reporting in the form of an event log table that can be viewed and a summary generated as outlined in the challenge.
* Given the time restrictions of the challenge, I chose to deprioritise the capability of recording staff. The app does not identify users in any way, nor does it record who is responsible for which events. Seeing which staff members were responsible for which actions or restricting actions to certain job roles seemed less business critical to me than the management of the inventory itself or the insights gained from the reporting on that. Furthermore, user authentication seemed like it would better fit a solution that had multiple devices as opposed to my implementation where there is only one app per location.
* I chose to sacrifice some system accuracy by ignoring recipe modifiers in my app. This choice was in part to simplify the workflow for the time restricted nature of the challenge, but in truth it was largely driven by the lack of quantity information available for the modifiers themselves. With no quantity attached to a 'modifier' portion, attempts to incorporate those into the inventory management would be inaccurate. This additional ingredient usage would currently be reflected under the 'take stock' action and so may sway the waste calculations.
* The summaries provided by the 'generate report' action are not time bound to a month, instead they are based on totals. The month requirement here was deprioritised, as the impact of this would not be felt for at least a month, in which time the logic could be added.
* The waste calculation in the report generation is based only on negative changes in inventory quantity and is not offset by positive ones as that is my understanding of how waste would be recorded given the description.

### Coding Practice Prioritisation

* My main priority here was to create an app that would cover a good amount of the back end logic for the business requirements, while being designed in a way that would be extensible in future, hence my use of flask. 
* Given the time restrictions, a number of things were deprioritised here. More robust error handling and edge case detection would be needed, as well as more data type verification where necessary. The code contains some duplication which would be better if reworked into more modular reusable code. I also did not have time to include tests, which would be highly important to have here.

### Data Comments

* The data provided for the code challenge has been modified slightly before being included to populate the database. Staff details relating to their pay, such as IBAN and BIC, are considered PII and are high risk. As this is an application focused on inventory management and not on staff pay, there is no need to include such data here.
* The lack of units for cost or price columns is an issue. A currency should be included where possible.
* As an ML Engineer the data itself is always something I look at but I imagine here a lot of the data was dummy data for the sake of the challenge. For example, all quantities being measured in volume (litres, millileters etc) does not always make sense for varying ingredients such as lettuce. A measurement of mass (grams etc) would probably be more meaningful. The quantities and pricing in general seemed off, probably due to being dummy data, but it was a change for me since I am used to working closely with real world data examples, so I found myself double checking results. I also wondered at the use of a single price for each ingredient. I imagine this was for simplifications sake for the challenge as in real world usage perhaps there would be variance in suppliers/transport cost etc based on location.