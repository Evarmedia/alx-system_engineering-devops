#!/usr/bin/python3

import requests
import re


def fetch_titles(subreddit, after='', word_counts={}, word_list=[]):
    # Base URL for fetching hot articles from a subreddit
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25&after={after}"
    headers = {'User-Agent': 'reddit-wordcount/0.1'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        # If the subreddit does not exist or other error, conclude the recursion
        return None

    data = response.json()
    if 'data' in data:
        for post in data['data']['children']:
            title = post['data']['title'].lower()
            for word in word_list:
                if word.lower() in word_counts:
                    occurrences = len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', title))
                    word_counts[word.lower()] += occurrences
                else:
                    word_counts[word.lower()] = len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', title))

        after = data['data']['after']
        if after is None:
            # If there's no more data to fetch, we're at the end
            return word_counts
        else:
            # Recurse to get more data
            return fetch_titles(subreddit, after, word_counts, word_list)
    else:
        # If the response doesn't contain post data, conclude the recursion
        return None

def count_words(subreddit, word_list):
    # Initialize word_counts dict
    word_counts = {word.lower(): 0 for word in word_list}
    word_counts = fetch_titles(subreddit, '', word_counts, word_list)
    
    if not word_counts:
        print("No posts match or the subreddit is invalid.")
        return
    
    # Filter out words with 0 occurrences and sort
    filtered_counts = {word: count for word, count in word_counts.items() if count > 0}
    sorted_counts = sorted(filtered_counts.items(), key=lambda x: (-x[1], x[0]))
    
    for word, count in sorted_counts:
        print(f"{word}: {count}")
