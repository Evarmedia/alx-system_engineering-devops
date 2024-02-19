#!/usr/bin/python3
"""Returns to-do list information for a given employee ID{param}."""
import requests
import sys

if __name__ == "__main__":
    api_url = "https://jsonplaceholder.typicode.com/"
    employee_name = requests.get(api_url + "users/{}".format(sys.argv[1])).json()
    todo_list = requests.get(api_url + "todo_list", params={"userId": sys.argv[1]}).json()

    completed = [t.get("title") for t in todo_list if t.get("completed") is True]
    print("Employee {} is done with tasks({}/{}):".format(
        employee_name.get("name"), len(completed), len(todo_list)))
    [print("\t {}".format(c)) for c in completed]
