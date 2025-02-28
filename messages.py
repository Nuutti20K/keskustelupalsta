import db

def add_message(content, user_id, thread_id):
    sql = """INSERT INTO messages (content, sent_at, user_id, thread_id)
             VALUES (?, datetime('now', 'localtime'), ?, ?)"""
    db.execute(sql, [content, user_id, thread_id])

def get_messages(thread_id):
    sql = """SELECT messages.id, messages.content, messages.sent_at,
             messages.user_id, users.username
             FROM messages, users
             WHERE messages.thread_id = ? AND messages.user_id = users.id
             ORDER BY messages.id DESC"""
    return db.query(sql, [thread_id])

def get_message(message_id):
    sql = "SELECT id, content, user_id, thread_id FROM messages WHERE id = ?"
    result = db.query(sql, [message_id])
    return result[0] if result else None

def update_message(message_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ?"
    db.execute(sql, [content, message_id])

def remove_message(message_id):
    sql = "DELETE FROM messages WHERE id = ?"
    db.execute(sql, [message_id])