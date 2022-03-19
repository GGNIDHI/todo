from flask import Flask
from flask import *

app=Flask(__name__)


@app.route("/index.html")

def index():
    return render_template('index.html')

@app.route("/layout.html")

def layout():
    return render_template("layout.html")

@app.route("/lists.html")

def lists():
    return render_template("lists.html")

@app.route("/tasks.html")
def tasks():
    return render_template("tasks.html")


if __name__=='__main__':
    app.run(debug=True)