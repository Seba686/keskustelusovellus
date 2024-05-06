from secrets import token_hex
from werkzeug.security import check_password_hash, generate_password_hash # Used for secure 
                                                                          # handling of passwords
from sqlalchemy import text # Required for SQL commands.
from flask import session
from db import db

# Check that correct credentials were given.
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

# Log user out.
def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]

# Register a new user.
def register(username, password, confirm_password):
    errors = verify_registration(username, password, confirm_password)
    if not errors:
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    return errors

# Verify register information.
def verify_registration(username, password, confirm_password):
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
    return errors

# Get user_id given a username.
def get_user_id(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username}).fetchone()
    return result

# Get username given a user_id.
def get_username(user_id):
    sql = text("SELECT username FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id}).fetchone()[0]
    return result
