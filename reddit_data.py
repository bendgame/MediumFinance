import pandas as pd
import dateutil.relativedelta
from datetime import date
import datetime
import yfinance as yf
import numpy as np
import praw
import sqlite3


#return a dataframe for the newest reddit posts
def get_reddit(cid= '', csec= '', uag= '', subreddit='wallstreetbets'):
    reddit = praw.Reddit(client_id= cid, client_secret= csec, user_agent= uag)

    posts = reddit.subreddit(subreddit).new(limit=None)
    #hot_bets = reddit.subreddit('wallstreetbets').hot(limit=1000)

    p = []
    for post in posts:
        p.append([post.title, post.score, post.selftext])
    posts_df = pd.DataFrame(p,columns=['title', 'score', 'post'])
    return posts_df