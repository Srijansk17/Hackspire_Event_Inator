import sqlite3

# Connect to the clues.db database
conn = sqlite3.connect('clues.db')
c = conn.cursor()

# Add users here
users = [
    ('Agent_P', 'Perry_the_Platypus'),
    ('Admin1', '1two3fore5'),
    ('Admin2', '1two3fore5'),
    ('Admin3', '1two3fore5'),
    ('Team_1','Password_for_team_1'),
    ('Team_2','Password_for_team_2'),
    ('Team_3','Password_for_team_3'),
    ('Team_4','Password_for_team_4'),
    ('Team_5','Password_for_team_5'),
    ('Team_6','Password_for_team_6'),
    ('Team_7','Password_for_team_7'),
    ('Team_8','Password_for_team_8'),
    ('Team_9','Password_for_team_9'),
    ('Team_10','Password_for_team_10'),
    ('Team_11','Password_for_team_11'),
    ('Team_12','Password_for_team_12')
]

for username, password in users:
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists")

conn.commit()
conn.close()
print("Users added successfully.")