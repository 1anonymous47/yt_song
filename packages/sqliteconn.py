import sqlite3

def initdb():
    try:
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()

        #-------------- If not exists

        #-------------- CREATE USERS TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50),
            status INTEGER NOT NULL DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_userongs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50),
            songid VARCHAR(12),
            status INTEGER NOT NULL DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            songid VARCHAR(12),
            tittle VARCHAR(100),
            audiosrc VARCHAR(24),
            videosrc VARCHAR(255),
            duration VARCHAR(12),
            status INTEGER NOT NULL DEFAULT 0
        )
        """)

        sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()

        #------------------
        return True
    except Exception as e:
        print("SQLITE DB Error ",e)
        return False

def initconn():
    try:
        sqliteConnection = sqlite3.connect('sql.db')
        return sqliteConnection

    except Exception as e:
        print("DB CONNECTION ERROR ",e)
        return False



