from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return render_template("greet.html", name=request.form.get("name")) 



# @app.route("/greet", methods=["POST"])
# def greet():
#     return render_template("greet.html", name=request.form.get("name"))

