from sqlalchemy.sql import text

from db import db

def get_threads():
    result = db.session.execute(text("SELECT T.id, U.username, T.title, T.content, T.created FROM \
                                     threads T, users U WHERE T.user_id=U.id ORDER BY created DESC"))
    threads = result.fetchall()
    return threads

def new_thread(user_id, title, content):
    # TODO: check input
    sql = text("INSERT INTO threads (user_id, title, content, created) VALUES (:user_id, :title, :content, NOW())")
    db.session.execute(sql, {"user_id":user_id, "title":title, "content":content})
    db.session.commit()