import sqlite3

con = sqlite3.connect("simple.db")

cur = con.cursor()

res = cur.execute("SELECT * FROM simple.sqlite_master WHERE type='table';")

print(res.fetchone())

con.commit()
con.close()