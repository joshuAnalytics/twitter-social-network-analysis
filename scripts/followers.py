# ----------------- sample script to retrieve follower data -----------------

import joblib
import pandas as pd
import tweepy as tp
import secrets as s
from twitter_sna import collector, api_init

handle_list = [
    # "@twitter_handle_1",
    # "@twitter_handle_2",
]

auth = tp.OAuthHandler(s.api_key, s.api_secret_key)
auth.set_access_token(s.access_token, s.access_token_secret)
api = tp.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
dc = collector.DataCollector(api)

dc.add_users(handle_list)

for handle in handle_list:
    dc.get_followers(handle)
