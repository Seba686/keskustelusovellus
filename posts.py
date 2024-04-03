from sqlalchemy.sql import text

from db import db

def show_threads():
    result = db.session.execute(text("SELECT id, title, content, created FROM threads ORDER BY created DESC"))
    threads = result.fetchall()
    return threads

def new_thread(title, content):
    sql = text("INSERT INTO threads (title, content, created) VALUES (:title, :content, NOW())")
    db.session.execute(sql, {"title":title, "content":content})
    db.session.commit()