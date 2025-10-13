from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

_ = load_dotenv(find_dotenv())
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")

mysql = MySQL(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"]) 
def login():
    if request.method == "POST":
        # Remember that user has logged in
        # Redirect to /
        # Is the user in the database
        email = request.form.get("email")
        password = request.form.get("password")
        cursor = mysql.connection.cursor()
        
        cursor.execute("select password from user where email=%s", (email,))
        rv = cursor.fetchall()
        db_password = rv[0][0]
        #print(db_password)
        if(check_password_hash(db_password, password)):
            session["email"] = email
            return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))
        cursor = mysql.connection.cursor()
        cursor.execute("insert into user(email, password) values(%s, %s)", (email, password))
        mysql.connection.commit()
        return redirect("/")
    else:
        return render_template("register.html")