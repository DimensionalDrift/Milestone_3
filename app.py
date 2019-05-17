import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Temp method to load MONGO_URI without commiting it to Github, this should be added to the path of the Heroku app later
with open ("MONGO_URI.txt", "r") as myfile:
    uri=myfile.readlines()[0]

print (uri)

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'cookbook'
app.config["MONGO_URI"] = uri

mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/get_users')
def get_users():
    users = mongo.db.users.find()
    return render_template("test.html", tasks=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port='8080',
            debug=True)