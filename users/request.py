import sqlite3
import json
from models import Users

def get_all_users():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u
        """)

        users = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            user = Users(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
            users.append(user.__dict__)

    return json.dumps(users)



def create_user(new_user):
    """Creating user in SQL"""
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Users
            ( first_name, last_name, email, bio, username, password, profile_image_url, created_on, active )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
            (
                new_user["first_name"],
                new_user["last_name"],
                new_user["email"],
                new_user["bio"],
                new_user["username"],
                new_user["password"],
                new_user["profile_image_url"],
                new_user["created_on"],
                new_user["active"]
            ),
        )

        id = db_cursor.lastrowid

        new_user["id"] = id

    return json.dumps(new_user)

def login_user(user):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.email,
            u.password
        FROM users u
        WHERE u.email = ?
        AND u.password = ?
        """, ( user["email"], user["password"]))

        data = db_cursor.fetchone()

        user = {
           "token": data['id'], 
           "valid": True
        }

        return json.dumps(user)