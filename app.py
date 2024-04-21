from flask import Flask
from os import getenv

UPLOAD_FOLDER = "./static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["MAX_CONTENT_LENGTH"] = 4 * 1000 * 1000 #TODO: add error handling

import routes