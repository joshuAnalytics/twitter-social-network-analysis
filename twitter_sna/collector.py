import tweepy as tw
import secrets as s
import joblib
import pandas as pd
import os


class DataCollector:
    def __init__(self, tweepy_api, cache_path="_cache", cache_file="df_users.jlb"):
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
        self.cache_file_path = os.path.join(cache_path, cache_file)
        if os.path.exists(self.cache_file_path):
            self.df_users = joblib.load(self.cache_file_path)
        else:
            self.create_cache_file()
            self.df_users = joblib.load(self.cache_file_path)

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
        joblib.dump(pd.DataFrame(columns=self.user_fields), self.cache_file_path)

    def to_csv(self):
        """
        saves a csv file of the user data
        """
        df_out = self.df_users.copy()
        df_out.set_index("id")
        df_out.to_csv("user_data.csv")

    def _fix_handle(self, handle):
        return handle.strip("@").lower()

    def get_followers(self, handle):
        """
        retrieves all followers for a user, with rate limit handling
        """
        handle = self._fix_handle(handle)
        followers_df = pd.DataFrame()
        # check the user is cached, if not retrive user stats
        if not self.is_handle_cached(screen_name):
            self.add_user(screen_name)

        print(self.df_users[self.df_users["screen_name"] == screen_name])

        # for response in limit_handled(tw.Cursor(api.followers, handle).items()):
        # print(response.screen_name)
        # followers_df = followers_df.append(parse_followers_data(handle, response, followers_fields), ignore_index=True)
        # followers_df.to_csv("_data/df_followers.csv", index=False)