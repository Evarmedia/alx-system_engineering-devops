import praw
import re

def count_words(subreddit, word_list, after=None, aggregated_counts=None):
    # Initialize Reddit instance
    reddit = praw.Reddit(client_id='your_client_id',
                         client_secret='your_client_secret',
                         user_agent='bot_user_agent')
    
    # Initial call setup
    if aggregated_counts is None:
        aggregated_counts = {word.lower(): 0 for word in word_list}

    # Base case for recursion: No more pages
    if after == "":
        sorted_counts = sorted(aggregated_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        for word, count in sorted_counts:
            if count > 0:
                print(f'{word}: {count}')
        return
    
    # Main logic for fetching and processing posts
    subreddit_instance = reddit.subreddit(subreddit)
    posts = subreddit_instance.hot(limit=100, params={"after": after})
    
    new_after = None
    for post in posts:
        # Processing titles for current page of posts
        title = post.title.lower()
        for word in word_list:
            # Count word occurrences without considering punctuation
            occurrences = len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', title))
            aggregated_counts[word.lower()] += occurrences
        
        new_after = post.fullname
    
    # Recursive call to process next page
    count_words(subreddit, word_list, after=new_after, aggregated_counts=aggregated_counts)

# Example
count_words('python', ['python', 'java', 'c++', 'javascript'])

