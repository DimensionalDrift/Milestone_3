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
from bson.json_util import dumps
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

# Recipe Blank
# I should probably use a recipe class to handle the recipe in python but for the minute this should do
recipeblank = {
    # Schema Values
    "@context": "https://schema.org/",
    "@type": "Recipe",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": 0.0,
        "reviewCount": 0,
    },
    "author": "",
    "comments": [],
    "cookTime": "",
    "datePublished": "",
    "description": "",
    "image": {"@type": "ImageObject", "url": "", "height": 0, "width": 0},
    "name": "",
    "prepTime": "",
    "recipeCategory": [],
    "recipeCuisine": [],
    "recipeIngredient": [],
    "recipeInstructions": [],
    "recipeYield": "",
    "totalTime": "",
    # My Values
    "ingredientdict": [],
    "utensils": [],
    "notes": "",
}

# Function to add values to list tables that store lists of categories,
# ingredients etc.
def addto_listtable(table, vallist):
    for item in vallist:
        entry = mongo.db[table].find_one({"name": item})
        # If the entry in the table exists increment its number by one
        if entry:
            add = entry["number"] + 1
            mongo.db[table].update(entry, {"$set": {"number": add }})
        # Otherwise create an entry
        else:
            new_entry = {"name": item, "number": 1}
            mongo.db[table].insert_one(new_entry)


# Function to handle making lists of form inputs that have multiple values, each of the entries are also converted to title case by default, setting the flag title to False will bypass that step
def formlister(table, form, key, title=True):
    # Create list
    flist = form.getlist(key)

    # If the flag is set, make each entry title case, making everything
    # title case might not make sense for everything but it will make
    # for less duplicates, I'll come up with a better solution later
    if title:
        for i in range(len(flist)):
            flist[i] = flist[i].title()

    # Add the values to mongodb tables
    addto_listtable(table, flist)

    return flist


# Function checks if a recipe is in a users list of favourites
def likecheck(rid):
    if "logged_in" in session and session["logged_in"] is True:
        userfav = mongo.db.users.find_one({"email": session["email"]})
        if rid in userfav["favourites"]:
            return True

    return False


# This loads all the lists of list tables into memeory, might not be a great idea but I can't think of another way to pass these into the select2 lists... .sort({"number": -1})
def dblistload():

    # Load the lists with the database entries
    categories = list(mongo.db.categories.find())
    cuisines = list(mongo.db.cuisines.find())
    ingredients = list(mongo.db.ingredients.find())
    units = list(mongo.db.units.find())
    utensils = list(mongo.db.utensils.find())

    # Load only the names from the database
    categories = [d["name"] for d in categories]
    cuisines = [d["name"] for d in cuisines]
    ingredients = [d["name"] for d in ingredients]
    units = [d["name"] for d in units]
    utensils = [d["name"] for d in utensils]

    return categories, cuisines, ingredients, units, utensils


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

if "DEPLOYED" in os.environ:
    app.config["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")
    app.config["GOOGLE_CX"] = os.environ.get("GOOGLE_CX")
    app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    app.config["IP"] = os.environ.get("IP")
    app.config["PORT"] = os.environ.get("PORT")

    debug = False
else:
    app.config.from_envvar("COOKBOOK_CONFIG")
    debug = True


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
    # temp = "cuisines"
    # addto_listtable(temp, ["French"])
    # print(mongo.db[temp].find_one())
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
        session["id"] = str(val["_id"])
        session["email"] = val["email"]
        return redirect(url_for("user", username=session["username"]))
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
    session.pop("email", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("home"))


# User Page
@app.route("/user/<username>")
@app.route("/user/<username>/<view>")
def user(username, view="submitted"):

    # If the user is not logged in at all
    if "username" not in session.keys():
        flash("Please log in to see your user profile")
        return redirect(url_for("login"))

    # If the user tries to view a profile that they are not logged in as
    if username != session["username"]:
        flash("You are not logged in as this user")
        return redirect(url_for("login"))

    recipes = mongo.db.recipes.find({"author": session["username"]})
    user = mongo.db.users.find_one({"username": session["username"]})

    # Create a list of the favourites recipes
    favourites = []
    for rid in user["favourites"]:
        favourites.append(mongo.db.recipes.find_one({"_id": ObjectId(rid)}))

    # Create a list of the comment tuples, the first item of the list is the comment, the second is the recipe itself
    commentdata = []
    for cid in user["comments"]:
        comment = mongo.db.comments.find_one({"_id": ObjectId(cid)})
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(comment["recipe_id"])})
        commentdata.append((comment, recipe))

    return render_template(
        "user.html",
        recipes=list(recipes),
        user=user,
        favourites=favourites,
        commentdata=commentdata,
        email=session["email"],
        username=session["username"],
        view=view,
    )


