import sqlite3

DB_NAME = "chat.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        mobile TEXT,
        guardian_name TEXT,
        guardian_mobile TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_message TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        user_id INTEGER NOT NULL,
        key TEXT NOT NULL,
        value TEXT,
        PRIMARY KEY (user_id, key),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


def create_user(username, password, mobile, guardian_name, guardian_mobile):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (username, password, mobile, guardian_name, guardian_mobile)
        VALUES (?, ?, ?, ?, ?)
        """,
        (username, password, mobile, guardian_name, guardian_mobile)
    )
    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, username, password, mobile, guardian_name, guardian_mobile
        FROM users
        WHERE username = ?
        """,
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, username, password, mobile, guardian_name, guardian_mobile
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def update_password(username, new_password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (new_password, username)
    )
    conn.commit()
    conn.close()


def save_chat(user_id, user_message, bot_response):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chats (user_id, user_message, bot_response) VALUES (?, ?, ?)",
        (user_id, user_message, bot_response)
    )
    conn.commit()
    conn.close()


def get_chat_history(user_id, limit=50):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_message, bot_response
        FROM chats
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]


def set_memory(user_id, key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memory (user_id, key, value)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, key) DO UPDATE SET value = excluded.value
    """, (user_id, key, value))
    conn.commit()
    conn.close()


def get_memory(user_id, key):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT value FROM memory WHERE user_id = ? AND key = ?",
        (user_id, key)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None