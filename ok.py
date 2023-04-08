import sqlite3

con = sqlite3.connect("simple.db")

cur = con.cursor()

res = cur.execute("SELECT * FROM simple;")

print(res.fetchall())

con.commit()
con.close()