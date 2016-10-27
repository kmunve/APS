import sqlite3

if __name__ == "__main__":
    sqlFile = "tables.sql"

    db = sqlite3.connect('test.db')
    db.execute('PRAGMA foreign_keys=ON')
    db.commit()
    cur = db.cursor()

    fd = open(sqlFile, 'r')
    sqlScript = fd.read()
    cur.executescript(sqlScript)

    db.close()


