from sqlalchemy.sql import text
from db import db
from werkzeug.utils import secure_filename
import time
import os
import app

def get_threads():
    result = db.session.execute(text("SELECT T.id, U.username, T.title, T.content, T.image, T.created FROM \
                                     threads T, users U WHERE T.user_id=U.id ORDER BY created DESC"))
    threads = result.fetchall()
    return threads

def get_thread(thread_id):
    sql = text("SELECT T.id, U.username, T.title, T.content, T.image, T.created FROM \
                threads T, users U WHERE T.user_id=U.id AND T.id=:id")
    result = db.session.execute(sql, {"id":thread_id})
    thread = result.fetchone()
    return thread

def new_thread(user_id, title, content, image):
    errors = []
    thread_id = None
    if not title:
        errors.append("Otsikko ei voi olla tyhjä.")
    elif len(title) > 120:
        errors.append("Otsikon enimmäispituus on 120 merkkiä.")
    if len(content) > 5000:
        errors.append("Viestin enimmäispituus on 5000 merkkiä.")
    if image and not allowed_file(image.filename):
        errors.append("Väärä tiedostomuoto.")
    if not errors:
        if image:
            filename = secure_filename(image.filename)
            filename = filename + str(time.time())
            image.save(os.path.join(app.UPLOAD_FOLDER, filename))
        else:
            filename = None
        sql = text("INSERT INTO threads (user_id, title, content, image, created) \
                VALUES (:user_id, :title, :content, :image, NOW()) RETURNING id")
        result = db.session.execute(sql, {"user_id":user_id, "title":title, "content":content, "image":filename})
        db.session.commit()
        thread_id = result.fetchone()[0]
    return errors, thread_id

def get_comments(thread_id):
    sql = text("SELECT U.username, C.content, C.created FROM \
               comments C, users U WHERE C.user_id=U.id AND C.thread_id=:id")
    result = db.session.execute(sql, {"id":thread_id})
    comments = result.fetchall()
    return comments

def get_comment_count(thread_id):
    sql = text("SELECT COUNT(*) FROM comments WHERE thread_id=:id")
    result = db.session.execute(sql, {"id":thread_id})
    count = result.fetchone()[0]
    return count

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

    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.ALLOWED_EXTENSIONS