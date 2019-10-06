# Flask App

# -------------------- Imports --------------------

import os
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    url_for,
    request,
    session,
    escape,
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail

import datetime
import isotime


# --------------------Functions and Templates --------------------

# A blank recipe template to be used when submitting a new recipe
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


# Function that returns the current date and time
def getdate():
    return datetime.datetime.utcnow()  # .strftime("%Y-%m-%d")


# Function to add values to list tables that store lists of categories,
# ingredients etc.
def addto_listtable(table, vallist):
    for item in vallist:
        entry = mongo.db[table].find_one({"name": item})
        # If the entry in the table exists increment its number by one
        if entry:
            add = entry["number"] + 1
            mongo.db[table].update(entry, {"$set": {"number": add}})
        # Otherwise create an entry
        else:
            new_entry = {"name": item, "number": 1}
            mongo.db[table].insert_one(new_entry)


# Function makes lists of form inputs that have multiple values. Each of
# the entries are then tracked in the database tables using
# addto_listtable. The entries are also converted to title case by
# default but setting the flag title to False will bypass that step
def formlister(table, form, key, title=True):
    # Create list
    flist = form.getlist(key)

    # If the flag is set, make each entry title case
    if title:
        for i in range(len(flist)):
            flist[i] = flist[i].title()

    # Add the values to mongodb tables
    addto_listtable(table, flist)

    return flist


# Function checks if a recipe is in the logged in users list of
# favourites and returns True if it is, False if not
def likecheck(rid):
    if "logged_in" in session and session["logged_in"] is True:
        userfav = mongo.db.users.find_one({"email": session["email"]})
        if rid in userfav["favourites"]:
            return True

    return False


# Function checks if the user has already rated this recipe and returns
# True if they have, False if not
def votecheck(rid):
    if "logged_in" in session and session["logged_in"] is True:
        userfav = mongo.db.users.find_one({"email": session["email"]})
        if rid in userfav["votes"]:
            return True

    return False


# Function loads all the lists of list tables into memeory, might not be
# a great idea as the lists get longer but I can't think of another way
# to pass these into the select2 lists...
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


# Function to retrieve a number of recipes from the database. The
# default order is by descending datePublished but both can be changed.
def recipeget(num, skip=0, sort="datePublished", order=-1, query=None):
    # If a search query is made then add the search query to the lookup
    if query:
        recipes = list(
            mongo.db.recipes.find({"$text": {"$search": query}})
            .sort(sort, order)
            .limit(num)
            .skip(num * skip)
        )

    # Otherwise it's just an ordered list of the last number of recipes
    else:
        recipes = list(
            mongo.db.recipes.find().sort(sort, order).limit(num).skip(num * skip)
        )

    return recipes


# Function to log an activity to the list of user activities, this
# database is used on the home page to give the user the sense that the
# website is active and encourage them to interact with the site.
def activitylog(uname, uid, rname, rid, rimage, act):
    # Checks which type of activity is being logged then uses a more
    # verbose description, in the future a random list of descriptions
    # could be used for each activity to add variety
    if act == "comment":
        activity = "commented on"

    elif act == "like":
        activity = "liked"

    elif act == "add":
        activity = "submitted the recipe for"

    else:
        activity = ""

    # New activity entry
    new_entry = {
        "user_name": uname,
        "user_id": uid,
        "recipe_name": rname,
        "recipe_id": rid,
        "recipe_image": rimage,
        "date": getdate(),
        "activity": activity,
    }

    # If the type of activity has not been recognized above then it is
    # not added to the database
    if len(activity) > 1:
        mongo.db.activity.insert_one(new_entry)
    else:
        print("Incorrect activity type")


# Function used to return a number of activity entries from the database

