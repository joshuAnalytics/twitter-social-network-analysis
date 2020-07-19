# twitter social network analysis

## Setup

To collect data, you will need a twitter api key & access token. These should be placed in a file called 'secrets.py`:

```python
access_token = "xxx"
access_token_secret = "xxx"
api_key = "xxx"
api_secret_key = "xxx"
```

## Modules

`get_user_data.py` collects data on [users](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object) and stores in a dataframe. 

## TODO

* get followers for each user and store in dataframes
* build network relationship dataframes using followers/followed
* load into social network analysis tool