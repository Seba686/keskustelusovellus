from itertools import zip_longest
from flask import render_template, request, redirect, session, url_for, abort
from app import app
import posts, users, topic_handler

@app.route("/")
def index():
    threads = posts.get_threads()
    return render_template("index.html", threads=threads) 

@app.route("/new_thread", methods=["GET", "POST"])
def new_thread():
    if "username" not in session:
        return render_template("error.html")
    topics = topic_handler.get_topics()
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
    return render_template("new_thread.html", title=title, content=content,
                           errors=status[0], topics=topics)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)
    username = request.form["username"]
    password = request.form["password"]
    if users.verify_login(username, password):
        return redirect("/")
    return render_template("login.html", error=True)
        
@app.route("/logout")
def logout():
    users.logout()
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
    subscriber_count = topic_handler.get_subscriber_count(thread.topic_id)
    if "username" in session:
        subscribed = topic_handler.subscribed(thread.topic_id, session["user_id"])
    else:
        subscribed = False
    return render_template("thread.html", thread=thread, comments=comments,
                           errors=errors, comment_content=comment_content,
                           comment_count=comment_count, subscriber_count=subscriber_count,
                           subscribed=subscribed)

@app.route("/topic/<string:topic>")
def topic(topic):
    threads = posts.get_threads_by_topic(topic)
    topic_id = topic_handler.get_topic(topic)
    subscriber_count = topic_handler.get_subscriber_count(topic_id.id)
    if "username" in session:
        subscribed = topic_handler.subscribed(topic_id.id, session["user_id"])
    else:
        subscribed = False
    return render_template("topic.html", threads=threads, topic=topic,
                           topic_id=topic_id.id, subscriber_count=subscriber_count,
                           subscribed=subscribed)

@app.route("/topics", methods=["GET", "POST"])
def get_topics():
    errors = None
    if request.method =="POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        topic = request.form["topic"]
        errors = topic_handler.new_topic(topic)
    topics = topic_handler.get_topics()
    topics = list(zip_longest(*(iter(topics), ) * 3)) # Convert list into list of 3-tuples
    return render_template("topics.html", errors=errors, topics=topics)

@app.route("/toggle_subscription", methods=["POST"])
def toggle_subscription():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    topic_id = request.form["topic"]
    user_id = request.form["user"]
    topic_handler.toggle_subscription(topic_id, user_id)
    return redirect(request.referrer)

@app.route("/home")
def home():
    if "username" not in session:
        return render_template("error.html")
    threads = posts.get_home_posts(session["user_id"])
    topic_count = topic_handler.get_topic_count(session["user_id"])
    return render_template("home.html", threads=threads, topic_count=topic_count)

@app.route("/profile/<int:user_id>/threads")
def profile_threads(user_id):
    threads = posts.get_user_threads(user_id)
    username = users.get_username(user_id)
    return render_template("profile.html", threads=threads, is_thread=True,
                           user_id=user_id, username=username)

@app.route("/profile/<int:user_id>/comments")
def profile_comments(user_id):
    comments = posts.get_user_comments(user_id)
    username = users.get_username(user_id)
    return render_template("profile.html", comments=comments, is_thread=False,
                           user_id=user_id, username=username)