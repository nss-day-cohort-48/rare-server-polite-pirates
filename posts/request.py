import sqlite3
import json
from models import Post, Users, Categories


def get_all_posts():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.id user_id,
            u.first_name user_first_name,
            u.last_name user_last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            c.id category_id,
            c.label category_label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'],
                        row['image_url'], row['content'], row['approved'])

            user = Users(row['user_id'], row['user_first_name'], row['user_last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
            
            category = Categories(row['category_id'], row['category_label'])

            post.user_display_name = {"user_name":row["username"]}

            post.user = user.__dict__
            post.category = category.__dict__

            posts.append(post.__dict__)

        return json.dumps(posts)


def get_single_post(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM posts p
        WHERE p.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                    data['publication_date'], data['image_url'], data['content'], data['approved'])

        return json.dumps(post.__dict__)


def create_post(new_post):

    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            (?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], new_post['approved']))

        id = db_cursor.lastrowid

        new_post['id'] = id

        # new_post['tags']: the client should pass a list of tag_id's
        # to be associated with this post
        for tag_id in new_post['tags']:
            # When interating (looping) through the list we can insert the tag_id
            # and new_post['id'] into the tagpost table to set up the
            # many to many relationship
            db_cursor.execute("""
            INSERT INTO PostTags
                (tag_id, post_id)
            VALUES (?, ?)
            """, (tag_id, new_post['id']))

    return json.dumps(new_post)


def delete_post(id):
    """
        DELETE FROM posts
        WHERE id = ?
    """, (id, )


def update_post(id, new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'], new_post['approved'], id))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True
