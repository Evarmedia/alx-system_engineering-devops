#!/usr/bin/python3

import requests


def top_ten(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)

    '''Check if the subreddit exists by ensuring
    a successful status code and data length'''
    if response.status_code == 200 and 'data' in response.json():
        data = response.json()['data']['children']

        if not data:
            print(None)
            return

        for post in data:
            print(post['data']['title'])
    else:
        print(None)