# Future feature, if the user repeats an action such as making multiple
# comments in a row on the same recipe the activity feed will have what
# look like duplicated entries. While everything is working as intended
# it does not look great when one user clogs up the activity feed. This
# function should check if a user has preformed the same action within a
# given number of activities and then not return these sudo duplicates.
def activityfeed(num):

    activity = mongo.db.activity.find().sort("date", -1).limit(num)
    activity = list(activity)

    return activity


# -------------------- Setup --------------------

# Setting up Flask
app = Flask(__name__)

# If the DEPLOYED environment variable is detected in Heroku then the
# app variables are pulled from the environment
if "DEPLOYED" in os.environ:
    # Heroku Environment Variables
    app.config["IP"] = os.environ.get("IP")
    app.config["PORT"] = os.environ.get("PORT")
    # Google Search API Environment Variables
    app.config["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")
    app.config["GOOGLE_CX"] = os.environ.get("GOOGLE_CX")
    # MongoDB Environment Variables
    app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    # Email Environment Variables
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
    app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL")
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

    debug = False

# Otherwise the variables are pulled from a config file only found on
# the development machine. Debug is also set to true only on the
# development machine
else:
    app.config.from_envvar("COOKBOOK_CONFIG")
    debug = True

# Setting up email for Flask
mail = Mail()
mail.init_app(app)

# Setting up PyMongo for Flask
mongo = PyMongo(app)

# -------------------- App Routes --------------------

# Home Page

# The first page that the user sees, the home page features an endless
# list of all the recipes that have been added to the database. Using
# the Infinite Scrolling Library, once the user gets to the end of the
# page and clicks the load more button the recipes will continuously
# load as the user scrolls. If the user is logged in then they can like
# recipes which add the recipes to the users list of liked recipes and
# they can comment on a recipe. This would not be encouraged as there
# are very little details the user can see from the home page but the
# option is there as well as all previous comments.
@app.route("/")
@app.route("/page/<page>")
def home(page="0"):
    # Number of recipes to load on homepage, in testing this can be changed
    num = 5

    # Calculate total number of recipes and maximum number of pages
    total = mongo.db.recipes.count()
    page = int(page)
    pagemax = divmod(total, num)[0]

    # Load a number of activities from the database
    activity = activityfeed(5)

    # Pull a number of recipes from the database. As the user scrolls
    # through the site the page number increases and so the function
    # returns the next set of recipes
    recipes = recipeget(num, page)
    recipelist = []

    # For each of the recipes to be loaded, create a list of tuples of
    # each recipe and its comments, drawn from the comments database
    for recipe in recipes:

        commentlist = []
        for cid in recipe["comments"]:
            comment = mongo.db.comments.find_one({"_id": ObjectId(cid)})
            user = mongo.db.users.find_one(
                {"_id": ObjectId(comment["user_id"])}
            )
            commentlist.append((comment, user))

        # If the user is logged in and the user has liked or rated the
        # recipe then the flags are set for the template to load the
        # appropriate assets
        like = likecheck(str(recipe['_id']))

        recipelist.append([recipe, commentlist, like])

    return render_template(
        "index.html",
        recipelist=recipelist,
        page=page,
        pagemax=pagemax,
        activity=activity,
    )


# Search Results Page

# This page is where the user is brought to when they preform a search
# in the top navigation bar. Short summary cards of recipes that meet
# the search criteria are shown in an endless list. At the moment
# advanced filtering has not been added to the back-end but the
# front-end code is there for the future. The page also uses the
# Infinite Scrolling Library to display the recipes.
@app.route("/search")
@app.route("/search/")
@app.route("/search/<query>")
@app.route("/search/<query>/<page>")
def search(query=None, page="0"):

    # Number of search results to load, in testing this can be changed
    num = 5

    # Pull a number of recipes from the database matching the users
    # search query. As the user scrolls through the site the page number
    # increases and so the function returns the next set of recipes
    page = int(page)
    recipes = recipeget(num, page, query=query)

    # Calculate total number of recipes and maximum number of pages
    total = len(recipes)
    pagemax = divmod(total, num)[0]

    # Load the lists for the select2 inputs
    categories, cuisines, ingredients, units, utensils = dblistload()

    return render_template(
        "search.html",
        query=query,
        recipes=recipes,
        page=page,
        pagemax=pagemax,
        categories=categories,
        cuisines=cuisines,
        ingredients=ingredients,
        units=units,
        utensils=utensils,
        cookTime="00:00",
        prepTime="00:00",
    )


