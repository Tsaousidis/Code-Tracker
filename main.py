
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

USER_TOKEN = os.getenv("USER_TOKEN")
MY_USERNAME = os.getenv("MY_USERNAME")
USERS_ENDPOINT = "https://pixe.la/v1/users"
GRAPH_ID = "itscodingtime"
GRAPH_ENDPOINT = f"{USERS_ENDPOINT}/{MY_USERNAME}/graphs"
UPDATE_GRAPH_ENDPOINT = f"{USERS_ENDPOINT}/{MY_USERNAME}/graphs/{GRAPH_ID}"
HEADERS = {'X-USER-TOKEN': USER_TOKEN}

def main():
    create_user()
    create_graph()

    study_time = int(input("How many minutes did you study code today?"))
    add_time(study_time)

def create_user():
    user_params = {
        "token": USER_TOKEN,
        "username": MY_USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }    

    response = requests.post(url=USERS_ENDPOINT, json=user_params)
    response.raise_for_status()

def create_graph():
    graph_config = {
        "id": GRAPH_ID,
        "name": "Coding Graph",
        "unit": "min",
        "type": "int",
        "color": "ajisai"    
    }   

    response = requests.post(url=GRAPH_ENDPOINT, json=graph_config, headers=HEADERS)
    response.raise_for_status()

def add_time(minutes):
    today = datetime.now().strftime("%Y%m%d")

    pixel_data = {
        "date": today,
        "quantity": str(minutes),
    }

    response = requests.post(url=UPDATE_GRAPH_ENDPOINT, json=pixel_data, headers=HEADERS)
    response.raise_for_status()

if __name__ == "__main__":
    main()

# Task1 -> Add update function
#response = requests.put(url=UPDATE_GRAPH_ENDPOINT, json=new_pixel_data, headers=headers)
#print(response.text)

# Task2 -> Add delete function
#response = requests.delete(url=UPDATE_GRAPH_ENDPOINT, headers=headers)
#print(response.text)

# Task3 -> Check for existing user and graph

# Task4 -> Add try-except in most of the rais_for_status() and improve input handling

# Task5 -> Add comments to the code

# Task5 -> Create a README file