from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from sqlalchemy import text
from db import db

def verify_login(username, password):
    sql = text("SELECT password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        return True
    return False

def register(username, password, confirm_password):
    # TODO: refactor this
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        return "käyttäjätunnus otettu"
    if len(username) < 3:
        return "käyttäjätunnus on liian lyhyt"
    if len(username) > 20:
        return "käyttäjätunnus on liian pitkä"
    if password != confirm_password:
        return "salasanat eivät täsmää"
    if len(password) < 8:
        return "salasana on liian lyhyt"
    if len(password) > 100:
        return "salasana on liian pitkä"
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return "success"