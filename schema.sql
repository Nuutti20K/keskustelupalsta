CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users
)

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    item_id INTEGER REFERENCES items
)