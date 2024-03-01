import sqlite3

DATABASE = 'tasks.db'

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE tasks (
        Name TEXT NOT NULL,
        Id INTEGER PRIMARY KEY,
        Points INTEGER NOT NULL,
        Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

connection.commit()
connection.close()
