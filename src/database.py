import sqlite3

DATABASE = 'hackathon_matcher.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hackathon TEXT,
                technology1 TEXT,
                technology2 TEXT,
                question1 TEXT,
                question2 TEXT,
                question3 TEXT
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                uid INTEGER,
                quid INTEGER,
                response TEXT
            )
        ''')

        db.commit()


def username_exists(db, username):
    return db.execute('SELECT 1 FROM users WHERE username = ?', (username,)).fetchone() is not None

def add_user(db, username, hackathon, technology1, technology2,
             question1,question2,question3):
    hackathon = str(hackathon)
    technology1 = str(technology1)
    technology2 = str(technology2)
    db.execute('''
        INSERT INTO users (username, hackathon, technology1, technology2,
               question1,question2,question3)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (username, hackathon, technology1, technology2, question1, question2, question3))
    db.commit()

def find_matches(db, technology):
    return db.execute('''
        SELECT * FROM users WHERE technology2 LIKE ?
    ''', ('%' + technology + '%',)).fetchall()

def get_all_users(db):
    return db.execute('''
        SELECT * FROM users
    ''',).fetchall()

def add_answer(db, uid, qid, response):
    db.execute('''
        INSERT INTO answers (uid, quid, response)
        VALUES (?, ?, ?)
    ''', (uid, qid, response))
    db.commit()


