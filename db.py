import sqlite3

con = sqlite3.connect('my_database.db')
cursor = con.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS User
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                created_at DEFAULT TIMESTAMP,
                first_name TEXT NOT NULL, 
                sur_name TEXT NOT NULL, 
                last_name TEXT, 
                role INTEGER DEFAULT 1,
                is_deleted INTEGER DEFAULT 0,
                username TEXT,
                password TEXT)
            """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Exercise
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                created_at TIMESTAMP,
                started_at TIMESTAMP,
                time_spent TEXT,
                name TEXT NOT NULL, 
                status INTEGER DEFAULT 1,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id)  REFERENCES User (id))
            """)


cursor.execute("""INSERT INTO User (first_name, sur_name, username, password) VALUES ('student', 'student', 'student', 
'student')""")

con.commit()
con.close()