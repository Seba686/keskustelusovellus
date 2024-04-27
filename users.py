from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from sqlalchemy import text
from db import db
from secrets import token_hex

def verify_login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        session["user_id"] = user.id
        session["csrf_token"] = token_hex(16)
        return True
    return False

def register(username, password, confirm_password):
    user = get_user_id(username)
    errors = []
    if user:
        errors.append("Käyttäjätunnus otettu.")
    if len(username) < 3:
        errors.append("Käyttäjätunnus on liian lyhyt.")
    if len(username) > 20:
        errors.append("Käyttäjätunnus on liian pitkä.")
    if password != confirm_password:
        errors.append("Salasanat eivät täsmää.")
    if len(password) < 8:
        errors.append("Salasana on liian lyhyt.")
    if len(password) > 100:
        errors.append("Salasanan enimmäispituus on 100 merkkiä.")
    if not errors:
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    return errors

def get_user_id(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user