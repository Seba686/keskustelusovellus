from flask import render_template, request, redirect, session, url_for, abort

from app import app
import posts, users

@app.route("/")
def index():
    threads = posts.get_threads()
    return render_template("index.html", threads=threads) 

@app.route("/new_thread", methods=["GET", "POST"])
def new_thread():
    if "username" not in session:
        return render_template("error.html")
    topics = posts.get_topics()
    if request.method == "GET":
        return render_template("new_thread.html", topics=topics)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    topic = request.form["topic"]
    user_id = session["user_id"]
    title = request.form["title"]
    content = request.form["content"]
    if "image" in request.files:
        image = request.files["image"]
    else:
        image = None
    status = posts.new_thread(topic, user_id, title, content, image)
    if not status[0]:
        return redirect(url_for("thread", id=status[1]))
    return render_template("new_thread.html", title=title, content=content, errors=status[0], topics=topics)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)
    username = request.form["username"]
    password = request.form["password"]
    if users.verify_login(username, password):
        return redirect("/") # TODO redirect to previous page
    return render_template("login.html", error=True)
        
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
        
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", get=True)
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
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        thread_id = request.form["thread_id"]
        user_id = session["user_id"]
        comment_content = request.form["content"]
        errors = posts.new_comment(thread_id, user_id, comment_content)
    thread = posts.get_thread(id)
    comments = posts.get_comments(id)
    comment_count = posts.get_comment_count(id)
    return render_template("thread.html", thread=thread, comments=comments,
                           errors=errors, comment_content=comment_content,
                           comment_count=comment_count)

@app.route("/topic/<string:topic>")
def topic(topic):
    threads = posts.get_threads_by_topic(topic)
    return render_template("topic.html", threads=threads, topic=topic)

@app.route("/topics", methods=["GET", "POST"])
def topics():
    errors = None
    if request.method =="POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        topic = request.form["topic"]
        errors = posts.new_topic(topic)
    topics = posts.get_topics()
    return render_template("topics.html", errors=errors, topics=topics)
