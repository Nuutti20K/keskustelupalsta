CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE threads (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE thread_classes (
    id INTEGER PRIMARY KEY,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
    title TEXT,
    value TEXT
);