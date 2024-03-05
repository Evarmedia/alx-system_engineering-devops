#!/usr/bin/python3

import praw

def recurse(subreddit, hot_list=[], last_post=None, count=10):
    reddit = praw.Reddit(client_id='your_client_id',
                         client_secret='your_client_secret',
                         user_agent='your_user_agent')

    try:
        current_subreddit = reddit.subreddit(subreddit)
        new_posts = current_subreddit.hot(limit=count, params={"after": last_post})
        new_hot_list = [post.title for post in new_posts]
        hot_list.extend(new_hot_list)

        if len(new_hot_list) == 0:
            if len(hot_list) == 0:
                return None
            else:
                return hot_list
        else:
            last_post = new_hot_list[-1]
            return recurse(subreddit, hot_list, last_post, count)
    except prawcore.exceptions.Redirect:
        return None