# Route to deal with changing user details
@app.route("/postuser", methods=["POST"])
def postuser():

    # Invalid charecters
    invalid = '[,/<>{}]" '
    # Create a dict of the form input
    formval = request.form.to_dict()
    # Boolean flag to check if the inputs are valid
    valid = True

    # Check if the user inputs are valid
    if "uform-email" in formval.keys():
        # Force certain values to be lowercase
        formval["uform-email"] = formval["uform-email"].lower()
        if "@" not in formval["uform-email"]:
            flash("Please enter a valid email")
            valid = False

        if mongo.db.users.find_one({"email": formval["uform-email"]}):
            flash(
                "You have already signed up with this email, if you have "
                "forgotten your login details then you can get in touch using "
                "the link at the end of the page"
            )
            valid = False

    # I'm not sure about letting the user update their username, the
    # author in recipe entries is set as the username so it would
    # require changing all the users recipe entries as well so for the
    # moment I'm not letting them
    if "uform-username" in formval.keys():
        formval["uform-username"] = formval["uform-username"].lower()
        if 8 > len(formval["uform-username"]):
            flash("Your username is too short")
            valid = False
        if any(x in invalid for x in formval["uform-username"]):
            flash("Only use letters, numbers and underscores in your username")
            valid = False
        # Check the username or email have not already been used
        if mongo.db.users.find_one({"username": formval["uform-username"]}):
            flash("User name is already taken")
            valid = False

    if "uform-password" in formval.keys():
        formval["uform-password"] = formval["uform-password"].lower()
        if 8 > len(formval["uform-password"]):
            flash("Your password too short")
            valid = False

    # If all the checks have been passed the relevant user details are
    # added and the user logged in
    if valid is True:
        # While it would make sense to update the entry in its relevant
        # if loops above but doing so meant it was possible that when
        # the user updated both the email and password but one of them
        # did not pass their test the correct entry would still update
        # which is not great UX
        if "uform-email" in formval.keys():
            flash("Your email has been updated")
            session["email"] = formval["uform-email"]
            mongo.db.users.update_one(
                {"username": session["username"]},
                {"$set": {"email": formval["uform-email"] }},
            )
        if "uform-password" in formval.keys():
            flash("Your password has been updated")
            formval["pass_hash"] = generate_password_hash(formval["uform-password"])
            del formval["uform-password"]
            mongo.db.users.update_one(
                {"username": session["username"]},
                {"$set": {"pass_hash": formval["pass_hash"] }},
            )

    return redirect(url_for("user", username=session["username"], view="edit"))


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
        # Add todays date
        formval["datejoined"] = datetime.datetime.utcnow()  # .strftime("%Y-%m-%d")
        # Add blank values to user entry
        formval["favourites"] = []
        formval["comments"] = []

        mongo.db.users.insert_one(formval)
        session["logged_in"] = True
        session["username"] = formval["username"]
        return redirect(url_for("home"))
    else:
        return redirect(url_for("signup"))


# Recipe Page
@app.route("/recipe/<rid>")
def recipe(rid):

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})
    print(recipe)
    comments = []
    for cid in recipe["comments"]:
        comment = mongo.db.comments.find_one({"_id": ObjectId(cid)})
        user = mongo.db.users.find_one({"_id": ObjectId(comment["user_id"])})
        comments.append((comment, user))

    # If the user is logged in and the user has liked the recipe then the like flag is set
    like = likecheck(rid)

    if request.args.get("show"):
        show = request.args.get("show")
    else:
        show = False

    return render_template(
        "recipe.html", recipe=recipe, like=like, comments=comments, show=show
    )


# Recipe like page
@app.route("/recipe/<rid>/like")
def recipelike(rid):

    if "logged_in" in session and session["logged_in"] is True:
        user = mongo.db.users.find_one({"_id": ObjectId(session["id"])})
        if likecheck(rid) is False:
            mongo.db.users.update(user, {"$push": {"favourites": rid }})
        else:
            mongo.db.users.update(user, {"$pull": {"favourites": rid }})

    return redirect(url_for("recipe", rid=rid))


