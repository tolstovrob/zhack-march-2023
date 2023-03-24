import sqlite3

connection = sqlite3.connect('data/users.db')


with open('data/users_schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()