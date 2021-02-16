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

@app.context_processor
def context_processor():
    return {
        "vendor": fn.config["vendor"],
    }

@app.route('/admin', methods=["GET", "POST"])
def admin_pages():
    print(x.request.args, '  request.args')
    # logout
    if "out" in x.request.args:
        x.session.pop("admin_logged", "")
        return x.redirect("/")

    if x.request.method == "POST" and x.request.form["action"] == "login":
        if x.request.form["password"] == fn.config["admin_password"]:
            x.session["admin_logged"] = int(time.time())
            return x.redirect('/admin')

        return x.render_template('admin/login.html', error=True)

    if time.time() - x.session.get("admin_logged", 0) > 24 * 3600:
        return x.render_template("admin/login.html")

    return x.render_template('admin/admin.html')

@app.route("/reset")
def reset():
    if x.request.host != "127.0.0.1:5000":
        return x.abort(404)

    res = "<pre>"
    # delete tables
    cur = db.postgres_db.cursor()
    cur.execute("SELECT TABLENAME FROM pg_tables where schemaname='public'")
    for t in cur.fetchall():
        cur.execute('DROP TABLE "%s"' % t)
    db.postgres_db.commit()

    db.postgres_db.create_tables([db.Product])

    # import yaml
    # with open(".site") as f:
    #     site = f.read().strip()
    # with open("site--%s/config.yaml" % site) as f:
    #     product_list = yaml.safe_load(f)["product_list"]

    # product_list_copy = []
    # for p in product_list:
    #     product_list_copy.append(p.copy())
    #     product_list_copy[-1].pop("code")
    #     product_list_copy[-1]["status"] = db.Product.ACTIVE
    # db.Product.insert_many(product_list_copy).execute()

    # res += "[+] Create model: Product: (%s)\n" % db.Product.select().count()
    return 'reset'


# main
@app.route("/", methods=["GET", "POST"])
def index():
    return x.render_template('login.html')

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
