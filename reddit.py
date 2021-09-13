import datetime
import pandas as pd
import praw
import streamlit as st

reddit = praw.Reddit(
    client_id = st.secrets["client_id"],
    client_secret = st.secrets["client_secret"],
    password = st.secrets["password"],
    user_agent = st.secrets["user_agent"],
    username = st.secrets["username"]
)

def get_newest_submissions(search_term=None, limit=10):
    print(f"Fetching top {limit} results..")
    
    subreddit = reddit.subreddit("whatcarshouldIbuy+askmechanics")

    submissions = {
        "created":[],
        "title":[],
        "score": [],
        "num_comments": [],
        "body":[],
        "top_comment": []
        }

    # search for submissions matching the search term
    results = subreddit.search(f'selftext:"{search_term}"', limit=limit)
    
    for submission in results:
        # replace instances of "more comments" in the comment tree
        submission.comments.replace_more(limit=0)

        submissions["created"].append(datetime.datetime.utcfromtimestamp(submission.created).date())
        submissions["title"].append(submission.title)
        submissions["score"].append(submission.score)
        submissions["num_comments"].append(submission.num_comments)
        submissions["body"].append(submission.selftext)
        if len(submission.comments) > 0:
            submissions["top_comment"].append(submission.comments[0].body)
        else:
            submissions["top_comment"].append("")
    
    submissions = pd.DataFrame(submissions)
    
    return submissions

if __name__ == "__main__":
    print(get_newest_submissions("toyota suv", limit=10).head())