# App Route to manage the search form found in the top navbar
@app.route("/postsearch", methods=["POST"])
def postsearch():
    query = escape(request.form["query"])
    return redirect(url_for("search", query=query))


# App Route to manage the advanced search form found on the search page
@app.route("/postadvsearch", methods=["POST"])
def postadvsearch():
    query = escape(request.form["advquery"])
    return redirect(url_for("search", query=query))


# Login Page

# This page where the user enters their email and password to login to
# the site. The page is just a simple form but also has links to the
# signup page and the forgotten password page.
@app.route("/login")
def login():
    print("logged and loaded")
    return render_template("login.html")


# App Route to manage the login form

# If the user enters an incorrect email or password they are redirected
# to the login page where a flash message will tell them what went
# wrong, otherwise the user is redirected to their user page
@app.route("/postlogin", methods=["POST"])
def postlogin():

    # Find email in database
    val = mongo.db.users.find_one(
        {"email": escape(request.form["loginEmail"])}
    )

    # If email and password are in database add the user details to the
    # session cookie and redirect them to their user page
    if val and check_password_hash(
        val["pass_hash"], escape(request.form["loginPassword"])
    ):
        session["logged_in"] = True
        session["username"] = val["username"]
        session["id"] = str(val["_id"])
        session["email"] = val["email"]
        return redirect(url_for("user", username=session["username"]))

    # Otherwise redirect the user to the login page again with an error
    elif val:
        flash("Your password is incorrect")
        return redirect(url_for("login"))
    else:
        flash("Your email is incorrect")
        return redirect(url_for("login"))


# App Route to log user out by clearing the session cookie
@app.route("/logout")
def logout():
    session["logged_in"] = False
    session.pop("email", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("home"))


# User Page

# This page is where the user can see and manage any recipes that they
# have submitted or interacted with. There are 4 views, 3 where the user
# can see the list of recipes that they have submitted, likes or
# commented on. The final view allows the user to change their email and
# password, however the user cannot change their username as it is used
# as an identifier some places in the database. While it's not common
# for a user to change their username I think it would be better UX so
# could be included in the future. Another feature that should be added
# in the future is for the user to be able to change their profile
# picture but that will have to be added later.
@app.route("/user/<username>")
@app.route("/user/<username>/<view>")
def user(username, view="submitted"):

    # If the user is not logged in at all and navigates to their user
    # page they are redirected to the login page and asked to login
    if "username" not in session.keys():
        flash("Please log in to see your user profile")
        return redirect(url_for("login"))

    # If the user tries to view a profile that they are not logged in as
    # they are warned that they are trying to use the site as another
    # user
    if username != session["username"]:
        flash("You are not logged in as this user")
        return redirect(url_for("login"))

    # The users recipes are loaded from the database
    recipes = mongo.db.recipes.find({"author": session["username"]})
    user = mongo.db.users.find_one({"username": session["username"]})

    # Create a list of the favourites recipes
    favourites = []
    for rid in user["favourites"]:
        favourites.append(mongo.db.recipes.find_one({"_id": ObjectId(rid)}))

    # Create a list of the comment tuples, the first item of the list is
    # the comment, the second is the recipe itself
    commentdata = []
    for cid in user["comments"]:
        comment = mongo.db.comments.find_one({"_id": ObjectId(cid)})
        recipe = mongo.db.recipes.find_one(
            {"_id": ObjectId(comment["recipe_id"])}
        )
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


