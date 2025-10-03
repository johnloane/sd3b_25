from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)

_ = load_dotenv(find_dotenv())
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")

mysql = MySQL(app)



SPORTS = ["Fencing", "Airsoft"]


@app.route("/")
def index():
    return render_template("index.html", sports = SPORTS)


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    if not name: 
        return render_template("failure.html", message="You did not enter a name")
    sport = request.form.get("sport")
    if not sport:
        return render_template("failure.html", message="You did not enter a sport")
    if sport not in SPORTS:
        return render_template("failure.html", message="Please do not try to hack our html")
    
    cursor = mysql.connection.cursor()
    # Check is this name and sport already exists in the database
    # If it already exists don't add it again
    cursor.execute("select * from registrant where name=%s and sport=%s", (name, sport))
    rv = cursor.fetchall()
    print(len(rv))
    if(len(rv) == 0):
        cursor.execute("insert ignore into registrant(name, sport) values(%s, %s)", (name, sport))
        mysql.connection.commit()
    else:
        print("That name and sport are already registered")
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    cursor = mysql.connection.cursor()
    cursor.execute("select * from registrant")
    rv = cursor.fetchall()
    return render_template("registrants.html", registrants = rv)


@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    if id:
        cursor = mysql.connection.cursor()
        cursor.execute("delete from registrant where id=%s", id)
        mysql.connection.commit()
    return redirect("/registrants")
    