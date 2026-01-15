
import re
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
# enable flashing
app.secret_key = "supper_secret_key_here"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# configure session lifetime
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days= 30)
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///plant.db")

#insure any storge is deleted
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["POST", "GET"])
def index():
    plants= db.execute("SELECT * FROM plants")
    return render_template("index.html", plants=plants)

@app.route("/login", methods=["POST","GET"])
def login():
    # if user want to login
    if request.method == "GET":
        return render_template("login.html",header="تسجيل الدخول")
    # user sent the form
    username = request.form.get("username")
    password = request.form.get("password")
    if not username :
        flash("الرجاء ادخال اسم المستخدم","danger")
        return redirect("/login")
    if not password :
        flash("الرجاء ادخال كلمة المرور","danger")
        return redirect("/login")
    rows = db.execute("SELECT * FROM users WHERE username = ?",username)
    if len(rows) != 1:
        flash("اسم المستخدم هذا غير موجود","danger")
        return redirect("/login")
    if not check_password_hash(rows[0]["hash"], password):
        flash("اسم المستخدم او كلمة السر غير صحيحة","danger")
        return redirect("/login")
    session["user_id"] = rows[0]["hash"]
    return redirect("/")


@app.route("/logout")
def logout():
    # forget the user
    session.clear()
    return redirect("/")


@app.route("/register" ,methods=["POST", "GET"])
def register():
    # get the registration form
    if request.method == "GET":
        return render_template("register.html")
    # ensure passwords are the same
    if request.form.get("p1") != request.form.get("p2"):
        flash("الرجاء ادخال كلمات سر متطابقة", "danger")
        return redirect("/register")
    username = request.form.get("username")
    password = request.form.get("p1")
    # ensure username field is not blanked
    if not username:
        flash("الرجاء ادخال اسم مستخدم","danger")
        return redirect("/register")
    #ensure password is avialble
    if not password:
        flash("الرجاء ادخال كلمة المرور", "danger")
        return redirect("/register")
    #restrict username to English
    if not re.match("^[A-Za-z0-9]+$",username):
        flash("يجب ان يكون اسم المستخدم بالانجليزية فقط","danger")
        return redirect("/register")
    #restrict password to English
    if not re.match("^[A-Za-z0-9]+$",password):
        flash("يجب ان تكون كلمة المرور بالانجليزية فقط","danger")
        return redirect("/register")
    #ensure password at least 8 characters
    if len(password) < 8:
        flash("يجب ان تكون كلمة المرور على الاقل ثمانية احرف","danger")
        return redirect("/register")
    rows = db.execute("SELECT username FROM users WHERE username = ?", username)
    if len(rows) != 0:
        flash("اسم المستخدم هذا محجوز أختر اسما اخر","danger")
        return redirect("/register")
    db.execute("INSERT INTO users('username', 'hash') VALUES (?, ?)",username, generate_password_hash(password))
    rows = db.execute("SELECT id FROM users WHERE username = ?", username)
    session["user_id"] = rows[0]["id"]
    return redirect("/")

@app.route("/cart" ,methods=["POST", "GET"])
def cart():
    # ensure the user is already logged in
    if "user_id" not in session:
        return redirect("/login")
    # ensure session is permanent
    session.permanent = True
    # ensure there is a cart
    if "cart" not in session:
        session["cart"] = []
    if request.method == "GET":
        plants = db.execute("SELECT DISTINCT * FROM plants WHERE id IN (?)",session["cart"])
        return render_template("cart.html", header="عربة التسوق", plants=plants)

    # save the items in the cart session
    if "add" in request.form:
        if (request.form.get("add")) not in session["cart"]:
            session["cart"].append(request.form.get("add"))
            return redirect("/cart")
    # remove the item from the cart
    elif "remove" in request.form:
        session["cart"].remove(request.form.get("remove"))
        return redirect("/cart")

