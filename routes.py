from flask import render_template, request, redirect, url_for
from sqlalchemy.sql import text

from app import app
import posts

@app.route("/")
def index():
    threads = posts.show_threads()
    return render_template("index.html", threads=threads) 

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    title = request.form["title"]
    posts.new_thread(title, content)
    return redirect("/")