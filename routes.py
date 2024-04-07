from flask import render_template, request, redirect, session

from app import app
import posts, users

@app.route("/")
def index():
    threads = posts.get_threads()
    return render_template("index.html", threads=threads) 

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    user_id = session["user_id"]
    title = request.form["title"]
    content = request.form["content"]
    posts.new_thread(user_id, title, content)
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)
    else:
        username = request.form["username"]
        password = request.form["password"]
        if users.verify_login(username, password):
            return redirect("/") #TODO redirect to previous page
        else:
            return render_template("login.html", error=True)
        
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
        
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        status = users.register(username, password, confirm_password)
        return render_template("register.html", status=status)