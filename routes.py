from flask import render_template, request, redirect, session, url_for

from app import app
import posts, users

@app.route("/")
def index():
    threads = posts.get_threads()
    return render_template("index.html", threads=threads) 

@app.route("/new_thread", methods=["GET", "POST"])
def new_thread():
    if request.method == "GET":
        return render_template("new_thread.html")
    else:
        user_id = session["user_id"]
        title = request.form["title"]
        content = request.form["content"]
        status = posts.new_thread(user_id, title, content)
        if not status[0]:
            return redirect(url_for("thread", id=status[1]))
        else:
            return render_template("new_thread.html", title=title, content=content, errors=status[0])


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
        return render_template("register.html", get=True)
    else:
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        errors = users.register(username, password, confirm_password)
        return render_template("register.html", errors=errors)

@app.route("/thread/<int:id>", methods=["GET", "POST"])
def thread(id):
    errors = None
    comment_content = None
    if request.method == "POST":
        thread_id = request.form["thread_id"]
        user_id = session["user_id"]
        comment_content = request.form["content"]
        errors = posts.new_comment(thread_id, user_id, comment_content)
    thread = posts.get_thread(id)
    comments = posts.get_comments(id)
    comment_count = posts.get_comment_count(id)
    return render_template("thread.html", thread=thread, comments=comments, \
                           errors=errors, comment_content=comment_content, comment_count=comment_count)