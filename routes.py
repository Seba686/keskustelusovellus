from flask import render_template, request, redirect, url_for
from sqlalchemy.sql import text

from app import app
from db import db
@app.route("/")
def index():
    result = db.session.execute(text("SELECT id, title, content, created FROM threads ORDER BY created DESC"))
    threads = result.fetchall()
    return render_template("index.html", threads=threads) 

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    title = request.form["title"]
    sql = text("INSERT INTO threads (title, content, created) VALUES (:title, :content, NOW())")
    db.session.execute(sql, {"title":title, "content":content})
    db.session.commit()
    return redirect("/")