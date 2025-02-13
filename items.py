import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def add_item(title, user_id, classes):
    sql = """INSERT INTO items (title, user_id)
             VALUES (?, ?)"""
    db.execute(sql, [title, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])

def get_items():
    sql = """SELECT items.id, items.title, items.user_id, users.username
             FROM items JOIN users ON items.user_id = users.id
             GROUP BY items.id
             ORDER BY items.id DESC"""
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.user_id,
                    users.username
             FROM items, users
             WHERE items.user_id = users.id AND
                   items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, classes):
    sql = "UPDATE items SET title = ? WHERE id = ?"
    db.execute(sql, [title, item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title
             FROM items
             WHERE title LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like])

def add_message(content, user_id, item_id):
    sql = """INSERT INTO messages (content, user_id, item_id)
             VALUES (?, ?, ?)"""
    db.execute(sql, [content, user_id, item_id])

def get_messages(item_id):
    sql = """SELECT messages.id, messages.content, messages.user_id, users.username
             FROM messages, users
             WHERE messages.item_id = ? AND messages.user_id = users.id
             ORDER BY messages.id DESC"""
    return db.query(sql, [item_id])

def get_message(message_id):
    sql = "SELECT id, content, user_id, item_id FROM messages WHERE id = ?"
    result = db.query(sql, [message_id])
    return result[0] if result else None

def update_message(message_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ?"
    db.execute(sql, [content, message_id])

def remove_message(message_id):
    sql = "DELETE FROM messages WHERE id = ?"
    db.execute(sql, [message_id])