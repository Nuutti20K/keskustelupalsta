import db

def add_item(title, user_id):
    sql = """INSERT INTO items (title, user_id)
             VALUES (?, ?)"""
    db.execute(sql, [title, user_id])

def get_items():
    sql = """SELECT items.id, items.title, users.id user_id, users.username
             FROM items JOIN users ON items.user_id = users.id
             GROUP BY items.id
             ORDER BY items.id DESC"""
    return db.query(sql)