# App Route to deal with changing user details
@app.route("/postuser", methods=["POST"])
def postuser():

    # Invalid charecters
    invalid = '[,/<>{}]" '
    # Create a dictionary of the form input
    formval = request.form.to_dict()
    # Boolean flag to check if the inputs are valid
    valid = True

    # Change Email
    # Check if the user inputs are valid, of they are not then warn the
    # user that something is wrong
    if "uform-email" in formval.keys():
        # Force certain values to be lowercase
        formval["uform-email"] = formval["uform-email"].lower()
        if "@" not in formval["uform-email"]:
            flash("Please enter a valid email")
            valid = False

        if mongo.db.users.find_one({"email": formval["uform-email"]}):
            flash(
                "You have already signed up with this email, if you have "
                "forgotten your login details then you can get in touch "
                "using the 'Contact Us' link at the end of the page"
            )
            valid = False

    # Change Username
    # I decided that it was easier to not let the user change their
    # username but I've left the functionality here in the backend just
    # in case I allow the user in the future
    if "uform-username" in formval.keys():
        formval["uform-username"] = formval["uform-username"].lower()
        if 8 > len(formval["uform-username"]):
            flash("Your username is too short")
            valid = False
        if any(x in invalid for x in formval["uform-username"]):
            flash(
                "Only use letters, numbers and underscores in your username"
            )
            valid = False
        # Check the username or email have not already been used
        if mongo.db.users.find_one({"username": formval["uform-username"]}):
            flash("User name is already taken")
            valid = False

    # Change Password
    if "uform-password" in formval.keys():
        formval["uform-password"] = formval["uform-password"].lower()
        if 8 > len(formval["uform-password"]):
            flash("Your password too short")
            valid = False

    # If all the checks have been passed the relevant user details are
    # added and the user logged in
    if valid is True:
        # While it would make sense to update the entry in its relevant
        # if loops above, doing so meant it was possible that when the
        # user updated both the email and password but one of them did
        # not pass their test the correct entry would still update but
        # an error still returned which is not great UX
        if "uform-email" in formval.keys():
            flash("Your email has been updated")
            session["email"] = formval["uform-email"]
            mongo.db.users.update_one(
                {"username": session["username"]},
                {"$set": {"email": formval["uform-email"]}},
            )
        if "uform-password" in formval.keys():
            flash("Your password has been updated")
            formval["pass_hash"] = generate_password_hash(
                formval["uform-password"]
            )
            del formval["uform-password"]
            mongo.db.users.update_one(
                {"username": session["username"]},
                {"$set": {"pass_hash": formval["pass_hash"]}},
            )

    return redirect(url_for(
        "user", username=session["username"], view="edit")
    )


# Signup Page

# This page where the user chooses a username and using an email and
# password can sign up to use the site. The page features a simple form
# but before the user can sign up a disclaimer pops up explaining that
# this project is a student project and no guarantees can be made
# regarding the safety of their data. As no emails are sent out to the
# users at the moment it is suggested that they use a dummy email if
# they are not comfortable using their real email.
@app.route("/signup")
def signup():
    return render_template("signupform.html")


# App Route to deal with the signup form
@app.route("/postsignup", methods=["POST"])
def postsignup():

    # Invalid characters
    invalid = '[,/<>{}]" '
    # Create a dict of the form input
    formval = request.form.to_dict()
    # Force certain values to be lowercase
    formval["email"] = formval["email"].lower()
    formval["username"] = formval["username"].lower()
    # Boolean flag to check if the inputs are valid
    valid = True

    # Check if the user inputs are valid as in there is an @ in the
    # email, the username and password are over 8 characters and that
    # the username does not contain any invalid characters
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
        # The password is hashed then deleted before being added to the
        # database
        formval["pass_hash"] = generate_password_hash(formval["password"])
        del formval["password"]
        # Add todays date
        formval["datejoined"] = getdate()
        # Add blank values to user entry
        formval["comments"] = []
        formval["favourites"] = []
        formval["votes"] = []

        val = mongo.db.users.insert_one(formval)

        # The values are then added to the session cookie so the user
        # remains logged in
        session["id"] = str(val.inserted_id)
        session["logged_in"] = True
        session["username"] = formval["username"]
        session["email"] = formval["email"]

        return redirect(url_for("user", username=session["username"]))
    # Otherwise they are redirected to the signup page with the
    # appropriate error
    else:
        return redirect(url_for("signup"))


