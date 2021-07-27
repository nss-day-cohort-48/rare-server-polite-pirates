import sqlite3
import json
from models import Users

def get_all_users():
    with sqlite3.connect(".rare.db") as conn:
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
        FROM users u
        """)

        users = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            user = Users(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
            users.append(user.__dict__)

    return json.dumps(users)