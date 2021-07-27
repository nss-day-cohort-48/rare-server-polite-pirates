import sqlite3
import json


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

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the user dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_user["id"] = id

    return json.dumps(new_user)
