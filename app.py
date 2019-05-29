import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime
import isotime

# Temp method to load MONGO_URI without committing it to Github, this should be added to the path of the Heroku app later
with open("MONGO_URI.txt", "r") as myfile:
    uri = myfile.readlines()[0]

# Setting up Flask and PyMongo
app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'cookbook'
app.config["MONGO_URI"] = uri

mongo = PyMongo(app)

# Home page Route - Under construction
@app.route('/')
def hello():
    return render_template('hello.html')

# Login Page - non functional
@app.route('/login')
def login():
    return render_template("login.html")

# Recipe submission form - user facing
# Still needs to pull data from databases
@app.route('/submitrecipe')
def submitrecipe():
    return render_template("recipeform.html")

# Recipe posting route - handles the form data
@app.route('/postrecipe', methods=['POST'])
def postrecipe():
    # Todays date
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    # Pulling out values with multiple inputs into lists
    typelist = request.form.getlist('rform-type')
    cuislist = request.form.getlist('rform-cuisine')
    ingrlist = request.form.getlist('rform-ingredient')
    quanlist = request.form.getlist('rform-quantity')
    unitlist = request.form.getlist('rform-unit')
    steplist = request.form.getlist('rform-step')
    utenlist = request.form.getlist('rform-utensils')

    # Convert time to ISO 8601 format
    tprep = isotime.converttime(request.form['rform-tprep'])
    tcook = isotime.converttime(request.form['rform-tcook'])
    tadd = isotime.addtime(
        request.form['rform-tprep'], request.form['rform-tcook'])

    # 'Zipping' the ingredients into a list and a list of dictionaries
    ingrdictlist = []
    ingrfulllist = []
    for i in range(len(ingrlist)):
        ingrdictlist.append({
            'name': ingrlist[i],
            'quantity': quanlist[i],
            'unit': unitlist[i],
        })
        ingrfulllist.append(quanlist[i] + ' ' +
                            unitlist[i] + ' ' + ingrlist[i])

    # 'Zipping' the steps into Schema dictionaries
    for i in range(len(steplist)):
        steplist[i] = {
            "@type": "HowToStep",
            "text": steplist[i]}

    # Gathering the recipe dictionary
    recipe = {
        # Schema Values
        "@context": "https://schema.org/",
        "@type": "Recipe",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 0,
            "reviewCount": 0
        },
        "author": "",  # Not exactly sure how this will work...
        "comment": [],
        "cookTime": tcook,
        "datePublished": today,
        "description": request.form['rform-description'],
        "image": {
            "@type": "ImageObject",
            "url": "",  # This still needs to be implemented
            "height": 200,
            "width": 200
        },
        "name": request.form['rform-title'],
        "prepTime": tprep,
        "recipeCategory": typelist,
        "recipeCuisine": cuislist,
        "recipeIngredient": ingrfulllist,
        "recipeInstructions": steplist,
        "recipeYield": request.form['rform-serving'],
        "totalTime": tadd,
        # My Values
        "ingredientdict": ingrdictlist,
        "utensils": utenlist,
        "notes": request.form['rform-notes'],
    }

    print(recipe)

    # Currently redirects to the submission page, should redirect to the users
    # recipe page
    return redirect(url_for('submitrecipe'))

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
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port='8080',
            debug=True)
