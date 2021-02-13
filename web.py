import datetime
import json
import logging
import time

import yaml

import flask as x
import utils as fn

import models as db

# Configuration
logging.root.level = logging.INFO

app = x.Flask(__name__, static_folder="static")
app.secret_key = fn.config["secret_key"]
app.logger = logging.root
app.jinja_options = {
    "line_comment_prefix": "#:",
    "extensions": ["jinja2.ext.autoescape", "jinja2.ext.with_", "jinja2.ext.loopcontrols"],
}


@app.before_request
def before_request():
    # check not admin page
    if not x.request.path.startswith("/admin/"):
        return

    # check login
    if time.time() - x.session.get("admin_logged", 0) > 24 * 3600:
        return x.redirect("/admin")

    return


# reset
@app.route("/reset")
def my_reset():
    new_data = db.Product()
    new_data.title = "Түм"
    new_data.price = 10000
    new_data.description = "Ахуй хэрэглээний бараа"
    new_data.status = db.Product.ACTIVE
    new_data.save()
    neg = db.Product.select().count()
    return f"this is {neg}"
    # return 'reset'


# main
@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello Sudar congratulations"

# static
@app.route("/favicon.ico")
def favicon_ico():
    return x.send_file("static/favicon/favicon.ico")


@app.route("/favicon.png")
def favicon_png():
    return x.send_file("static/favicon/favicon.png")


@app.route("/robots.txt")
def robots_txt():
    # debt: allow robots after changed personal bank account
    response = x.make_response("User-agent: * Disallow: /")
    response.headers["Content-Type"] = "text/plain"
    return response