# Recipe comment page
@app.route("/recipe/<rid>/comment", methods=["POST"])
def recipecomment(rid):

    today = datetime.datetime.utcnow()  # .strftime("%Y-%m-%d")

    if "logged_in" in session and session["logged_in"] is True:
        comment = {
            "user_id": session["id"],
            "recipe_id": rid,
            "date": today,
            "comment": request.form["comment"],
        }
        # Comment Id
        newcomment = mongo.db.comments.insert_one(comment)
        # Add the comment to the recipe
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})
        mongo.db.recipes.update(recipe, {"$push": {"comments": newcomment.inserted_id }})
        # Add the comment to the user
        user = mongo.db.users.find_one({"_id": ObjectId(session['id'])})
        mongo.db.users.update(user, {"$push": {"comments": newcomment.inserted_id }})



    return redirect(url_for("recipe", rid=rid, show=True))


# Recipe vote page
@app.route("/recipe/<rid>/vote", methods=["POST"])
def recipevote(rid):

    if "logged_in" in session and session["logged_in"] is True:

        recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})
        avg = recipe["aggregateRating"]["ratingValue"]
        num = recipe["aggregateRating"]["reviewCount"]

        newavg = ((avg * num) + int(request.form["star"])) / (num + 1)

        mongo.db.recipes.update(
            recipe,
            {
                "$set": {
                    "aggregateRating": {"ratingValue": newavg, "reviewCount": num + 1}
                }
            },
        )

    return redirect(url_for("recipe", rid=rid))


# Recipe edit page
@app.route("/recipe/<rid>/edit")
def recipeedit(rid):
    if "logged_in" in session and session["logged_in"] is True:
        # Load the lists
        categories, cuisines, ingredients, units, utensils = dblistload()

        # Load the recipe
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})

        if recipe["cookTime"]:
            cookTime = isotime.fromisostring(recipe["cookTime"])
        else:
            cookTime = "00:00"
        if recipe["prepTime"]:
            prepTime = isotime.fromisostring(recipe["prepTime"])
        else:
            prepTime = "00:00"

        print(recipe["cookTime"], recipe["cookTime"])
        print(cookTime, prepTime)
        return render_template(
            "recipeform.html",
            key=app.config["GOOGLE_API_KEY"],
            cx=app.config["GOOGLE_CX"],
            rid=rid,
            categories=categories,
            cuisines=cuisines,
            ingredients=ingredients,
            units=units,
            utensils=utensils,
            recipe=recipe,
            cookTime=cookTime,
            prepTime=prepTime,
        )
    else:
        flash("You must be logged in to edit a recipe")
        return redirect(url_for("login"))


# Recipe delete page
@app.route("/recipe/<rid>/delete")
def recipedelete(rid):

    # Delete the comments associated with the recipe from both the comment database and the user entries
    for comment in mongo.db.comments.find({"recipe_id":rid}):
        print(comment["_id"])
        for user in mongo.db.users.find({"comments":ObjectId(comment["_id"])}):
            print(user["email"])
            mongo.db.users.update(user, {"$pull": {"comments": ObjectId(comment["_id"]) }})

        mongo.db.comments.delete_one(comment)

    # Delete the recipe from favourites
    for user in mongo.db.users.find():
        if "favourites" in user.keys() and rid in user["favourites"]:
            print(user["email"])
            mongo.db.users.update(user, {"$pull": {"favourites": rid }})

    # Delete the recipe entry
    mongo.db.recipes.delete_one({"_id": ObjectId(rid)})

    return redirect(url_for("user", username=session["username"], view="submitted"))


# Recipe Submission Page
@app.route("/submitrecipe")
def submitrecipe():

    if ("logged_in" in session.keys()) and (session["logged_in"] is True):

        # Load the lists
        categories, cuisines, ingredients, units, utensils = dblistload()

        print("Load page")
        return render_template(
            "recipeform.html",
            key=app.config["GOOGLE_API_KEY"],
            cx=app.config["GOOGLE_CX"],
            categories=categories,
            cuisines=cuisines,
            ingredients=ingredients,
            units=units,
            utensils=utensils,
            recipe=recipeblank,
            cookTime="00:00",
            prepTime="00:00",
        )
    else:
        flash("Please log in before posting a recipe")
        return redirect(url_for("login"))


