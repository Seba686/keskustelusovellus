CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT UNIQUE
);

CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    subscribed BOOLEAN,
    UNIQUE (topic_id, user_id)
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    title TEXT,
    content TEXT,
    image TEXT,
    created TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES threads,
    user_id INTEGER REFERENCES users,
    content TEXT,
    created TIMESTAMP
);