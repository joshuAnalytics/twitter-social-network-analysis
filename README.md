# twitter social network analysis

A tool for generating social network analysis with twitter data. Given a list of twitter users, retrieve all the followers for those users and analyse the social network. 

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
```

## twitter_sna.collector

* collects simple metadata on [users](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object) 
* collects data on all a user's followers

## TODO

* build network relationship dataframes using followers/followed
* load into social network analysis tool