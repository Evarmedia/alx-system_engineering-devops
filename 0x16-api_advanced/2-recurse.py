#!/usr/bin/python3
""" recursive function that queries the Reddit API """
import requests
import sys
after = None


def recurse(subreddit, hot_list=[]):
    """     Args:
        subreddit: subreddit name
        hot_list: list of hot titles in subreddit
        after: last hot_item appended to hot_list
    Returns:
        a list containing the titles of all hot articles for the subreddit
        or None if queried subreddit is invalid """
    global after
    headers = {'User-Agent': 'mishakmosi'}
    get_url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params1 = {'after': after}
    fin_res = requests.get(
        get_url,
        headers=headers,
        allow_redirects=False,
        params=params1)

    if fin_res.status_code == 200:
        next_ = fin_res.json().get('data').get('after')
        if next_ is not None:
            after = next_
            recurse(subreddit, hot_list)
        list_titles = fin_res.json().get('data').get('children')
        for title_ in list_titles:
            hot_list.append(title_.get('data').get('title'))
        return hot_list
    else:
        return (None)