# Recipe Page

# This is a full page with all the submitted details of a given recipe.
# The page features the image associated with the recipe, the list of
# ingredients, steps and other additional details each in their own
# cards. The user can interact with the recipe by liking it or leaving a
# comment.
@app.route("/recipe/<rid>")
def recipe(rid):
    # The recipe is loaded
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})

    # The comments associated with the recipes are loaded into a list to
    # be passed to the template
    comments = []
    for cid in recipe["comments"]:
        comment = mongo.db.comments.find_one({"_id": ObjectId(cid)})
        user = mongo.db.users.find_one({"_id": ObjectId(comment["user_id"])})
        comments.append((comment, user))

    # If the user is logged in and the user has liked or rated the
    # recipe then the flags are set for the template to load the
    # appropriate assets
    like = likecheck(rid)
    vote = votecheck(rid)

    # If show is set then the comments are shown on load, otherwise the
    # user has to press a button to reveal them
    if request.args.get("show"):
        show = request.args.get("show")
    else:
        show = False

    return render_template(
        "recipe.html", recipe=recipe, like=like, vote=vote,
        comments=comments, show=show
    )


# App Route to like a recipe
@app.route("/recipe/<rid>/like")
def recipelike(rid):

    # If a user is logged in
    if "logged_in" in session and session["logged_in"] is True:
        user = mongo.db.users.find_one({"_id": ObjectId(session["id"])})
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})

        # If the user has not liked the page before then update the
        # users database entry and add the recipe to their liked list
        if likecheck(rid) is False:
            mongo.db.users.update(user, {"$push": {"favourites": rid}})

            # Add the like to the global activity feed
            activitylog(
                user["username"],
                session["id"],
                recipe["name"],
                rid,
                recipe["image"],
                "like",
            )
        # If the user has already liked the recipe then remove the like
        # from their liked list
        else:
            mongo.db.users.update(user, {"$pull": {"favourites": rid}})

    # If a user is not logged in then redirect them to the login page
    # and display an error
    else:
        flash("Pleaes log in or sign up to like and comment on recipes!")
        return redirect(url_for("login"))

    return redirect(url_for("recipe", rid=rid))


# App Route to add a comment to the recipe
@app.route("/recipe/<rid>/comment", methods=["POST"])
def recipecomment(rid):

    # If a user is logged in
    if "logged_in" in session and session["logged_in"] is True:
        # Generate the comment database entry and add it to the database
        comment = {
            "user_id": session["id"],
            "recipe_id": rid,
            "date": getdate(),
            "comment": escape(request.form["comment"]),
        }
        newcomment = mongo.db.comments.insert_one(comment)
        commentid = str(newcomment.inserted_id)

        # Add the comment to the recipe database entry
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})
        mongo.db.recipes.update(recipe, {"$push": {"comments": commentid}})

        # Add the comment to the user database entry
        user = mongo.db.users.find_one({"_id": ObjectId(session["id"])})
        mongo.db.users.update(user, {"$push": {"comments": commentid}})

        # Add the activity to the global feed
        activitylog(
            user["username"],
            session["id"],
            recipe["name"],
            rid,
            recipe["image"],
            "comment",
        )

    return redirect(url_for("recipe", rid=rid, show=True))


