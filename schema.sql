CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    title TEXT,
    content TEXT,
    link TEXT,
    created TIMESTAMP
);