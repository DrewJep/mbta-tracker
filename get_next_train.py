import requests
import json
import os
from datetime import datetime

mbta_key = os.getenv("mbta_key")

HEADERS = {
    "x-api-key": mbta_key
}

def clean_timestamp(timestamp):
    if timestamp is None:
        return None
    dt = datetime.fromisoformat(timestamp)
    pretty = dt.strftime("%B %d, %Y at %I:%M %p")
    return pretty

def get_next_train(stop_id):
    url = f"https://api-v3.mbta.com/predictions?filter[stop]={stop_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            next_train = data['data'][0]
            departure_time = next_train['attributes']['departure_time']
            return clean_timestamp(departure_time)
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def get_stop_info(stop_id):
    url = f"https://api-v3.mbta.com/stops/{stop_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data']:
            stop_info = data['data']
            return stop_info
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def get_stop_ids():
    lines = ["Red", "Orange", "Blue", "Green-B", "Green-C", "Green-D", "Green-E"]
    user_line = input("Enter the line (Red, Orange, Blue, Green-B, Green-C, Green-D, Green-E): ")
    if user_line not in lines:
        print("Invalid line. Please enter a valid line.")
        return None
    url = f"https://api-v3.mbta.com/stops?filter[route]={user_line}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        stop_ids = [stop['id'] for stop in data['data']]
        stop_names = [stop['attributes']['name'] for stop in data['data']]
        return dict(zip(stop_ids, stop_names))
    else:
        print(f"Error: {response.status_code}")
        return None 

def main():
    run = True
    while run:
        user_input = input("what would you like to do? (1: Get next train, 2: Get stop IDs, 3: Exit): ")
        if user_input == "1":
            stop_id = input("Enter the stop ID: ")
            stop_info = get_stop_info(stop_id)
            if stop_info:
                print(stop_info['attributes']['name'])
            next_train_time = get_next_train(stop_id)
            if next_train_time:
                print(f"The next train departs at: {next_train_time}")
            else:
                print("No upcoming trains found for this stop.")
        elif user_input == "2":
            stop_ids = get_stop_ids()
            if stop_ids:
                print("Stop IDs: Stop Names")
                for stop_id, stop_name in stop_ids.items():
                    print(f"{stop_id}: {stop_name}")
        elif user_input == "3":
            run = False
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
