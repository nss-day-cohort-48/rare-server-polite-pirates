CREATE TABLE "Users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "first_name" varchar,
    "last_name" varchar,
    "email" varchar,
    "bio" varchar,
    "username" varchar,
    "password" varchar,
    "profile_image_url" varchar,
    "created_on" date,
    "active" bit
);
CREATE TABLE "DemotionQueue" (
    "action" varchar,
    "admin_id" INTEGER,
    "approver_one_id" INTEGER,
    FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
    FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
    PRIMARY KEY (action, admin_id, approver_one_id)
);
CREATE TABLE "Subscriptions" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "follower_id" INTEGER,
    "author_id" INTEGER,
    "created_on" date,
    FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
    FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);
CREATE TABLE "Posts" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER,
    "category_id" INTEGER,
    "title" varchar,
    "publication_date" date,
    "image_url" varchar,
    "content" varchar,
    "approved" bit
);
CREATE TABLE "Comments" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "post_id" INTEGER,
    "author_id" INTEGER,
    "content" varchar,
    "created_on" date,
    FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
    FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);
CREATE TABLE "Reactions" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "label" varchar,
    "image_url" varchar
);
CREATE TABLE "PostReactions" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER,
    "reaction_id" INTEGER,
    "post_id" INTEGER,
    FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
    FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
    FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);
CREATE TABLE "Tags" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "label" varchar
);
CREATE TABLE "PostTags" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "post_id" INTEGER,
    "tag_id" INTEGER,
    FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);
CREATE TABLE "Categories" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "label" varchar
);
INSERT INTO Categories ('label')
VALUES ('News');
INSERT INTO Tags ('label')
VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url')
VALUES ('happy', 'https://pngtree.com/so/happy');

INSERT INTO `Posts` VALUES (null, 1, 1, "Oldest Post", 1627581763818, "empty for now", "this is a sample posts", 0);

INSERT INTO `Posts` VALUES (null, 2, 2, "Newest Post", 1627581865735, "empty for now", "this is a sample posts", 0);

INSERT INTO `Posts` VALUES (null, 2, 2, "Newester Post", 1627582049660, "empty for now", "this is a sample posts", 0);


INSERT INTO `Users` VALUES (null, "me", "mylastname", "www.me@me.com", "Interesting Bio Stuff", "meme", "password", "https://techcrunch.com/wp-content/uploads/2010/07/github-logo.png?w=512", 07-27-2021, TRUE)

INSERT INTO `Users` VALUES (null, "Hannah", "Hall", "www.sdsd.com", "Interesting Bio Stuff", "hannahHall", "password", "https://techcrunch.com/wp-content/uploads/2010/07/github-logo.png?w=512", 07-27-2021, TRUE);

INSERT INTO `Categories` VALUES (null, "News");

INSERT INTO `Tags` VALUES (null, "cool label");

INSERT INTO `PostTags` VALUES (null, 1, 1);
INSERT INTO `PostTags` VALUES (null, 7, 2);


INSERT INTO `Comments` VALUES (null, 1, 1, "This is a comment", 1627582649113);
DROP TABLE `Comments`;

SELECT *
FROM `PostTags`;

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

SELECT
    t.id,
    t.label
FROM Tags t
JOIN PostTags pt ON t.id = pt.tag_id
JOIN Posts p ON p.id = pt.post_id
WHERE p.id = 1;


SELECT
    t.id,
    t.label
FROM Tags t
JOIN PostTags pt ON t.id = pt.tag_id
JOIN Posts p ON p.id = pt.post_id
WHERE p.id = 1;