import sqlite3
import json
from models import Post


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
            u.first_name user_first_name,
            u.last_name user_last_name,
            c.label category_label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        """)

        posts = []

        dataset = db_cursor.fetchall()

        # Get the owners of the animal by following the relationship from customers to animal
        # through the join table
        db_cursor.execute("""
                 Select
                     c.id,
                     c.name
                 From Customer c
                 Join CustomerAnimal ca on c.id = ca.customer_id
                 Join Animal a on a.id = ca.animal_id
                 where a.id = ?
             """, (animal.id, ))
        customer_rows = db_cursor.fetchall()
        # Loop through the customer_rows to create a dictionary for each customer
        # then append the customer to the customers list in animal
        for customer_row in customer_rows:
            customer = {
                'id': customer_row['id'],
                'name': customer_row['name']
            }
            animal.customers.append(customer)

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
