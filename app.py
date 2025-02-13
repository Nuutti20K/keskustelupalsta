import secrets
import sqlite3
from flask import Flask
from flask import abort, flash, render_template, request, redirect, session
import config
import items
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat!")
        return redirect("/register")
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")
    
    return redirect("/")

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    messages = items.get_messages(item_id)
    return render_template("show_item.html", item=item, messages=messages)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_items = users.get_items(user_id)
    user_messages = users.get_messages(user_id)
    return render_template("show_user.html", user=user, items=user_items, messages=user_messages)

@app.route("/edit_item/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    
    if request.method == "GET":
        return render_template("edit_item.html", item=item)
    
    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        if not title or len(title) > 50:
            abort(403)
        items.update_item(item_id, title)
        return redirect("/item/" + str(item_id))
    
@app.route("/edit_message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    require_login()

    message = items.get_message(message_id)
    if not message:
        abort(404)
    if message["user_id"] != session["user_id"]:
        abort(403)
    
    if request.method == "GET":
        return render_template("edit_message.html", message=message)
    
    if request.method == "POST":
        check_csrf()
        content = request.form["content"]
        if not content or len(content) > 300:
            abort(403)
        items.update_message(message_id, content)
        return redirect("/item/" + str(message["item_id"]))
    
@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    
    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
        
@app.route("/remove_message/<int:message_id>", methods=["GET", "POST"])
def remove_message(message_id):
    require_login()

    message = items.get_message(message_id)
    if not message:
        abort(404)
    if message["user_id"] != session["user_id"]:
        abort(403)
    
    if request.method == "GET":
        return render_template("remove_message.html", message=message)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_message(message_id)
        return redirect("/item/" + str(message["item_id"]))

@app.route("/new_item", methods=["GET", "POST"])
def create_item():
    require_login()

    if request.method == "GET":
        return render_template("new_item.html")
    
    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        if not title or len(title) > 50:
            abort(403)
        user_id = session["user_id"]

        items.add_item(title, user_id)
        return redirect("/")

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/create_message", methods=["POST"])
def create_message():
    require_login()
    check_csrf()

    content = request.form["content"]
    if not content or len(content) > 300:
        abort(403)
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    items.add_message(content, user_id, item_id)
    return redirect("/item/" + str(item_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        del session["csrf_token"]
    return redirect("/")