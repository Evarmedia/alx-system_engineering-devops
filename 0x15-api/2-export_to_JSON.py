#!/usr/bin/python3
"""Exports to-do list from api for a given employee ID to JSON format."""
import json
import requests
import sys

if __name__ == "__main__":
    employee_id = sys.argv[1]
    api_url = "https://jsonplaceholder.typicode.com/"
    user = requests.get(api_url + "users/{}".format(employee_id)).json()
    employee_username = user.get("username")
    todos = requests.get(api_url + "todos", params={"userId": employee_id}).json()

    with open("{}.json".format(employee_id), "w") as jsonfile:
        json.dump({employee_id: [{
                "task": t.get("title"),
                "completed": t.get("completed"),
                "username": employee_username
            } for t in todos]}, jsonfile)
