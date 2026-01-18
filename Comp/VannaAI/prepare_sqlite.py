import pandas as pd
import sqlite3

df = pd.read_csv("test.csv")
conn = sqlite3.connect("test.db")
df.to_sql("test", conn, if_exists="replace", index=False)

conn.close()
