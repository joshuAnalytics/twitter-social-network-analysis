# ----------------- sample script to load csv data into neo4j -----------------
import glob
import pandas as pd

from twitter_sna.neo4j_connector import Connection

CSV_PATH = "_data/df_followers_*.csv"
A_COL = "screen_name"
B_COL = "follows"

# establish connection to neo4j db
conn = Connection(uri="neo4j://localhost:7687", user="", password="")

# clear the db
conn.delete_all()

# load csvs
df = pd.concat([pd.read_csv(f, usecols=[A_COL, B_COL], nrows=10) for f in glob.glob(CSV_PATH)], ignore_index=True)

# run cypher queries to load the data
for row in df.itertuples(index=False):
    conn.link_users(row[0], row[1], rtype="FOLLOWS")
    print(f"linked {row[0]} -> {row[1]}")
