#!/usr/bin/python3

import requests


def recurse(subreddit, hot_list=[], after=None):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Chrome/88.0.4324.182 Safari/537.36"}
    params = {"limit": 100, "after": after}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    children = data.get("data", {}).get("children", [])
    if not children:
        return hot_list
    
    for child in children:
        title = child.get("data", {}).get("title")
        if title:
            hot_list.append(title)
    
    after = data.get("data", {}).get("after")
    if after:
        return recurse(subreddit, hot_list, after)
    else:
        return hot_list
    