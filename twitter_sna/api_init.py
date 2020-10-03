import tweepy as tp
import secrets as s


class ApiInit:
    def __init__(self):
        # initialize the tweepy api
        auth = tp.OAuthHandler(s.api_key, s.api_secret_key)
        auth.set_access_token(s.access_token, s.access_token_secret)
        self.api = tp.API(auth, wait_on_rate_limit=True)
