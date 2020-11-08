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
    preferences = db.Column(db.String(100),default ="") #places saved
    def __init__(self,email,name,password):
        self.email = email
        self.name = name
        self.password = password
    @property
    def preferences(self):
        return [str(x) for x in self.preferences.split(";")]
    @preferences.setter
    def preferences(self,val):
        self.preferences += ";" +str(val)
'''
@app.route("/preferences",methods = ["POST","GET"])  
def preferences():
    if "login" in session and session["login"] == True:
        return redirect(url_for("mainpage"))
    if request.method == "POST":
        return  redirect(url_for("mainpage"))
    else:
        return render_template("preferences.html")
'''
@app.route("/login",methods = ["POST","GET"])  
def login():
    if "login" in session and session["login"] == True:
        return redirect(url_for("generic"))
    if request.method == "POST":
        q = users.query.filter_by(email = request.form["email"]).first()
        if q and q.password == request.form["password"]:
            
            session["login"] = True
            session["name"] = q.name
            app.permanent = True
            redirect(url_for("generic"))
        return  redirect(url_for("login"))
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
        name = request.form["name"]
        password = request.form["password"]
        found_user = users.query.filter_by(email = email).first()
        if not found_user:
            usr = users(email,name,password)
            db.session.add(usr)
            db.session.commit()
            session["login"] = True
            session["name"] = name
            return redirect(url_for("login"))
        return redirect(url_for("register.html"))
    else:
        return render_template("register.html") 

@app.route("/")
def mainpage():
    return render_template("index.html")
@app.route("/allusers")
def use():
    m = users.query.all()
    x = ""
    for user in m:
        print(user)
    return "d"

@app.route("/generic",methods = ["POST","GET"])
def generic():
    name = "dude"
    if "name" in session:
        name = session["name"]
    return render_template("generic.html",name = name)

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
