# code_challenge

## Introduction

This repo contains code for a command line based inventory management system. It features a server (which uses flask endpoints to update records, generate reports or list data) and a client (a simple command line app to interact with the endpoints).


## Installation & Running the App

* Please clone the repo. All commands in this README are run at the repo level and not within subfolders.

* To load the project requirements, I recommend using venv. This project was built using Python 3.6.5. The project requirements are found in requirements.txt and can be loaded when inside of the environment using:

    pip install -r requirements.txt

* The app uses an SQLite database initialised based on the location of the restaurant. In order to create this database and populate the necessary tables, please use the init_app.py file. To do so, run the command below and follow the prompt to input the location_id of the restaurant. If you do not know the desired location id, a csv of all locations can be found in server/csvs/locations.csv. If you do not mind which location, you can enter 1.

    python server/init_app.py 

* I recommend opening two terminal windows, one for the server, and one for the client. To run the server please use the following command:

    FLASK_APP=server/main flask run

To run the client, please run:

    python client/main.py 

* To verify the app is functioning correctly, the option to view specific tables has been included within the app (eg. events, ingredients). Alternatively you may start up an interactive sqlite session where you can query the tables directly using the command:

    sqlite3 



## Design Choices & Priorities

# Command Line Application

* The decision to create a command line application instead of using a browser as outlined in the challenge was largely due to my lack of experience with front end development as a machine learning engineer. I felt that time spent on ramping up on this would detract from the time I could spend implementing the back end logic for the inventory management itself. A command line app was suggested in my initial call with nory as an option, and I decided to try it out for this reason. This decision has some knock on effects in terms of the requirements. 
* This command line app works locally, on one machine only (a computer/laptop), as opposed to the mobile browser approach outlined in the challenge which would allow for multiple users on different devices. I did however set up my app in a server/client style with this in mind as a future requirement, using flask endpoints to showcase how the server side may be accessed by a more fleshed out front end. As only one user would be using the client at any one time in my current implementation, I didn't implement any threading/locking but that is something that could be included also for future iterations.
* The user experience of using a command line app would not be suitable for restaurant staff who may be non technical. It also wouldn't be suitable for the pace of a restaurant. Therefore the client side of this app is primarily to demonstrate the functionality of the back end. The lack of a UI means that data entry in this app relies on correctly typing values. For this reason I have chosen for the user to input ids rather than names for their desired inventory entry, with the option to list all ingredients, recipes etc to lookup ids if needed.

# Business Requirement Prioritisation

* My main priorities were the inventory management events (accepting deliveries, taking stock, selling items) as well as some basic reporting in the form of an event log table that can be viewed and a summary generated as outlined in the challenge.
* Given the time restrictions of the challenge, I chose to deprioritise the capability of recording staff. The app does not identify users in any way, nor does it record who is responsible for which events. Seeing which staff members were responsible for which actions or restricting actions to certain job roles seemed less business critical to me than the management of the inventory itself or the insights gained from the reporting on that. Furthermore, user authentication seemed like it would better fit a solution that had multiple devices as opposed to my implementation where there is only one app per location.
* I chose to sacrifice some system accuracy by ignoring recipe modifiers in my app. This choice was in part to simplify the workflow for the time restricted nature of the challenge, but in truth it was largely driven by the lack of quantity information available for the modifiers themselves. With no quantity attached to a 'modifier' portion, attempts to incorporate those into the inventory management would be inaccurate. This additional ingredient usage would currently be reflected under the 'take stock' action and so may sway the waste calculations.
* The summaries provided by the 'generate report' action are not time bound to a month, instead they are based on totals. The month requirement here was deprioritised, as the impact of this would not be felt for at least a month, in which time the logic could be added.
* The waste calculation in the report generation is based only on negative changes in inventory quantity and is not offset by positive ones as that is my understanding of how waste would be recorded given the description.

# Coding Practice Prioritisation

* My main priority here was to create an app that would cover a good amount of the back end logic for the business requirements, while being designed in a way that would be extensible in future, hence my use of flask. 
* Given the time restrictions, a number of things were deprioritised here. More robust error handling and edge case detection would be needed, as well as more data type verification where necessary. The code contains some duplication which would be better if reworked into more modular reusable code. I also did not have time to include tests, which would be highly important to have here.

## Data Comments

* The data provided for the code challenge has been modified slightly before being included to populate the database. Staff details relating to their pay, such as IBAN and BIC, are considered PII and are high risk. As this is an application focused on inventory management and not on staff pay, there is no need to include such data here.
* The lack of units for cost or price columns is an issue. A currency should be included where possible.
* As an ML Engineer the data itself is always something I look at but I imagine here a lot of the data was dummy data for the sake of the challenge. For example, all quantities being measured in volume (litres, millileters etc) does not always make sense for varying ingredients such as lettuce. A measurement of mass (grams etc) would probably be more meaningful. The quantities and pricing in general seemed off, probably due to being dummy data, but it was a change for me since I am used to working closely with real world data examples, so I found myself double checking results. I also wondered at the use of a single price for each ingredient. I imagine this was for simplifications sake for the challenge as in real world usage perhaps there would be variance in suppliers/transport cost etc based on location.