# App Route to rate a recipe
@app.route("/recipe/<rid>/vote", methods=["POST"])
def recipevote(rid):

    # If a user is logged in
    if "logged_in" in session and session["logged_in"] is True:

        user = mongo.db.users.find_one({"_id": ObjectId(session["id"])})

        # If the recipe has not been rated before by the user then
        # calculate the new rating including the users vote and update
        # the database
        if rid not in user["votes"]:
            recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})
            avg = recipe["aggregateRating"]["ratingValue"]
            num = recipe["aggregateRating"]["reviewCount"]

            newavg = ((avg * num) + int(escape(
                request.form["star"]))) / (num + 1)

            mongo.db.recipes.update(
                recipe,
                {
                    "$set": {
                        "aggregateRating": {
                            "ratingValue": newavg,
                            "reviewCount": num + 1,
                        }
                    }
                },
            )

            mongo.db.users.update(user, {"$push": {"votes": rid}})

    return redirect(url_for("recipe", rid=rid))


# App Route to edit a recipe only if the user wrote the recipe
@app.route("/recipe/<rid>/edit")
def recipeedit(rid):

    # If a user is logged in
    if "logged_in" in session and session["logged_in"] is True:

        # Load the lists for the select2 inputs
        categories, cuisines, ingredients, units, utensils = dblistload()

        # Load the recipe
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})

        # If the recipe has either a cooking or prep time then convert
        # it from the iso standard time used in the database to a time
        # string
        if recipe["cookTime"]:
            cookTime = isotime.fromisostring(recipe["cookTime"])
        else:
            cookTime = "00:00"
        if recipe["prepTime"]:
            prepTime = isotime.fromisostring(recipe["prepTime"])
        else:
            prepTime = "00:00"

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

    # If a user is not logged in then redirect them to the login page
    # and display an error
    else:
        flash("You must be logged in to edit a recipe")
        return redirect(url_for("login"))


# App Route to delete a recipe only if the user wrote the recipe
@app.route("/recipe/<rid>/delete")
def recipedelete(rid):

    # If a user is logged in
    if "logged_in" in session and session["logged_in"] is True:

        # Load the recipe and user
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})
        user = mongo.db.users.find_one({"_id": ObjectId(session["id"])})

        # If the user did not write the recipe then they are redirected
        # to the login page and scolded
        if recipe["author"] != user["username"]:
            flash(
                "You did not write this recipe so you're not allowed "
                + "to delete it!"
            )
            return redirect(url_for("login"))

        # Delete the comments associated with the recipe from both the
        # comment database and user entries
        for comment in mongo.db.comments.find({"recipe_id": rid}):
            for user in mongo.db.users.find(
                    {"comments": ObjectId(comment["_id"])}):
                mongo.db.users.update(
                    user, {"$pull": {"comments": ObjectId(comment["_id"])}}
                )

            mongo.db.comments.delete_one(comment)

        # Delete the recipe from users favourites
        for user in mongo.db.users.find():
            if "favourites" in user.keys() and rid in user["favourites"]:
                mongo.db.users.update(user, {"$pull": {"favourites": rid}})

        # Delete the recipe entry
        mongo.db.recipes.delete_one({"_id": ObjectId(rid)})

    return redirect(
        url_for("user", username=session["username"], view="submitted")
    )


# Recipe Submission Page

# A form for submitting a recipe to the database. It features 3 main
# types of inputs, plain text input for things like the title, select2
# inputs for things that will be repeated from user to user like
# cuisines and ingredients, and a image picker for the recipes image.
# The image picker pulls images from Google images and the user can
# search for an image that best represents their recipe. I know it's
# usually not a good idea to hotlink others images from around the web
# but for the purpose of this project with limited users and limited
# space in the free Heroku site for actual uploads I figured it will be
# ok.
@app.route("/submitrecipe")
def submitrecipe():

    # If a user is logged in
    if "logged_in" in session and session["logged_in"] is True:

        # Load the lists for the select2 inputs
        categories, cuisines, ingredients, units, utensils = dblistload()

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

    # Otherwise redirect the user to the login page
    else:
        flash("Please log in before posting a recipe")
        return redirect(url_for("login"))


