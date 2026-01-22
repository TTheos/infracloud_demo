import pyotp  # generates one-time passwords (installed in lab, not used further here)
import sqlite3  # database for username/passwords
import hashlib  # secure hashes and message digests
import uuid  # for creating universally unique identifiers (not used further here)
from flask import Flask, request

app = Flask(__name__)  # two underscores before and after name
db_name = 'test.db'


@app.route('/')
def index():
    return 'Welcome to the hands-on lab for an evolution of password systems!'


#########################################
# Plain Text (v1)
#########################################
@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN
    (USERNAME TEXT PRIMARY KEY NOT NULL,
    PASSWORD TEXT NOT NULL);''')
    conn.commit()

    try:
        # Use parameters to avoid SQL injection issues
        c.execute("INSERT INTO USER_PLAIN (USERNAME,PASSWORD) VALUES (?, ?)",
                  (request.form['username'], request.form['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "username has been registered."

    conn.close()
    print('username: ', request.form['username'], ' password: ', request.form['password'])
    return "signup success"


def verify_plain(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?", (username,))
    record = c.fetchone()
    conn.close()
    if not record:
        return False
    return record[0] == password


@app.route('/login/v1', methods=['GET', 'POST'])
def login_v1():
    if request.method == 'POST':
        if verify_plain(request.form['username'], request.form['password']):
            return 'login success'
        return 'Invalid username/password'
    return 'Invalid Method'


#########################################
# Password Hashing (v2) - SHA256 without salt
#########################################
@app.route('/signup/v2', methods=['GET', 'POST'])
def signup_v2():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
    (USERNAME TEXT PRIMARY KEY NOT NULL,
    HASH TEXT NOT NULL);''')
    conn.commit()

    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) VALUES (?, ?)",
                  (request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "username has been registered."

    conn.close()
    print('username: ', request.form['username'], ' password: ', request.form['password'], ' hash: ', hash_value)
    return "signup success"


def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT HASH FROM USER_HASH WHERE USERNAME = ?", (username,))
    record = c.fetchone()
    conn.close()
    if not record:
        return False
    return record[0] == hashlib.sha256(password.encode()).hexdigest()


@app.route('/login/v2', methods=['GET', 'POST'])
def login_v2():
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            return 'login success'
        return 'Invalid username/password'
    return 'Invalid Method'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')

