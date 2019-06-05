import os
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    url_for,
    request,
    session,
    abort,
)
from flask_pymongo import PyMongo
import pprint
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
    UserMixin,
)

import datetime
import isotime

# A user class from a previous version of things
# class User(object):
#     def __init__(self, email, username, password):
#         self.email = email
#         self.username = username
#         self.set_password(password)

#     def set_password(self, password):
#         self.pw_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.pw_hash, password)


# Temp method to load MONGO_URI without committing it to Github, this
# should be added to the path of the Heroku app later
# with open("MONGO_URI.txt", "r") as myfile:
#     uri = myfile.readlines()[0]


# Setting up Flask and PyMongo
app = Flask(__name__)
app.config.from_envvar("COOKBOOK_CONFIG")

# From a defferent attempt to log in users
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"  # the login view of your application
# # app.config['SECRET_KEY'] = "lkkajdghdadkglajkgah" # a secret key for
# # your app

mongo = PyMongo(app)

# Home Page - Under construction
@app.route("/")
def home():
    return render_template("hello.html")


# Login Page
@app.route("/login")
def login():
    print("logged and loaded")
    return render_template("login.html")


# Route to deal with login form
@app.route("/postlogin", methods=["POST"])
def postlogin():

    # Find email in database
    val = mongo.db.users.find_one({"email": request.form["loginEmail"]})

    # If email and password are in database
    if val and check_password_hash(val["pass_hash"], request.form["loginPassword"]):
        session["logged_in"] = True
        session["username"] = val["username"]
        print(session)
        return redirect(url_for("home"))
    # else if email was correct
    elif val:
        flash("Your password is incorrect")
        return redirect(url_for("login"))
    else:
        flash("Your email is incorrect")
        return redirect(url_for("login"))


# Route to log user out
@app.route("/logout")
def logout():
    session["logged_in"] = False
    session.pop("username", None)
    return redirect(url_for("home"))


# User Page - under construction
@app.route("/user")
def user():
    print(mongo.db.users.find_one())
    return render_template("user.html")


# Signup Page
@app.route("/signup")
def signup():
    return render_template("signupform.html")


# Route to deal with signup form
@app.route("/postsignup", methods=["POST"])
def postsignup():

    # Invalid charecters
    invalid = '[,/<>{}]" '
    # Create a dict of the form input
    formval = request.form.to_dict()
    # Force certain values to be lowercase
    formval["email"] = formval["email"].lower()
    formval["username"] = formval["username"].lower()
    # Boolean flag to check if the inputs are valid
    valid = True

    # Check if the usre inputs are valid
    if "@" not in formval["email"]:
        flash("Please enter a valid email")
        valid = False
    if 8 > len(formval["username"]):
        flash("Your username is too short")
        valid = False
    if 8 > len(formval["password"]):
        flash("Your password too short")
        valid = False
    if any(x in invalid for x in formval["username"]):
        flash("Only use letters, numbers and underscores in your username")
        valid = False

    # Check the username or email have not already been used
    if mongo.db.users.find_one({"username": formval["username"]}):
        flash("User name is already taken")
        valid = False

    if mongo.db.users.find_one({"email": formval["email"]}):
        flash(
            "You have already signed up with this email, if you have "
            "forgotten your login details then you can get in touch using "
            "the link at the end of the page"
        )
        valid = False

    # If all the checks have been passed the password is hashed, the
    # user details are added and the user logged in
    if valid is True:
        formval["pass_hash"] = generate_password_hash(formval["password"])
        del formval["password"]
        mongo.db.users.insert_one(formval)
        session["logged_in"] = True
        session["username"] = formval["username"]
        return redirect(url_for("home"))
    else:
        return redirect(url_for("signup"))


# Recipe Submission Page
# Still needs to pull data from databases
@app.route("/submitrecipe")
def submitrecipe():
    print(session)
    print(session.keys())
    if ("logged_in" in session.keys()) and (session["logged_in"] is True):
        print("Load page")
        return render_template(
            "recipeform.html",
            key=app.config["GOOGLE_API_KEY"],
            cx=app.config["GOOGLE_CX"],
        )
    else:
        flash("Please log in before posting a recipe")
        return redirect(url_for("login"))


# Recipe posting route - handles the form data
@app.route("/postrecipe", methods=["POST"])
def postrecipe():
    # Todays date
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    print(request.form)

    # Pulling out values with multiple inputs into lists
    typelist = request.form.getlist("rform-type")
    cuislist = request.form.getlist("rform-cuisine")
    ingrlist = request.form.getlist("rform-ingredient")
    quanlist = request.form.getlist("rform-quantity")
    unitlist = request.form.getlist("rform-unit")
    steplist = request.form.getlist("rform-step")
    utenlist = request.form.getlist("rform-utensils")

    # Convert time to ISO 8601 format
    tprep = isotime.converttime(request.form["rformTprep"])
    tcook = isotime.converttime(request.form["rformTcook"])
    tadd = isotime.addtime(request.form["rformTprep"], request.form["rformTcook"])

    # 'Zipping' the ingredients into a list and a list of dictionaries
    ingrdictlist = []
    ingrfulllist = []
    for i in range(len(ingrlist)):
        ingrdictlist.append(
            {"name": ingrlist[i], "quantity": quanlist[i], "unit": unitlist[i]}
        )
        ingrfulllist.append(quanlist[i] + " " + unitlist[i] + " " + ingrlist[i])

    # 'Zipping' the steps into Schema dictionaries
    for i in range(len(steplist)):
        steplist[i] = {"@type": "HowToStep", "text": steplist[i]}

    # Gathering the recipe dictionary
    recipe = {
        # Schema Values
        "@context": "https://schema.org/",
        "@type": "Recipe",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 0,
            "reviewCount": 0,
        },
        "author": "",  # Not exactly sure how this will work...
        "comment": [],
        "cookTime": tcook,
        "datePublished": today,
        "description": request.form["rformDescription"],
        "image": {
            "@type": "ImageObject",
            "url": "",  # This still needs to be implemented
            "height": 200,
            "width": 200,
        },
        "name": request.form["rform-title"],
        "prepTime": tprep,
        "recipeCategory": typelist,
        "recipeCuisine": cuislist,
        "recipeIngredient": ingrfulllist,
        "recipeInstructions": steplist,
        "recipeYield": request.form["rform-serving"],
        "totalTime": tadd,
        # My Values
        "ingredientdict": ingrdictlist,
        "utensils": utenlist,
        "notes": request.form["rformNotes"],
    }

    print(recipe)

    # Currently redirects to the submission page, should redirect to the users
    # recipe page
    return redirect(url_for("home"))


# Junk Routes
# @app.route('/get_users')
# def get_users():
#     users = mongo.db.users.find()
#     return render_template("test.html", tasks=users)

# @app.route('/ingredient')
# def ingredient():
#     return render_template("ingredient.html")

# @app.route('/search')
# def search():
#     recipes = mongo.db.recipes.find()
#     return render_template("search.html", recipes=recipes)


# Main loop - will need to be changed when hosting on Heroku
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host="0.0.0.0", port="8080", debug=True)
