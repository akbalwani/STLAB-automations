import json
from flask import Flask, redirect, url_for, request, render_template, session
app = Flask(__name__)
app.secret_key = "somekey"

team = ["abhaggarwal@axway.com", "akksharma@axway.com", "akbalwani@axway.com", "chmseth@axway.com", "dsharma@axway.com", "djhamb@axway.com", "gchaturvedi@axway.com", "hparveen@axway.com", "jchaudhary@axway.com",
        "laanand@axway.com", "mosharjil@axway.com", "ngautam@axway.com", "nitgoel@axway.com", "nuniyal@axway.com", "pbishnoi@axway.com", "rchaudhary@axway.com", "sakumar2@axway.com", "sbohra@axway.com", "ssinghkarki@axway.com"]

parent_dir = "C:\\Users\\akbalwani\\Desktop\\test\\License-automation\\jsonfiles"


@app.route('/check')
def check_login():
    if "logged_user" in session:
        # print(session["logged_user"])
        return session['logged_user']
        # return f"{session['logged_user']}"
    else:
        return 5


@app.route('/')
@app.route('/home')
def home():
    if check_login() == 5:
        return "<p>not logged in , please login </p> "

    else:
        return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form["uname"]
        paswd = request.form["psw"]
        if user in team and paswd == user:
            # return f"this {user} is in support team"
            # return render_template("data-collector.html", user=user)
            session["logged_user"] = user
            return redirect(url_for("user"))
        else:
            return "<h1> Not a part of team </h1>"
    else:
        return render_template("login.html")


@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == "POST" and check_login() != 5:
        user_data = {}
        host = request.form['server-ip']
        username = request.form['server-user']
        password = request.form['server-pass']
        port = request.form['server-port']
        path = request.form['server-path']
        st_type = request.form['st_type']
        user_data = {'host': host, 'username': username,
                     'password': password, 'port': port, 'path': path, 'st_type': st_type}

        with open(parent_dir+"\\response.json", 'r+') as file:
            file_data = json.load(file)
            file_data["servers"].append(user_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

        return render_template("success.html", message=user_data)
    else:
        if check_login() == 5:
            return "not logged in"
        else:
            return render_template("data-collector.html", user=session['logged_user'])


if __name__ == '__main__':
    app.run(debug=True)
