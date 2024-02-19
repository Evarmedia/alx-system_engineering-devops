#!/usr/bin/python3
"""Exports to-do list information for a given employee ID to CSV format."""
import csv
import requests
import sys

if __name__ == "__main__":
    employee_id = sys.argv[1]
    api_url = "https://jsonplaceholder.typicode.com/"
    get_user = requests.get(api_url + "users/{}".format(employee_id)).json()
    employee_username = get_user.get("username")
    todos = requests.get(api_url + "todos",
                         params={"userId": employee_id}).json()

    with open("{}.csv".format(employee_id), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        [writer.writerow(
            [employee_id, employee_username,
             t.get("completed"),
             t.get("title")]
         ) for t in todos]
