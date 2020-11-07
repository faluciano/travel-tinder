from flask import Flask, render_template, request, url_for, redirect,session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
import googlemaps
app = Flask(__name__) 
seckey = os.urandom(12)
app.secret_key=seckey
app.permanent_session_lifetime = timedelta(minutes = 5)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    def __init__(self,email,name,password):
        self.email = email
        self.name = name
        self.password = password

@app.route("/login",methods = ["POST","GET"])  
def login():
    if "login" in session and session["login"] == True:
        return redirect(url_for("mainpage"))
    if request.method == "POST":
        session["login"] = True
        app.permanent = True
        return  redirect(url_for("mainpage"))
    else:
        return render_template("form.html")

@app.route("/logout")
def logout():
    session["login"] = False
    return redirect(url_for("mainpage"))

@app.route("/register",methods = ["POST","GET"])  
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        return render_template("register.html")
    else:
        return render_template("register.html") 

@app.route("/")
def mainpage():
    return render_template("index.html")
'''
@app.route("/generic")
def masdfpage():
    return render_template("generic.html")
'''
if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
