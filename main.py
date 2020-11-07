from flask import Flask, render_template, request, url_for, redirect,session

app = Flask(__name__) 

@app.route("/login",methods = ["POST","GET"])  
def home():
    if request.method == "POST":
        for i in request.form:
            print(i,type(request.form[i]))
        return render_template("form.html")
    else:
        return render_template("form.html") 

@app.route("/")
def mainpage():
    return render_template("index.html")

@app.route("/elements")
def elemntspage():
    return render_template("elements.html")

@app.route("/generic")
def masdfpage():
    return render_template("generic.html")
    
if __name__ == "__main__":
	app.run(debug = True)
