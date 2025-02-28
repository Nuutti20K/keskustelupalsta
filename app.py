import secrets
import sqlite3
from flask import Flask
from flask import abort, flash, render_template, request, redirect, session
import config
import threads
import messages
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
    all_threads = threads.get_threads()
    return render_template("index.html", threads=all_threads)

@app.route("/register")
def register():
    if "user_id" in session:
        abort(403)
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

@app.route("/thread/<int:thread_id>")
def show_thread(thread_id):
    thread = threads.get_thread(thread_id)
    if not thread:
        abort(404)
    classes = threads.get_classes(thread_id)
    thread_messages = messages.get_messages(thread_id)
    return render_template("show_thread.html", thread=thread, classes=classes, messages=thread_messages)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_threads = users.get_threads(user_id)
    user_messages = messages.get_messages(user_id)
    return render_template("show_user.html", user=user, threads=user_threads, messages=user_messages)

@app.route("/edit_thread/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):
    require_login()

    thread = threads.get_thread(thread_id)
    if not thread:
        abort(404)
    if thread["user_id"] != session["user_id"]:
        abort(403)
    
    if request.method == "GET":
        all_classes = threads.get_all_classes()
        classes = {}
        for my_class in all_classes:
            classes[my_class] = ""
        for entry in threads.get_classes(thread_id):
            classes[entry["title"]] = entry["value"]
        
        return render_template("edit_thread.html", thread=thread, classes=classes, all_classes=all_classes)
    
    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        if not title or len(title) > 50:
            abort(403)

        all_classes = threads.get_all_classes()

        classes = []
        for entry in request.form.getlist("classes"):
            if entry:
                class_title, class_value = entry.split(":")
                if class_title not in all_classes:
                    abort(403)
                if class_value not in all_classes[class_title]:
                    abort(403)
                classes.append((class_title, class_value))

        threads.update_thread(thread_id, title, classes)
        return redirect("/thread/" + str(thread_id))
    
@app.route("/edit_message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    require_login()

    message = messages.get_message(message_id)
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
        messages.update_message(message_id, content)
        return redirect("/thread/" + str(message["thread_id"]))
    
@app.route("/remove_thread/<int:thread_id>", methods=["GET", "POST"])
def remove_thread(thread_id):
    require_login()

    thread = threads.get_thread(thread_id)
    if not thread:
        abort(404)
    if thread["user_id"] != session["user_id"]:
        abort(403)
    
    if request.method == "GET":
        return render_template("remove_thread.html", thread=thread)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            threads.remove_thread(thread_id)
            return redirect("/")
        else:
            return redirect("/thread/" + str(thread_id))
        
@app.route("/remove_message/<int:message_id>", methods=["GET", "POST"])
def remove_message(message_id):
    require_login()

    message = messages.get_message(message_id)
    if not message:
        abort(404)
    if message["user_id"] != session["user_id"]:
        abort(403)
    
    if request.method == "GET":
        return render_template("remove_message.html", message=message)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            messages.remove_message(message_id)
        return redirect("/thread/" + str(message["thread_id"]))

@app.route("/new_thread", methods=["GET", "POST"])
def create_thread():
    require_login()

    if request.method == "GET":
        classes = threads.get_all_classes()
        return render_template("new_thread.html", classes=classes)
    
    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        if not title or len(title) > 50:
            abort(403)
        user_id = session["user_id"]

        all_classes = threads.get_all_classes()

        classes = []
        for entry in request.form.getlist("classes"):
            if entry:
                class_title, class_value = entry.split(":")
                if class_title not in all_classes:
                    abort(403)
                if class_value not in all_classes[class_title]:
                    abort(403)
                classes.append((class_title, class_value))

        threads.add_thread(title, user_id, classes)
        return redirect("/")

@app.route("/find_thread")
def find_thread():
    query = request.args.get("query")
    if query:
        results = threads.find_threads(query)
    else:
        query = ""
        results = []
    return render_template("find_thread.html", query=query, results=results)

@app.route("/create_message", methods=["POST"])
def create_message():
    require_login()
    check_csrf()

    content = request.form["content"]
    if not content or len(content) > 300:
        abort(403)
    thread_id = request.form["thread_id"]
    thread = threads.get_thread(thread_id)
    if not thread:
        abort(403)
    user_id = session["user_id"]

    messages.add_message(content, user_id, thread_id)
    return redirect("/thread/" + str(thread_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        abort(403)

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