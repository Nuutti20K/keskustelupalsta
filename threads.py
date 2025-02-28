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

def get_classes(thread_id):
    sql = "SELECT title, value FROM thread_classes WHERE thread_id = ?"
    return db.query(sql, [thread_id])

def add_thread(title, user_id, classes):
    sql = """INSERT INTO threads (title, user_id)
             VALUES (?, ?)"""
    db.execute(sql, [title, user_id])

    thread_id = db.last_insert_id()

    sql = "INSERT INTO thread_classes (thread_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [thread_id, class_title, class_value])

def get_threads():
    sql = """SELECT threads.id, threads.title, threads.user_id, users.username
             FROM threads JOIN users ON threads.user_id = users.id
             GROUP BY threads.id
             ORDER BY threads.id DESC"""
    return db.query(sql)

def get_thread(thread_id):
    sql = """SELECT threads.id,
                    threads.title,
                    threads.user_id,
                    users.username
             FROM threads, users
             WHERE threads.user_id = users.id AND
                   threads.id = ?"""
    result = db.query(sql, [thread_id])
    return result[0] if result else None

def update_thread(thread_id, title, classes):
    sql = "UPDATE threads SET title = ? WHERE id = ?"
    db.execute(sql, [title, thread_id])

    sql = "DELETE FROM thread_classes WHERE thread_id = ?"
    db.execute(sql, [thread_id])

    sql = "INSERT INTO thread_classes (thread_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [thread_id, class_title, class_value])

def remove_thread(thread_id):
    sql = "DELETE FROM threads WHERE id = ?"
    db.execute(sql, [thread_id])

def find_threads(query):
    sql = """SELECT id, title
             FROM threads
             WHERE title LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like])