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


def get_all_comments():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id
            c.author_id
            c.content
            
        FROM Comments c
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = comments(row['id'], row['post_id'], row['author_id'], row['content'],)
            comments.append(comment.__dict__)

    return json.dumps(comments)
