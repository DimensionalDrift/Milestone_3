# Milestone Project 3

## Alpha Testing
The site is currently live for early Alpha testing, if you would like to try it out you can find it here:

http://cimp3-cookbook.herokuapp.com/

<!--

TODO List:
Add - Test out mobile view
Add - Implement advanced search result filtering (a bunch more recipes need to be added before this can be done)
Add - Category exploring page where recipes are grouped by cuisine or time
Add - Link to forgotten password form
Add - Stop sudo duplicates being added to the activity feed
Fix - fitimage sometimes needs to be reloaded for it to work correctly, find out why it does not load the first time (probably something to do with callbacks)
Fix - Popups like coming soon or the star rating on mobile only go away when you tap elsewhere on the screen, it mean they get in the way when voting on a recipe so they need to timeout when tapped.
Fix - Add placeholder image if recipe image does not load



DONE List:
Add - search page with results and stuff
Fix - Stop the user voting on a recipe multiple times, that's just not fair
Add - Coming soon popups to some things that are not working
Fix - Change the mongodb to use the new fresh database and add a bunch of sample recipes to the database
Fix - Comments on the home page all open when one button is clicked, generally having multiple recipe cards needs to be fixed on the home page

User Stories
As a user I would like:

to add my recipes to my collection
to add other users recipes to my collection
to view other users recipes
to comment on other users recipes
to vote on other users recipes
to sort recipes by different users
to sort recipes by different cuisine
to sort recipes by different ingredient
to sort recipes by different meal type
to view recipes step by step while cooking
to give feedback to the website to help improve the experience

Mandatory Requirements
A project violating any of these requirements will FAIL

    Data handling: Build a mangoDB-backed Flask project for a web application that allows users to store and manipulate data records about a particular domain. If you are considering using a different database, please discuss that with your mentor first and inform Student Care.

    Database structure: Put some effort into designing a database structure well-suited for your domain. Make sure to put some thought into the nesting relationships between records of different entities.

    User functionality: Create functionality for users to create, locate, display, edit and delete records (CRUD functionality).

    Use of technologies: Use HTML and custom CSS for the website's front-end.

    Structure: Incorporate a main navigation menu and structured layout (you might want to use Materialize or Bootstrap to accomplish this).

Documentation: Write a README.md file for your project that explains what the project does and the value that it provides to its users.

    Version control: Use Git & GitHub for version control.

Attribution: Maintain clear separation between code written by you and code from external sources (e.g. libraries or tutorials). Attribute any code from external sources to its source via comments above the code and (for larger dependencies) in the README.

    Deployment: Deploy the final version of your code to a hosting platform such as Heroku.

Project Example Idea:
External user’s goal:
Find and share recipes

Site owner's goal:
Promote a brand of cooking tools.

Potential features to include:
Create a web application that allows users to store and easily access cooking recipes. Recipes would include fields such as ingredients, preparation steps, required tools, cuisine, etc.

Create the backend code and frontend form(s) to allow users to add new recipes to the site, edit them and delete them.

Create the backend and frontend functionality for users to locate recipes based on the recipe's fields. You may choose to create a full search functionality, or just a directory of recipes.

Provide results in a manner that is visually appealing and user friendly.

Advanced potential feature (nice-to-have)
Build upon the required tools field to promote your brand of kitchen tools (e.g. oven, pressure cooker, etc…).

    Create a dashboard to provide some statistics about all the recipes.



Design Resourse
https://www.furtherfood.com/submitrecipe/
https://www.bbcgoodfood.com/
https://tastesbetterfromscratch.com
https://www.allrecipes.com
https://www.facebook.com/
https://www.thingiverse.com/
https://www.instructables.com/
https://www.nexusmods.com/mods/


