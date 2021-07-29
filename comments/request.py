import sqlite3
import json
from models import comment


def create_comment(new_comment):

    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO comments
            (post_id, author_id, content, created_on)
        VALUES
            (?, ?, ?, ?);
        """, (new_comment['post_id'], new_comment['author_id'], new_comment['content'], new_comment['created_on']))

        id = db_cursor.lastrowid

        new_comment['id'] = id

    return json.dumps(new_comment)
