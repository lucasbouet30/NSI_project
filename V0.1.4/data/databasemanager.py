import sqlite3
import os

con = sqlite3.connect("bob.db")
cur = con.cursor()
clear = lambda: os.system('cls')

while True:
    usrinput = input("->    ")
    
    if usrinput.lower() in ["cls", "clear"]:
        clear()
        continue
    elif usrinput == ".tables":
        usrinput = 'SELECT * FROM sqlite_master WHERE type="table"'

    try:
        res = cur.execute(usrinput)
        print(res.fetchall())
        con.commit()
    except Exception as e:
        print("error:", e)
