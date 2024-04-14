from sqlalchemy.sql import text

from db import db

def get_threads():
    result = db.session.execute(text("SELECT T.id, U.username, T.title, T.content, T.created FROM \
                                     threads T, users U WHERE T.user_id=U.id ORDER BY created DESC"))
    threads = result.fetchall()
    return threads

def get_thread(thread_id):
    sql = text("SELECT T.id, U.username, T.title, T.content, T.created FROM \
                threads T, users U WHERE T.user_id=U.id AND T.id=:id")
    result = db.session.execute(sql, {"id":thread_id})
    thread = result.fetchone()
    return thread

def new_thread(user_id, title, content):
    errors = []
    thread_id = None
    if not title:
        errors.append("Otsikko ei voi olla tyhjä.")
    elif len(title) > 120:
        errors.append("Otsikon enimmäispituus on 120 merkkiä.")
    if len(content) > 5000:
        errors.append("Viestin enimmäispituus on 5000 merkkiä.")
    if not errors:
        sql = text("INSERT INTO threads (user_id, title, content, created) \
                VALUES (:user_id, :title, :content, NOW()) RETURNING id")
        result = db.session.execute(sql, {"user_id":user_id, "title":title, "content":content})
        db.session.commit()
        thread_id = result.fetchone()[0]
    return errors, thread_id

def get_comments(thread_id):
    sql = text("SELECT U.username, C.content, C.created FROM \
               comments C, users U WHERE C.user_id=U.id AND thread_id=:id")
    result = db.session.execute(sql, {"id":thread_id})
    comments = result.fetchall()
    return comments

def new_comment(thread_id, user_id, content):
    errors = []
    if not content:
        errors.append("Kommentti ei voi olla tyhjä.")
    if len(content) > 5000:
        errors.append("Kommentin enimmäispituus on 5000 merkkiä.")
    if not errors:
        sql = text("INSERT INTO comments (thread_id, user_id, content, created) \
                VALUES (:thread_id, :user_id, :content, NOW())")
        db.session.execute(sql, {"thread_id":thread_id, "user_id":user_id, "content":content})
        db.session.commit()
        return errors
    else:
        return errors