Documentation and Tutorials
https://www.w3schools.com/
https://getbootstrap.com/docs/4.3/
https://fontawesome.com/
https://docs.mongodb.com/
https://select2.org/
https://flask-pymongo.readthedocs.io/en/latest/
https://api.jquery.com/
https://developers.google.com/custom-search/docs/element
https://developers.google.com/custom-search/v1/introduction
http://api.mongodb.com/python/current/tutorial.html
http://flask.pocoo.org/docs/1.0/tutorial/
http://flask.pocoo.org/docs/0.12/patterns/flashing/
https://pythonise.com/feed/flask/flask-message-flashing
https://pythonprogramming.net/jquery-flask-tutorial/
https://www.sitesell.com/blog/2017/02/recipe-schema.htmlkno
https://www.w3schools.com/css/css_tooltip.asp
https://devinpractice.com/2019/03/25/flask-mongodb-tutorial/
https://www.tutorialspoint.com/flask/flask_sessions.htm
http://flask.pocoo.org/snippets/54/
https://medium.com/@egealpay1/flask-user-authentication-1eda0af6016c
https://stackoverflow.com/questions/1860482/when-do-you-choose-to-load-your-javascript-at-the-bottom-of-the-page-instead-of
https://overiq.com/flask-101/authentication-in-flask/
https://pythonspot.com/login-authentication-with-flask/
https://infinidum.com/2018/08/18/making-a-simple-login-system-with-flask-login/
https://stackoverflow.com/questions/36835615/difference-between-input-group-and-form-group
https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
https://infinite-scroll.com/api.html
https://flask.palletsprojects.com/en/1.1.x/security/
https://www.idiotinside.com/2015/05/10/python-auto-generate-requirements-txt/
https://security.openstack.org/guidelines/dg_cross-site-scripting-xss.html
https://medium.com/@abderrahman.hamila/what-sanitize-mean-and-why-sanitize-in-code-data-5c68c9f76164
https://medium.com/@smirnov.am/securing-flask-web-applications-f877e374b427
https://stackoverflow.com/questions/43925397/what-is-the-best-way-to-sanitize-inputs-with-flask-and-when-using-mongodb
https://pythonhosted.org/Flask-Mail/
https://stackoverflow.com/questions/43728500/python-flask-e-mail-form-example



Libraries
https://github.com/ttskch/select2-bootstrap4-theme
https://github.com/select2/select2-bootstrap-theme
https://github.com/metafizzy/infinite-scroll


Code Snippets
https://stackoverflow.com/questions/7271482/getting-a-list-of-values-from-a-list-of-dicts
https://www.codeproject.com/Questions/1185082/How-to-create-input-field-with-a-button-click
http://jsfiddle.net/omugbdm1/3/
https://stackoverflow.com/questions/7020659/submit-form-using-a-button-outside-the-form-tag
https://ux.stackexchange.com/questions/58302/error-message-for-invalid-username
https://stackoverflow.com/questions/3736553/how-to-execute-function-after-image-is-loaded-into-a-div-with-jquery
https://stackoverflow.com/questions/51404129/how-to-access-external-javascript-files-through-jinjaflask/51405432
https://stackoverflow.com/questions/11178426/how-can-i-pass-data-from-flask-to-javascript-in-a-template/42158426
https://stackoverflow.com/questions/16310918/css-scale-and-square-center-crop-image
https://coderwall.com/p/ijrrpa/flask-flash-messages-as-bootstrap-alert
https://webdesign.tutsplus.com/tutorials/a-simple-javascript-technique-for-filling-star-ratings--cms-29450
https://codepen.io/jexordexan/pen/yyYEJa
https://github.com/philsturgeon/codeigniter-template/blob/master/user_guide/changelog.html
https://stackoverflow.com/questions/18775074/recreate-3-column-facebook-style-parcial-scrolling-then-fixed-position-css
https://stackoverflow.com/questions/3666953/showing-git-branch-structure
https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
https://git-scm.com/book/en/v1/Git-Tools-Stashing
https://medium.com/datadriveninvestor/git-rebase-vs-merge-cc5199edd77c
https://stackoverflow.com/questions/5340724/get-changes-from-master-into-branch-in-git

Conventions and Style Guides
https://stackoverflow.com/questions/3736553/how-to-execute-function-after-image-is-loaded-into-a-div-with-jquery
https://google.github.io/styleguide/htmlcssguide.html#ID_and_Class_Name_Delimiters
https://www.webfx.com/blog/web-design/20-html-best-practices-you-should-follow/
https://code.tutsplus.com/tutorials/30-css-best-practices-for-beginners--net-6741
https://code.tutsplus.com/tutorials/24-javascript-best-practices-for-beginners--net-5399
https://gist.github.com/sloria/7001839
https://keepachangelog.com/en/1.0.0/
https://moz.com/blog/the-ultimate-guide-to-the-google-search-parameters
https://uxdesign.cc/death-to-complexity-how-we-simplified-advanced-search-a9ab2940acf0
https://dribbble.com/tags/advanced_search
https://uxplanet.org/how-to-improve-advanced-search-ux-450df698004c
https://stackoverflow.com/questions/6028211/what-is-the-standard-naming-convention-for-html-css-ids-and-classes

Icon Credits
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/"              title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"              title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/"              title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"              title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/"              title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"              title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>




Just to recap quickly:

1. Finish user profile
2. Create a template for an individual recipe
3. Create homepage to list all recipes w/ links to individual recipe page for each
4. On user profile page add edit/delete button for each recipe, and possibly on individual recipe page if user owns that recipe
5. Write delete route/function -> @app.route('/delete/<recipe_id>/)
6. Write update route/function -> @app.route('/update/<recipe_id>/')
7. Create update recipe template w/ pre-filled form for user to update recipe, or add ability to edit inline on the user profile/recipe page and POST to the URL with javascript

-->