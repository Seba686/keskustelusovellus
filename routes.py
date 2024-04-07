from flask import render_template, request, redirect, session, url_for

from app import app
import posts, users

@app.route("/")
def index():
    threads = posts.get_threads()
    return render_template("index.html", threads=threads) 

@app.route("/new_thread")
def new_thread():
    return render_template("new_thread.html")

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
    
@app.route("/new_comment", methods=["POST"])
def new_comment():
    thread_id = request.form["thread_id"]
    user_id = session["user_id"]
    content = request.form["content"]
    posts.new_comment(thread_id, user_id, content)
    return redirect(url_for("thread", id=thread_id))

@app.route("/thread/<int:id>")
def thread(id):
    thread = posts.get_thread(id)
    comments = posts.get_comments(id)
    return render_template("thread.html", thread=thread, comments=comments)