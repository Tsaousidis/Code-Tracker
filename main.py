
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file (USER_TOKEN, MY_USERNAME)
load_dotenv()

# Environment and API configuration
USER_TOKEN = os.getenv("USER_TOKEN")
MY_USERNAME = os.getenv("MY_USERNAME")
USERS_ENDPOINT = "https://pixe.la/v1/users"
GRAPH_ID = "itscodingtime"
GRAPH_ENDPOINT = f"{USERS_ENDPOINT}/{MY_USERNAME}/graphs"
UPDATE_GRAPH_ENDPOINT = f"{USERS_ENDPOINT}/{MY_USERNAME}/graphs/{GRAPH_ID}"
HEADERS = {'X-USER-TOKEN': USER_TOKEN}

def main():
    """Entry point and: creates user/graph if necessary and prompts user for an action."""
    ensure_user_exists()
    ensure_graph_exists()

    while True:
        try:
            # Ask the user whether to add or delete today's entry
            action = input("Do you want to [a]dd or [d]elete today's entry? ").strip().lower()

            if action == "a":
                study_time = get_study_time()
                add_time(study_time)
                break  # Exit loop after successful add
            elif action == "d":
                delete_today_entry()
                break  # Exit loop after successful delete
            else:
                print("Invalid option. Please type 'a' or 'd'.")
        except Exception as e:
            print(f"An error occurred: {e}")

def ensure_user_exists():
    """Creates a user only if it doesn't exist."""
    try:
        user_params = {
            "token": USER_TOKEN,
            "username": MY_USERNAME,
            "agreeTermsOfService": "yes",
            "notMinor": "yes",
        }    

        response = requests.post(url=USERS_ENDPOINT, json=user_params)
        
        if response.status_code == 200:
            print("User created successfully.")
        elif response.status_code == 409 and "already exist" in response.text:
            print("User already exists. Skipping creation.")
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to create user: {e}")

def ensure_graph_exists():
    """Creates a graph only if it doesn't exist."""
    try:
        graph_config = {
            "id": GRAPH_ID,
            "name": "Coding Graph",
            "unit": "min",
            "type": "int",
            "color": "ajisai"    
        }   

        response = requests.post(url=GRAPH_ENDPOINT, json=graph_config, headers=HEADERS)
        
        if response.status_code == 200:
            print("Graph created successfully.")
        elif response.status_code == 409 and "already exist" in response.text:
            print("Graph already exists. Skipping creation.")
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to create graph: {e}") 

def get_study_time():
    """Prompts the user to enter valid study time in minutes."""
    while True:
        try:
            return int(input("How many minutes did you study code today? "))
        except ValueError:
            print("Please enter a valid number.")

def add_time(minutes):
    """Adds coding time to Pixela graph."""
    today = datetime.now().strftime("%Y%m%d")
    try:
        pixel_data = {
            "date": today,
            "quantity": str(minutes),
        }

        response = requests.post(url=UPDATE_GRAPH_ENDPOINT, json=pixel_data, headers=HEADERS)
        
        if response.status_code == 200:
            print(f"Successfully logged {minutes} minutes.")
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to log time: {e}")

def delete_today_entry():
    """Deletes today's log in case of a mistake."""
    today = datetime.now().strftime("%Y%m%d")
    delete_endpoint = f"{UPDATE_GRAPH_ENDPOINT}/{today}"
    
    try:
        response = requests.delete(url=delete_endpoint, headers=HEADERS)
        if response.status_code == 200:
            print("✅ Today's entry deleted successfully.")
        elif response.status_code == 404:
            print("⚠️ No entry found for today.")
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to delete today's entry: {e}")


if __name__ == "__main__":
    main()

