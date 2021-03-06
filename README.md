# twitter social network analysis

A tool for generating social network analysis with twitter data. Given a list of twitter users, retrieve all the followers for those users and analyse the social network. 

* collector: collects data on all a user's followers and stores them as csv files
* neo4j_connector: builds a social network graph using the relationships from the collected twitter users

<br/><br/>

# instructions

see examples in scripts folder

<br/><br/>
# setup

## api keys

To collect data, you will need a twitter api key & access token. These should be placed in a file called 'secrets.py`:

```python
access_token = "xxx"
access_token_secret = "xxx"
api_key = "xxx"
api_secret_key = "xxx"
```
<br/><br/>
## python env setup

```bash
conda create -n twitter-sna python=3.7
conda activate twitter-sna
pip install -e .
```
<br/><br/>
## neo4j setup<br/><br/>

**JDK**

[download JDK](https://neo4j.com/docs/operations-manual/current/installation/requirements/) and install

**neo4j server**

[download neo4j server community edition](https://neo4j.com/download-center/#community)

**disable auth**

in `conf/neo4j.conf`, uncomment the line: `dbms.security.auth_enabled=false`

**start the server**

```bash
bash neo4j-community-4.1.3/bin/neo4j start
```



