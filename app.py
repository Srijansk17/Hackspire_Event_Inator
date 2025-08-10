import sqlite3
import os

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
""""""
app = Flask(__name__)
app.secret_key = "mystery_secret_key"  # Needed for sessions

# ----------- Database Initialization -----------

def init_db():
    conn = sqlite3.connect('clues.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ----------- Routes -----------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'detective' and password == 'mystery123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid credentials"
    return render_template('login.html', error=error)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('clues.db')
    c = conn.cursor()

    if request.method == 'POST':
        clue = request.form.get('clue')
        if clue:
            c.execute("INSERT INTO clues (content) VALUES (?)", (clue,))
            conn.commit()

    c.execute("SELECT * FROM clues")
    clues = c.fetchall()
    conn.close()
    return render_template("dashboard.html", clues=clues)

@app.route('/delete_clue/<int:id>', methods=['POST'])
def delete_clue(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('clues.db')
    c = conn.cursor()
    c.execute("DELETE FROM clues WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
@app.route('/login2')
def login2():
    return render_template('login2.html')

@app.route("/backstory")
def backstory():
    return render_template("backstory.html")


if __name__ == "__main__":
    init_db()  # if you're using this to create clues.db
    app.run(debug=True)
