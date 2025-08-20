import sqlite3

# Connect to the clues.db database
conn = sqlite3.connect('clues.db')
c = conn.cursor()

# Add users here
users = [
    ('Admin', 'A_joy_ride'),
    ('Team_001','65_joy_001'),
    ('Team_002','65_joy_002'),
    ('Team_003','65_joy_003'),
    ('Team_004','65_joy_004'),
    ('Team_005','65_joy_005'),
    ('Team_006','65_joy_006'),
    ('Team_007','65_joy_007'),
    ('Team_008','65_joy_008'),
    ('Team_009','65_joy_009'),
    ('Team_010','65_joy_010'),
    ('Team_011','65_joy_011'),
    ('Team_012','65_joy_012'),
    ('Team_013','65_joy_013'),
    ('Team_014','65_joy_014'),
    ('Team_015','65_joy_015')
]

for username, password in users:
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists")

conn.commit()
conn.close()
print("Users added successfully.")