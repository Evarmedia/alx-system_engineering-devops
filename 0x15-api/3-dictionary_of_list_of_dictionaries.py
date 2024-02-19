#!/usr/bin/python3
"""Exports to-do list from api of all employees to JSON format."""
import json
import requests

if __name__ == "__main__":
    api_url = "https://jsonplaceholder.typicode.com/"
    users = requests.get(api_url + "users").json()

    with open("todo_all_employees.json", "w") as jsonfile:
        json.dump({
            u.get("id"): [{
                "username": u.get("username"),
                "task": t.get("title"),
                "completed": t.get("completed"),
            } for t in requests.get(api_url + "todos",
                                    params={"userId": u.get("id")}).json()]
            for u in users}, jsonfile)
