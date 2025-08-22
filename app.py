import os
import random
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_default_secret_key_if_not_set_in_env") # Use environment variable for secret key, fallback for local dev

# ----------- Database Initialization -----------
def init_db():
    conn = None
    try:
        conn = sqlite3.connect('clues.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS clues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Database 'clues.db' initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

# ----------- Chatbot Logic Configuration -----------
CORRECT_PASSCODE = "~key~986~sos"
MESSAGES_FILE = 'msgs.txt' # Path to your messa ges file

# Load messages from msgs.txt
def load_random_messages():
    messages = []
    # Construct the absolute path to msgs.txt to ensure it's found correctly
    # Assumes msgs.txt is in the same directory as app.py
    messages_file_path = os.path.join(app.root_path, MESSAGES_FILE)
    
    if os.path.exists(messages_file_path):
        try:
            with open(messages_file_path, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f if line.strip()]
            print(f"Messages loaded successfully from {MESSAGES_FILE}")
        except Exception as e:
            print(f"Error reading {MESSAGES_FILE}: {e}. Using default messages.")
            messages = [
                "You're getting warmer, spy!",
                "Not quite, but your efforts are noted.",
                "The truth is out there, but not here, Agent.",
                "Keep searching, the secret awaits."
            ]
    else:
        print(f"Warning: {MESSAGES_FILE} not found at {messages_file_path}. Using default messages.")
        messages = [
            "You're getting warmer, spy!",
            "Not quite, but your efforts are noted.",
            "The truth is out there, but not here, Agent.",
            "Keep searching, the secret awaits."
        ]
    return messages

# Load messages when the server starts
RANDOM_MESSAGES = load_random_messages()


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

        conn = sqlite3.connect('clues.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid credentials. Please try again."

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

# Route for the story page
@app.route('/story')
def story():
    return render_template('story.html')

# Route for the image page
@app.route('/backstory')
def backstory():
    return render_template('backstory.html')

@app.route('/testimony_info')
def testimony_info():
    return render_template('testimony_info.html')

# Route for the backstory info page
@app.route('/backstory_info')
def backstory_info():
    return render_template('backstory_info.html')

@app.route('/story_testimony')
def story_testimony():
    return render_template('story_testimony.html')

@app.route('/testimony')
def testimony():
    return render_template('testimony.html')

@app.route('/The_Final_Report')
def The_Final_Report():
    """Serves the PDF file from the 'static' folder."""
    try:
        # send_from_directory is a secure way to send files from a directory.
        return send_from_directory(
            'static',  # The directory where the file is stored
            'The_Truth.pdf',  # The name of the file
            as_attachment=False  # Set to False to display it in the browser
        )
    except FileNotFoundError:
        return "Error: File not found.", 404

@app.route('/The_Truth')
def The_Truth():
    """Serves the PDF file from the 'static' folder."""
    try:
        # send_from_directory is a secure way to send files from a directory.
        return send_from_directory(
            'static',  # The directory where the file is stored
            'The_Final_report.pdf',  # The name of the file
            as_attachment=False  # Set to False to display it in the browser
        )
    except FileNotFoundError:
        return "Error: File not found.", 404




'''@app.route("/backstory")
def backstory():
    return render_template("backstory_info.html")
    '''

# New route for the special Grand Revel Passcode page
@app.route('/GrandRevelPwd')
def grand_revel_pwd():
    return render_template('GrandRevelPwd.html')
'''
# Bot message handling route
# This route receives POST requests from your chatbot's frontend
@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json() # Get JSON data from the request body
    received_msg = data.get('message', '').strip() # Extract the 'message' field and strip whitespace
    
    response_text = ""

    if received_msg == CORRECT_PASSCODE:
        # Exact match: Instruct the client-side JavaScript to redirect
        print("Correct passcode received. Instructing client to redirect.")
        # Return a JSON response with a 'redirect' URL
        return jsonify(success=True, redirect=url_for('grand_revel_pwd'))
        
    elif received_msg.startswith("~") and "~" in received_msg[1:]: # Checks for '~' followed by another '~'
        # Partial match: message starts with '~' and contains at least one other '~'
        if RANDOM_MESSAGES:
            response_text = random.choice(RANDOM_MESSAGES)
        else:
            response_text = "You're close, but no hints loaded yet!" # Fallback if msgs.txt is empty
        print(f"Partial match. Sending random message: {response_text}")
        return jsonify(success=True, message=response_text)
    else:
        # No match or invalid format
        response_text = "Try harder, this is a passcode for top secret stuff"
        print(f"No match. Sending: {response_text}")
        return jsonify(success=True, message=response_text)
'''
# Bot message handling route
# This route receives POST requests from your chatbot's frontend
@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json() # Get JSON data from the request body
    received_msg = data.get('message', '').strip() # Extract the 'message' field and strip whitespace
    
    response_text = ""

    # --- MODIFIED LOGIC ---
    # 1. Get the set of correct tokens
    # We use filter(None, ...) to remove empty strings that result from splitting by '~'
    correct_tokens = set(filter(None, CORRECT_PASSCODE.split('~')))
    
    # 2. Get the set of tokens from the user's message
    received_tokens = set(filter(None, received_msg.split('~')))

    # 3. Check for an exact match first
    if received_msg == CORRECT_PASSCODE:
        # Exact match: Instruct the client-side JavaScript to redirect
        print("Correct passcode received. Instructing client to redirect.")
        # Return a JSON response with a 'redirect' URL
        return jsonify(success=True, redirect=url_for('grand_revel_pwd'))
    
    # 4. NEW: Check if the tokens are correct but jumbled
    elif correct_tokens == received_tokens:
        response_text = "Try juggling the tokens"
        print(f"Jumbled passcode received. Sending hint: {response_text}")
        return jsonify(success=True, message=response_text)

    # 5. Check for a partial match (original logic)
    elif received_msg.startswith("~") and "~" in received_msg[1:]: # Checks for '~' followed by another '~'
        if RANDOM_MESSAGES:
            response_text = random.choice(RANDOM_MESSAGES)
        else:
            response_text = "You're close, but no hints loaded yet!" # Fallback if msgs.txt is empty
        print(f"Partial match. Sending random message: {response_text}")
        return jsonify(success=True, message=response_text)
    
    # 6. If none of the above, it's an incorrect attempt
    else:
        # No match or invalid format
        response_text = "Try harder, this is a passcode for top secret stuff"
        print(f"No match. Sending: {response_text}")
        return jsonify(success=True, message=response_text)



if __name__ == "__main__":
    init_db()  # Initialize the database when the app starts

    # Use environment variable for port, default to 5000 if not set (for local development)
    port = int(os.environ.get("PORT", 5000))
    
    # Run the Flask app
    # host='0.0.0.0' makes it accessible externally (e.g., in a Docker container or server)
    # debug=False for production hosting
    app.run(host='0.0.0.0', port=port, debug=False)
