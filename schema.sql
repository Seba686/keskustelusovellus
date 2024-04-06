CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    link TEXT,
    created TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);