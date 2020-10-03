import tweepy as tw
import secrets as s
import joblib as jlb
import pandas as pd
from pathlib import Path
import os


class DataCollector:
    def __init__(self, tweepy_api, cache_path="_cache/", cache_file="df_users.jlb"):
        self.api = tweepy_api
        self.user_fields = [
            "id",
            "screen_name",
            "name",
            "description",
            "followers_count",
            "friends_count",
            "favourites_count",
            "statuses_count",
        ]
        self.follower_fields = ["id_str", "name", "screen_name", "followers_count", "friends_count", "created_at"]
        self.cache_path = cache_path
        self.cache_file = cache_file
        self.cache_file_path = Path(cache_path, cache_file)
        if os.path.exists(self.cache_file_path):
            self.df_users = jlb.load(self.cache_file_path)
        else:
            self.create_cache_file()
            self.df_users = jlb.load(self.cache_file_path)

    def add_users(self, handle_list):
        """
        pass a list of user handles to add to dataset
        """
        for handle in handle_list:
            handle = self._fix_handle(handle)
            self.add_user(handle)
        print(f"\ntotal users {self.df_users.shape[0]}")

    def add_user(self, handle):
        """
        add user data to the users dataset
        """
        handle = self._fix_handle(handle)
        if not self.is_handle_cached(handle):
            response = self.api.get_user(handle)
            user_row = self.parse_user_data(response, self.user_fields)
            self.df_users = self.df_users.append(user_row, sort=False)
            jlb.dump(self.df_users, self.cache_file_path)
            print(f"{handle} added")
        else:
            print(f"{handle} already cached")
        pass

    def is_handle_cached(self, handle):
        """
        check if user is already cached
        """
        handle = self._fix_handle(handle)
        if handle in self.df_users["screen_name"].values:
            return True
        return False

    def parse_user_data(self, user_response, user_fields):
        """
        parse the required fields from the twitter response
        """
        user_dict = vars(user_response)["_json"]
        responses = {}
        for field in user_fields:
            responses[field] = user_dict[field]
        responses["screen_name"] = responses["screen_name"].lower()
        return pd.DataFrame.from_dict(responses, orient="index").T

    def create_cache_file(self):
        """
        create an empty cache file
        """
        jlb.dump(pd.DataFrame(columns=self.user_fields), self.cache_file_path)

    def to_csv(self):
        """
        saves a csv file of the user data
        """
        df_out = self.df_users.copy()
        df_out.set_index("id")
        df_out.to_csv("user_data.csv")

    def _fix_handle(self, handle):
        return handle.strip("@").lower()

    def _get_num_followers(self, handle):
        """
        returns number of followers for a given handle
        """
        handle = self._fix_handle(handle)
        if not self.is_handle_cached(handle):
            self.add_user(handle)
        return self.df_users[self.df_users["screen_name"] == handle]["followers_count"]

    def _parse_followers_data(self, handle, response, followers_fields):
        """
        parses the followers tweepy response to pandas df
        """
        user_dict = vars(response)["_json"]
        follower_dict = {}
        for field in followers_fields:
            follower_dict[field] = user_dict[field]

        follower_dict["screen_name"] = follower_dict["screen_name"].lower()
        follower_dict["follows"] = handle
        return follower_dict

    def rate_limit_remaining(self):
        """
        get the remaining requests info from twitter
        """
        return self.api.rate_limit_status()["resources"]["application"]["/application/rate_limit_status"]["remaining"]

    def get_followers(self, handle):
        """
        retrieves all followers for a user, with rate limit handling
        """
        handle = self._fix_handle(handle)
        followers_df = pd.DataFrame()

        # check the user is cached, if not retrive user stats
        if not self.is_handle_cached(handle):
            self.add_user(handle)

        followers_df_path = "_data/df_followers.csv"
        followers_df = pd.DataFrame(columns=self.follower_fields)
        followers_df.to_csv(followers_df_path, index=False)

        print("remaining requests before rate limit:")
        # request the followers using tweepy
        for response in tw.Cursor(self.api.followers, handle).items(2000):
            followers_df = pd.read_csv(followers_df_path)
            followers_df = followers_df.append(
                self._parse_followers_data(handle, response, self.follower_fields), ignore_index=True
            )
            followers_df["follows"] = handle
            followers_df.to_csv(followers_df_path, index=False)
            print(self.rate_limit_remaining(), end="\r")