# App Route to post the Recipe
@app.route("/postrecipe", methods=["POST"])
def postrecipe():

    # Pulling out form values with multiple inputs into lists
    typelist = formlister("categories", request.form, "rform-type")
    cuislist = formlister("cuisines", request.form, "rform-cuisine")
    ingrlist = formlister("ingredients", request.form, "rform-ingredient")
    unitlist = formlister("units", request.form, "rform-unit", title=False)
    utenlist = formlister("utensils", request.form, "rform-utensils")
    quanlist = request.form.getlist("rform-quantity")
    steplist = request.form.getlist("rform-step")

    # Sort some of the lists
    typelist = sorted(typelist)
    cuislist = sorted(cuislist)
    utenlist = sorted(utenlist)

    # Convert time to ISO 8601 format
    tprep = isotime.converttime(escape(request.form["rformTprep"]))
    tcook = isotime.converttime(escape(request.form["rformTcook"]))
    tadd = isotime.addtime(
        escape(request.form["rformTprep"]), escape(request.form["rformTcook"])
    )

    # 'Zipping' the ingredients into a list and a list of dictionaries,
    # both are submitted to the database so that ingredients can be used
    # for filtering search results without having to pull them out of a
    # dictionary
    ingrdictlist = []
    ingrfulllist = []
    for i in range(len(ingrlist)):
        ingrdictlist.append(
            {"name": ingrlist[i], "quantity":
                quanlist[i], "unit": unitlist[i]}
        )
        ingrfulllist.append(
            quanlist[i] + " " + unitlist[i] + " " + ingrlist[i]
        )

    # 'Zipping' the steps into Schema dictionaries
    for i in range(len(steplist)):
        steplist[i] = {"@type": "HowToStep", "text": steplist[i]}

    # Separating out the image url and dimensions
    # This assumes that there are no commas in the url which should be true
    if len(escape(request.form["rformImageurl"])) > 0:
        imglist = escape(request.form["rformImageurl"]).split(",")

    # If no image is picked then a none image is passed to the database
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
        "author": session["username"],
        "comments": [],
        "cookTime": tcook,
        "datePublished": getdate(),
        "description": escape(request.form["rformDescription"]),
        "image": {
            "@type": "ImageObject",
            "url": imglist[0],
            "height": int(imglist[1]),
            "width": int(imglist[2]),
        },
        "name": escape(request.form["rform-title"]).title(),
        "prepTime": tprep,
        "recipeCategory": typelist,
        "recipeCuisine": cuislist,
        "recipeIngredient": ingrfulllist,
        "recipeInstructions": steplist,
        "recipeYield": escape(request.form["rform-serving"]),
        "totalTime": tadd,
        # My Values
        "ingredientdict": ingrdictlist,
        "utensils": utenlist,
        "notes": escape(request.form["rformNotes"]),
    }

    # Add the recipe to the database and pull out it's database number
    newrecipe = mongo.db["recipes"].insert_one(recipe)
    rid = newrecipe.inserted_id

    # Add the submission to the global feed
    activitylog(
        session["username"], session["id"],
        recipe["name"], rid, recipe["image"], "add"
    )

    # Redirects to the newly submitted recipe
    return redirect(url_for("recipe", rid=rid))


# App Route to update a recipe

