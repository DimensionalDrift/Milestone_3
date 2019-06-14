# Milestone Project 3

<!--

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



Design Resourse
https://www.furtherfood.com/submitrecipe/
https://www.bbcgoodfood.com/
https://tastesbetterfromscratch.com
https://www.allrecipes.com
https://www.facebook.com/


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


Libraries
https://github.com/ttskch/select2-bootstrap4-theme
https://github.com/select2/select2-bootstrap-theme


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

Conventions and Style Guides
https://stackoverflow.com/questions/3736553/how-to-execute-function-after-image-is-loaded-into-a-div-with-jquery
https://google.github.io/styleguide/htmlcssguide.html#ID_and_Class_Name_Delimiters
https://www.webfx.com/blog/web-design/20-html-best-practices-you-should-follow/
https://code.tutsplus.com/tutorials/30-css-best-practices-for-beginners--net-6741
https://code.tutsplus.com/tutorials/24-javascript-best-practices-for-beginners--net-5399
https://gist.github.com/sloria/7001839


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