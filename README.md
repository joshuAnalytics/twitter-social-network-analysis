# twitter social network analysis

## api keys

To collect data, you will need a twitter api key & access token. These should be placed in a file called 'secrets.py`:

```python
access_token = "xxx"
access_token_secret = "xxx"
api_key = "xxx"
api_secret_key = "xxx"
```

## setup

```bash
conda create -n twitter-sna python=3.7
conda activate twitter-sna
pip install -e .


## Modules

`get_user_data.py` collects data on [users](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object) and stores in a dataframe. 

## TODO

* get followers for each user and store in dataframes
* build network relationship dataframes using followers/followed
* load into social network analysis tool