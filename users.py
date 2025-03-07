from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_threads(user_id):
    sql = "SELECT id, title FROM threads WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def get_messages(user_id):
    sql = """SELECT messages.id, messages.content, messages.sent_at,
             messages.thread_id, threads.title
             FROM messages JOIN threads ON messages.thread_id = threads.id
             WHERE messages.user_id = ?
             ORDER BY messages.id DESC"""
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None