# Pulls the data from the form and compares it to the original recipe,
# where any inputs have changed the database is updated
@app.route("/updaterecipe/<rid>", methods=["POST"])
def updaterecipe(rid):

    # Pull the recipe from the database
    oldrecipe = mongo.db.recipes.find_one({"_id": ObjectId(rid)})

    # Pulling out values with multiple inputs into lists
    typelist = formlister("categories", request.form, "rform-type")
    cuislist = formlister("cuisines", request.form, "rform-cuisine")
    ingrlist = formlister("ingredients", request.form, "rform-ingredient")
    unitlist = formlister("units", request.form, "rform-unit", title=False)
    utenlist = formlister("utensils", request.form, "rform-utensils")
    quanlist = request.form.getlist("rform-quantity")
    steplist = request.form.getlist("rform-step")

    # Sort some of the lists
    typelist = sorted(typelist)
    cuislist = sorted(cuislist)
    utenlist = sorted(utenlist)

    # Convert time to ISO 8601 format
    tprep = isotime.converttime(escape(request.form["rformTprep"]))
    tcook = isotime.converttime(escape(request.form["rformTcook"]))
    tadd = isotime.addtime(
        escape(request.form["rformTprep"]), escape(request.form["rformTcook"])
    )

    # 'Zipping' the ingredients into a list and a list of dictionaries
    ingrdictlist = []
    ingrfulllist = []
    for i in range(len(ingrlist)):
        ingrdictlist.append(
            {"name": ingrlist[i],
                "quantity": quanlist[i], "unit": unitlist[i]}
        )
        ingrfulllist.append(
            quanlist[i] + " " + unitlist[i] + " " + ingrlist[i]
        )

    # 'Zipping' the steps into Schema dictionaries
    for i in range(len(steplist)):
        steplist[i] = {"@type": "HowToStep", "text": steplist[i]}

    # Separating out the image url and dimensions
    # This assumes that there are no commas in the url which should be true
    if len(escape(request.form["rformImageurl"])) > 0:
        imglist = escape(request.form["rformImageurl"]).split(",")
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
        "description": escape(request.form["rformDescription"]),
        "image": {
            "@type": "ImageObject",
            "url": imglist[0],
            "height": int(imglist[1]),
            "width": int(imglist[2]),
        },
        "name": escape(request.form["rform-title"]).title(),
        "prepTime": tprep,
        "recipeCategory": typelist,
        "recipeCuisine": cuislist,
        "recipeIngredient": ingrfulllist,
        "recipeInstructions": steplist,
        "recipeYield": escape(request.form["rform-serving"]),
        "totalTime": tadd,
        # My Values
        "ingredientdict": ingrdictlist,
        "utensils": utenlist,
        "notes": escape(request.form["rformNotes"]),
    }

    # List of inputs that are not to be checked for any changes
    exemptlist = ["_id", "comments", "aggregateRating", "datePublished"]

    # Comparing the two recipes, if an entry is different then update
    # the database
    for item in recipe:
        if recipe[item] != oldrecipe[item] and item not in exemptlist:
            mongo.db.recipes.update_one(
                {"_id": ObjectId(rid)}, {"$set": {item: recipe[item]}}
            )

    return redirect(url_for("recipe", rid=rid))


# App Route for the contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")


# App Route to send a contact message to the email
@app.route("/postcontact", methods=["POST"])
def postcontact():

    # This message is quite simple as of now, it could be jazzed up in
    # the future but it's only me that sees it so I'm not too worried
    msg = Message("Cookbook Email", recipients=["ca.ciprojects@gmail.com"])
    msg.html = " From: %s <br> Subject: %s <br><br> Message: %s" % (
        escape(request.form["cformEmail"]),
        escape(request.form["cformSubject"]),
        escape(request.form["cformText"]),
    )
    mail.send(msg)

    return redirect(url_for("contact"))


# App Route for testing code snippets on a test page
@app.route("/test")
def test():
    return render_template("test.html")


# App Route to handle is a user navigates to a non existent page
@app.errorhandler(404)
def page_not_found(e):
    flash(
        "It appears that the page you were looking for does not exist,"
        + " if you believe that this is an error please contact us using the"
        + " form below."
    )
    return render_template("contact.html"), 404


# Main loop
if __name__ == "__main__":
    app.secret_key = os.urandom(12)

    app.run(host=app.config["IP"], port=app.config["PORT"], debug=debug)
