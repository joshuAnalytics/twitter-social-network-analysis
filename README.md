# twitter social network analysis

A tool for generating social network analysis with twitter data. Given a list of twitter users, retrieve all the followers for those users and analyse the social network. 

# main components: 

* data collector: collects data on all a user's followers
* graph: *WIP*

# setup

## api keys

To collect data, you will need a twitter api key & access token. These should be placed in a file called 'secrets.py`:

```python
access_token = "xxx"
access_token_secret = "xxx"
api_key = "xxx"
api_secret_key = "xxx"
```

## python env setup

```bash
conda create -n twitter-sna python=3.7
conda activate twitter-sna
pip install -e .
```

## neo4j setup

* [download JDK](https://neo4j.com/docs/operations-manual/current/installation/requirements/) and install

* [download neo4j server community edition](https://neo4j.com/download-center/#community)

start the server:

```bash
bash neo4j-community-4.1.3/bin/neo4j start
```



