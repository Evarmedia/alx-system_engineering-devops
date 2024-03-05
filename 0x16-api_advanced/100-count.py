#!/usr/bin/python3
""" recursive function that queries the Reddit API"""
import requests
import sys
after = None
count_dic = []


def count_words(subreddit, word_list):
    """parses the title of all hot articles, and prints a sorted count of given
    keywords (case-insensitive, delimited by spaces) """
    global after
    global count_dic
    headers = {'User-Agent': 'mishakmosi'}
    get_url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params1 = {'after': after}
    response = requests.get(get_url, headers=headers, allow_redirects=False,
                            params=params1)
