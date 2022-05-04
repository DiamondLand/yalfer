import os
import sqlite3

dump_ = open("dump.sql", encoding="utf-8")
dump_sql = dump_.read()

if os.path.exists("database.db"):
    os.remove("database.db")

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.executescript(dump_sql)
