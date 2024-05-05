from db import db
from sqlalchemy.sql import text # Required for SQL commands.

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

# Get all topics. Will be shown in topics.html.
def get_topics():
    result = db.session.execute(text("SELECT topic FROM topics"))
    topics = result.fetchall()
    topics = [topic[0] for topic in topics]
    return topics

# Get topic and topic_id.
def get_topic(topic):
    sql = text("SELECT id, topic FROM topics WHERE topic=:topic")
    result = db.session.execute(sql, {"topic":topic}).fetchone()
    return result

# Subscribe or unsubscribe to a topic.
def toggle_subscription(topic_id, user_id):
    # Upsert operation. Flip the boolean of subscribed if (user, topic) pair is already inserted.
    sql = text("INSERT INTO subscriptions (topic_id, user_id, subscribed) \
               VALUES (:topic_id, :user_id, true) \
               ON CONFLICT (topic_id, user_id) DO UPDATE \
               SET subscribed = NOT subscriptions.subscribed")
    db.session.execute(sql, {"topic_id": topic_id, "user_id": user_id})
    db.session.commit()

# Get number of users subscribed to a topic.
def get_subscriber_count(topic_id):
    sql = text("SELECT COUNT(id) FROM subscriptions WHERE topic_id=:id \
               AND subscribed = TRUE")
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()[0]

# Check if user is subscribed to a topic.
def subscribed(topic_id, user_id):
    sql = text("SELECT COALESCE((SELECT subscribed FROM subscriptions \
               WHERE topic_id=:topic_id AND user_id=:user_id), FALSE)")
    result = db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id})
    return result.fetchone()[0]

# Get number of topics a user is subscribed to.
def get_topic_count(user_id):
    sql = text("SELECT COUNT(id) FROM subscriptions WHERE \
               user_id=:user_id AND subscribed = TRUE")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]