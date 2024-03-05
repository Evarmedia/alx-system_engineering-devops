#!/usr/bin/python3

import praw
import re

def count_words(subreddit, word_list, titles=None):
    if titles is None:
        titles = []

    reddit = praw.Reddit(client_id='your_client_id',
                     client_secret='your_client_secret',
                     user_agent='your_user_agent')

    try:
        current_subreddit = reddit.subreddit(subreddit)
        new_posts = current_subreddit.hot(limit=10)

        for post in new_posts:
            titles.append(post.title.lower())

        if len(titles) > 0:
            word_count = {word: sum(re.findall(r'\b' + re.escape(word) + r'\b', ' '.join(titles).lower()).count(word.lower()) for word in word_list)}

            sorted_word_count = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))

            for word, count in sorted_word_count:
                if count > 0:
                    print(f'{word.lower()}: {count}')
        else:
            print("No posts match the given subreddit.")
    except praw.exceptions.Redirect:
        print("Subreddit is invalid.")
