from os import getenv
from flask import Flask

UPLOAD_FOLDER = "./static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["MAX_CONTENT_LENGTH"] = 4 * 1000 * 1000

import routes
