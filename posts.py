import time
import os
from itertools import zip_longest
from sqlalchemy.sql import text # Required for SQL commands.
from werkzeug.utils import secure_filename # Securely handle filenames from users.
from db import db
import app

# Get all threads. Newest thread first.
def get_threads():
    result = db.session.execute(text("SELECT Th.id, A.topic, U.username, Th.title, Th.content, \
                                     Th.image, Th.created FROM threads Th, users U, topics A WHERE \
                                     Th.user_id=U.id AND Th.topic_id=A.id ORDER BY Th.created DESC"))
    threads = result.fetchall()
    return threads

# Get specific thread. Called when the user opens the comment section.
def get_thread(thread_id):
    sql = text("SELECT T.id, A.topic, U.username, T.title, T.content, T.image, T.created FROM \
                threads T, users U, topics A WHERE T.user_id=U.id AND T.id=:id AND A.id=T.topic_id")
    result = db.session.execute(sql, {"id":thread_id})
    thread = result.fetchone()
    return thread

# Create a new thread.
def new_thread(topic, user_id, title, content, image):
    thread_id = None
    result = verify_new_thread(topic, title, content, image)
    errors = result[0]
    topic_id = result[1]
    if not errors:
        if image:
            filename = secure_filename(image.filename)
            filename = str(time.time())+ filename
            image.save(os.path.join(app.UPLOAD_FOLDER, filename))
        else:
            filename = None
        sql = text("INSERT INTO threads (topic_id, user_id, title, content, image, created) \
                VALUES (:topic_id, :user_id, :title, :content, :image, NOW()) RETURNING id")
        result = db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id, "title":title, \
                                          "content":content, "image":filename})
        db.session.commit()
        thread_id = result.fetchone()[0]
    return errors, thread_id

# Verify that a new thread can be created and handle errors.
def verify_new_thread(topic, title, content, image):
    errors = []
    if not title:
        errors.append("Otsikko ei voi olla tyhjä.")
    elif len(title) > 120:
        errors.append("Otsikon enimmäispituus on 120 merkkiä.")
    if len(content) > 5000:
        errors.append("Viestin enimmäispituus on 5000 merkkiä.")
    if not topic:
        errors.append("Aihe on pakollinen.")
    else:
        sql = text("SELECT id FROM topics WHERE topic=:topic")
        topic_id = db.session.execute(sql, {"topic":topic}).fetchone()
        if not topic_id:
            errors.append("Aihetta ei löytynyt. Luo uusi aihe.")
        else:
            topic_id = topic_id[0]
    if image and not allowed_file(image.filename):
        errors.append("Väärä tiedostomuoto.")
    return errors, topic_id

# Get comments associated with a thread.
def get_comments(thread_id):
    sql = text("SELECT U.username, C.content, C.created FROM \
               comments C, users U WHERE C.user_id=U.id AND C.thread_id=:id")
    result = db.session.execute(sql, {"id":thread_id})
    comments = result.fetchall()
    return comments

# Get number of comments.
def get_comment_count(thread_id):
    sql = text("SELECT COUNT(*) FROM comments WHERE thread_id=:id")
    result = db.session.execute(sql, {"id":thread_id})
    count = result.fetchone()[0]
    return count

# Create new comment.
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

# Create new topic.
def new_topic(topic):
    errors = []
    if len(topic) > 30:
        errors.append("Aiheen enimmäispituus on 30 merkkiä.")
    elif len(topic) < 3:
        errors.append("Aiheen minimipituus on 3 merkkiä.")
    sql = text("SELECT id FROM topics WHERE topic=:topic")
    found = db.session.execute(sql, {"topic":topic}).fetchone()
    if found:
        errors.append("Aihe on jo luotu.")
    if not errors:
        sql = text("INSERT INTO topics (topic) VALUES (:topic)")
        db.session.execute(sql, {"topic":topic})
        db.session.commit()
    return errors

# Get threads associated with a topic. 
def get_threads_by_topic(topic):
    sql = text("SELECT Th.id, U.username, Th.title, Th.content, Th.image, Th.created FROM \
                threads Th, users U, topics A WHERE Th.user_id=U.id AND A.topic=:topic AND \
                Th.topic_id=A.id ORDER BY Th.created DESC")
    result = db.session.execute(sql, {"topic":topic})
    threads = result.fetchall()
    return threads

# Get all topics. Will be shown in topics.html.
def get_topics():
    result = db.session.execute(text("SELECT topic FROM topics"))
    topics = result.fetchall()
    topics = [topic[0] for topic in topics]
    topics = list(zip_longest(*(iter(topics), ) * 3)) # Convert list into list of 3-tuples
    return topics

# Verify that the file extension is supported. 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.ALLOWED_EXTENSIONS