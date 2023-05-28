import sqlite3

# ========================USERS=============
connection_user = sqlite3.connect("social_network.db")
cursor_user = connection_user.cursor()

cursor_user.execute("DROP TABLE IF EXISTS users")

sql = """CREATE TABLE users(
   id INTEGER PRIMARY KEY,
   FIRST_NAME VARCHAR(100) NOT NULL,
   LAST_NAME VARCHAR(100) NOT NULL,
   AGE INTEGER NOT NULL,
   SEX VARCHAR(6)
)"""
cursor_user.execute(sql)
cursor_user.execute(
    "INSERT INTO users \
                    VALUES (1, 'Leonard', 'Hofstadter', 31, 'm')"
)
cursor_user.execute(
    "INSERT INTO users \
                    VALUES (2, 'Sheldon', 'Cooper', 35, 'm')"
)
cursor_user.execute("SELECT * FROM users")
rows = cursor_user.fetchall()
for row in rows:
    print(row)

connection_user.close()


# ========================PROFILES=============
connection_profiles = sqlite3.connect("social_network.db")
cursor_profiles = connection_profiles.cursor()

cursor_profiles.execute("DROP TABLE IF EXISTS profiles")

sql = """CREATE TABLE profiles(
   user_id INTEGER PRIMARY KEY,
   post_id INTEGER NOT NULL,
   followers INTEGER,
   subscriptions INTEGER
)"""
cursor_profiles.execute(sql)
cursor_profiles.execute("INSERT INTO profiles VALUES (1, 1, 2, 5)")
cursor_profiles.execute("INSERT INTO profiles VALUES (2, 1, 0, 0)")
cursor_profiles.execute("SELECT * FROM profiles")
rows = cursor_profiles.fetchall()
for row in rows:
    print(row)

connection_profiles.close()


# ========================POSTS=============
connection_posts = sqlite3.connect("social_network.db")
cursor_posts = connection_posts.cursor()

cursor_posts.execute("DROP TABLE IF EXISTS users")

sql = """CREATE TABLE users(
   post_id INTEGER PRIMARY KEY,
   number_of_likes INTEGER,
   number_of_comments INTEGER,
   post_content VARCHAR(200)
)"""
cursor_posts.execute(sql)
cursor_posts.execute("INSERT INTO users VALUES (1, 0, 1,'hi')")
cursor_posts.execute("INSERT INTO users VALUES (2, 4, 6,'cats are cute')")
cursor_posts.execute("SELECT * FROM users")
rows = cursor_posts.fetchall()
for row in rows:
    print(row)

connection_posts.close()


# ========================COMMENTS=============
connection_comments = sqlite3.connect("social_network.db")
cursor_comments = connection_comments.cursor()

cursor_comments.execute("DROP TABLE IF EXISTS users")

sql = """CREATE TABLE users(
   comment_id INTEGER PRIMARY KEY,
   post_id INTEGER,
   comment_user_id INTEGER,
   comment_content VARCHAR(150)
)"""
cursor_comments.execute(sql)
cursor_comments.execute("INSERT INTO users VALUES (1, 1, 2,'hello')")
cursor_comments.execute("INSERT INTO users VALUES (2, 2, 1,'totally agree')")
cursor_comments.execute("SELECT * FROM users")
rows = cursor_comments.fetchall()
for row in rows:
    print(row)

connection_comments.close()


# ========================LIKES=============
connection_likes = sqlite3.connect("social_network.db")
cursor_likes = connection_likes.cursor()

cursor_likes.execute("DROP TABLE IF EXISTS users")

sql = """CREATE TABLE users(
   post_id INTEGER PRIMARY KEY,
   like_id INTEGER NOT NULL,
   user_id INTEGER NOT NULL
)"""
cursor_likes.execute(sql)
cursor_likes.execute("INSERT INTO users VALUES (1, 1, 1)")
cursor_likes.execute("INSERT INTO users VALUES (2, 2, 2)")
cursor_likes.execute("SELECT * FROM users")
rows = cursor_likes.fetchall()
for row in rows:
    print(row)

connection_likes.close()