# Recipe posting route - handles the form data
@app.route("/postrecipe", methods=["POST"])
def postrecipe():
    print("Im Submitting!")
    print(request.form)
    # Todays date
    today = datetime.datetime.utcnow()  # .strftime("%Y-%m-%d")

    # Pulling out values with multiple inputs into lists
    typelist = formlister("categories", request.form, "rform-type")
    cuislist = formlister("cuisines", request.form, "rform-cuisine")
    ingrlist = formlister("ingredients", request.form, "rform-ingredient")
    unitlist = formlister("units", request.form, "rform-unit", title=False)
    utenlist = formlister("utensils", request.form, "rform-utensils")
    quanlist = request.form.getlist("rform-quantity")
    steplist = request.form.getlist("rform-step")

    # Sort lists
    typelist = sorted(typelist)
    cuislist = sorted(cuislist)
    utenlist = sorted(utenlist)

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

    # Seperating out the image url and dimensions
    # This assumes that there are no commas in the url which should be true

    print(request.form["rformImageurl"])
    if len(request.form["rformImageurl"]) > 0:
        imglist = request.form["rformImageurl"].split(",")
    else:
        imglist = [None, 0, 0]

    # Gathering the recipe dictionary
    recipe = {
        # Schema Values
        "@context": "https://schema.org/",
        "@type": "Recipe",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 0.0,
            "reviewCount": 0,
        },
        "author": session["username"],  # This should probably follow schema
        "comments": [],
        "cookTime": tcook,
        "datePublished": today,
        "description": request.form["rformDescription"],
        "image": {
            "@type": "ImageObject",
            "url": imglist[0],
            "height": int(imglist[1]),
            "width": int(imglist[2]),
        },
        "name": request.form["rform-title"].title(),
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
    newrecipe = mongo.db["recipes"].insert_one(recipe)

    # Currently redirects to the submission page, should redirect to the users
    # recipe page
    return redirect(url_for("recipe", rid=newrecipe.inserted_id))


# Recipe posting route - handles the form data
@app.route("/updaterecipe/<rid>", methods=["POST"])
def updaterecipe(rid):
    print("Im updating!")
    oldrecipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})

    # print(request.form)
    # Todays date
    today = datetime.datetime.utcnow()  # .strftime("%Y-%m-%d")

    # Pulling out values with multiple inputs into lists
    typelist = formlister("categories", request.form, "rform-type")
    cuislist = formlister("cuisines", request.form, "rform-cuisine")
    ingrlist = formlister("ingredients", request.form, "rform-ingredient")
    unitlist = formlister("units", request.form, "rform-unit", title=False)
    utenlist = formlister("utensils", request.form, "rform-utensils")
    quanlist = request.form.getlist("rform-quantity")
    steplist = request.form.getlist("rform-step")

    # Sort lists
    typelist = sorted(typelist)
    cuislist = sorted(cuislist)
    utenlist = sorted(utenlist)

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

    # Seperating out the image url and dimensions
    # This assumes that there are no commas in the url which should be true

    # print(request.form["rformImageurl"])
    if len(request.form["rformImageurl"]) > 0:
        imglist = request.form["rformImageurl"].split(",")
    else:
        imglist = [None, 0, 0]

    # Gathering the recipe dictionary
    recipe = {
        # Schema Values
        "@context": "https://schema.org/",
        "@type": "Recipe",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 0.0,
            "reviewCount": 0,
        },
        "author": session["username"],  # This should probably follow schema
        "comments": [],
        "cookTime": tcook,
        "datePublished": oldrecipe["datePublished"],
        "description": request.form["rformDescription"],
        "image": {
            "@type": "ImageObject",
            "url": imglist[0],
            "height": int(imglist[1]),
            "width": int(imglist[2]),
        },
        "name": request.form["rform-title"].title(),
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

    exemptlist = ["_id", "comments", "aggregateRating", "datePublished"]
    for item in recipe:
        if recipe[item] != oldrecipe[item] and item not in exemptlist:
            mongo.db.recipes.update_one(
                {"_id": ObjectId(rid)}, {"$set": {item: recipe[item] }}
            )

    return redirect(url_for("recipe", rid=rid))


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

    app.run(host=app.config["IP"], port=app.config["PORT"], debug=debug)
