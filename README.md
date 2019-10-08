# Milestone Project 3 - Cookbook

<img src="wireframe/cookbook_screenshot.png" alt="Cookbook Home Page">

The aim of this project was to create a social and interactive recipe database for users to add their own recipes as well as browse other users submissions. A live version of the site can be found at the link below:

<p align="center">
    http://cimp3-cookbook.herokuapp.com
</p>

The design of the website borrows heavily from a certain popular social media site so should be quite familiar. Users of the site have full CRUD access to the database for their own recipes. A user can create a profile on the site and add as many recipes as they like. Users can delete any recipes they have submitted as well as amend them. Users can also leave comments on recipes so they can leave any feedback they might have for other users.

## UX

When first approaching this project it was helpful to think about potential users needs to inform the design and function of the site. As such, these user stories were considered when designing the site:

As a user I would like to:

- view other users recipes
- comment on other users recipes
- add my recipes to my collection
- add other users recipes to my collection
- manage the recipes in my collection all in one place
- vote on other users recipes
- explore recipes by different cuisine, ingredient, meal type, users etc.
- view recipes step by step while cooking
- give feedback to the website to help improve the experience

Initially it was also planned to have accounts that would have superuser access to the site, these were some of privileges that superusers would have:

As a superuser I would like to:

- moderate the content of the site
- manage entries that have been published to the site
- view usage statistics of the site
- remove users that are not adhering to the site's terms of use


Not all of these goals were fully realized though but that will be discussed in the [Future Features](#future-features) section further down.

## Features

### Existing Features

The website is made of of five main page types:

- The Home Page
- The User Page
- Individual Recipe Pages
- The Search Page
- The Contact/Changelog Page

each of these pages have different features which are described in more detail below.


#### Basic Layout

The basic layout of the site features a header and a footer on all pages. The header is the main navigation for the site with links to different pages and functionality. The header also contains a search bar which allows the user to search for any keyword that might relate to a recipe. On mobile the links in the header are compressed into a 'Hamburger Menu' which expands the header to reveal the links. The footer looks both the same on desktop and mobile and features some standard copyright style text and links to more peripheral information about the site that is not relevant to its functionality. For example, there is a link to the contact form for the site and a link to this page if a user would like to read more about the technical details of the site.


#### The Home Page

The home page is the first point of contact that the user has with the website. It features a list of recipes that users have added to the database. On first load, the page loads five recipes. If the user wishes to scroll through more recipes then they can click/tap the 'Load More' button at the bottom of the page to start endlessly scrolling the rest of the recipes in the database. This interaction has been set up this way for two reasons: First is to allow the user to reach the bottom of the site to interact with the footer. Secondly, since endless scrolling can be resource intensive it is better to have the user choose when to start endless scrolling so that the site loads quicker on first contact.

If the user is using a screen larger than a mobile phone then the home page will also display a list of recent activity on the site. When users like, comment or add recipes to the site, that interaction is added to a list and displayed on the home page. This is to encourage users to explore recent recipes and also give the user the sense that the site is active. At the moment, when a user clicks/taps on an entry in the activity feed then they are taken to the recipe featured in the activity.


#### The Users Page

If the user is interested in interacting with the site, such as adding their own recipes or commenting on others, then the user must create an account and log into it. From the home page the user can either log into an existing account or create a new one by clicking on the 'Login' link in the header. This brings the user to the login page, if a user is creating a new account there is a further link to the account creation page. Both these pages are very similar, featuring a simple web form asking for relevant detail like email and password. The signup page also features a modal which pops up warning the user that this website is a student project and that no guarantees can be made with regard to data safety. Usually standard practice would put warnings like this in a 'Terms and Conditions' pop up that a user must tick to agree to but what is there is sufficient.

Once the user has either signed up or logged in then they are redirected to their own user page. This page features 4 sections: submitted recipes, liked recipes, comments the user has made and a form to update user details. The page also includes some information about the user such as when they first joined the site and how many recipes they have submitted or liked. From this page the user can also edit and delete any recipes that they have submitted but as of right now users are unable to delete any comments they have made.

To update user details a simple web form is used, when a user either enters a new email, password or both, the database is updated. Initially a user was also allowed to update their username but since the username is used as a unique identifier elsewhere it would have required some refactoring of the database structure so that ability has been removed. It is not uncommon to limit the user in this way but I would have liked to give the user the option and it may be included in the future.


#### Recipe Pages

Recipes are presented in a neat layout using multiple Bootstrap cards for each of the sections of the recipe. The first card has the basic information about the recipe such as the name, a description, prep/cooking times, and Cuisine and Meal Type tags. These tags are intended to be links to a sort of gallery layout for similarly tagged recipes but that has not been implemented yet. The first card also has the interactive elements of the recipe with the like button, the share button and the comments button. The like button adds the recipe to a users list of liked recipes that can be found on the users page. The share button is intended to be a link to something like Androids Share Sheet where the user can forward the recipe to others but it has yet to be implemented. The comments button reveals any comments that have been made about the recipe and if the user is logged in then there is a text box so that they can post their own comments. After that, the ingredients and recipe steps are presented on two separate cards as simple lists.

When a user wishes to add a recipe they are brought to a web form to start writing their recipe. The web form has a similar layout to the recipes themselves using different bootstrap cards for different sections of the recipe. The form uses multiple input types each of which are detailed below:

* ##### Simple Text Boxes

    These are the simplest inputs used in the recipe form, both text boxes and text areas are used to add details such the recipes title and description.

* ##### Select2 Dropdown Inptus

    Select2 boxes are a more advanced version of the simple HTML select element and allow the user to search for the input they want to add. When adding something like an ingredient to the recipe a user can start to type what they are looking for into the Select2 box and if it has already been used in another recipe then the user can just choose the relevant ingredient. The idea was that this should help reduce the amount of fragmentation from spelling errors or synonyms in the database. Another feature of Select2 boxes is that the list of options can be sorted by popularity as the options are stored in their own document in the database with a frequency counter. This means that over time the more popular entries will float to the top of the list making it a little easier for the user to select common entries like for example 'Butter', 'Milk' and 'Eggs'.

* ##### Tempus Dominus Inputs

    A time picker is a common input found in other online forms so the Tempus Dominus library is used to enhance the entries for 'Cook Time' and 'Prep Time'. When the user clicks on the input a box pops up allowing the user to pick a number of hours and minutes for the entry. The inputs have been limited to 23hrs 59 minutes with the reason why explained in the section [below](#tempus-dominus).

* ##### Image Selector

    A social recipe website would be lacking without some good eye catching images so with that in mind a custom image picker was designed. In order to avoid having to host image files with the possibly of running out of server space, a solution using Google Images was implemented. When the user clicks/taps on the default recipe image, a modal pops up with a search bar asking them to search for images that best represents their recipe. When the user enters a search query a grid of Google image search results pop up. The user can then click/tap the image that they like and the link to that image is added to the recipe database entry. Then when someone navigates to that recipe or the recipe is viewed on the home page the image is pulled from the link and rendered. I know that hotlinking is not good practice in the real world but since this project is quite small in scope, is going to have limited users and is only going to be used for a limited time I figured this solution is acceptable.


#### Search Results Page

The navigation bar at the top of every page features a search bar that when the user enters a search query they are redirected to a page of results. The results are displayed as snippets in a reverse chronological list that like the home page are endlessly scrolling once the user clicks/taps the 'Load More' button. The search results page also contains advanced search options that in the future would allow the user to narrow down their query to better find what they are looking for.


#### Contact/Changelog Page

As users were testing out the site there was no way for them get in contact if they found an issue or had any comments. Also if a user was testing mid development there needed to be a way to tell them about any changes that were made or bugs that were fixed so they knew what to be testing. With that in mind the contact/changelog page was added. It features a simple webform that asks for the users email, a subject line and the message they would like to send. That is then passed to the Flask-Mail extension which sends an email to a public facing email which is set up to forward emails to a personal email.


### Future Features

There were many features that were considered and even worked on but had to be cut for time or they were deemed too large for the scope of the project.

* #### Personalized Profile Picture.
    At the moment the user cannot choose their own profile picture like they can choose the image for their recipe. It didn't make sense to use the same method of picking a profile picture from Google Images so it was just left that all user profile pictures were the same default image. In the future if image uploading was implemented then custom profile pictures could be used.

* #### Delete Comments.
    At the moment users cannot delete or edit a comment once it has been made. While it would be possible to have a similar method of deleting a comment as you can delete a recipe, a deleted comment must be handled differently once deleted. Since comments can be part of a conversation if a user deletes or edits a comment then it should be indicated that it has been changed/removed so that any other user would know that the conversation might not be complete. This would require some refactoring of the data structures as well as including an exemption for deleted comments so this feature was not included.

* #### Password Recovery.
    Unlike a typical website, this site does not require a user to have a valid email address to use the site. If a user does use a dummy email (which is encouraged as full data safety cannot be guaranteed) having a method to recover a password wouldn't work in all situations so this feature was left to the future.

* #### Cuisine/Meal Type/Ingredient/User Feature Pages.
    It was planned to have feature pages for recipes grouped by things like the Cuisine or Meal Type so users could explore related recipes. This functionality sort of exists in the search feature but is not quite the masonry style gallery that was initially planned. The tags that exist on recipe pages are the start of this feature being implemented.

* #### Advanced Search Functionality.
    The search page was designed with the advanced search functionality but in order to get it to work would require more backend work so it has been left to the future. The aim would be to have the filters included in the search query to mongodb but in limited testing was proving to be difficult so had to be left.

* #### Unit System Preference.
    When users enter ingredients into their recipe they are asked for the name of the ingredient, the quantity and the unit of that quantity. The reason the unit was separated from the quantity was that it was planned to allow the user to choose the system of measurement that they preferred and then all the recipes would be converted for the user in that system such as Imperial or Metric. While unit conversions are easily programmed it was decided to leave that feature for the future.

* #### Custom Content Management System
    As the website grows and users add recipes to the database, some content management would have to take place to make sure that the website has relevant and useful data for users. A simple content management system was planned that would allow a superuser to manage regular users profiles and recipe entries so that any bad actors or low quality comments/recipes could be removed from the site. Also planned for a content management system would be site usage statistics, such as number of recipes added over time and list of active users and popular recipes. Data such as this would help site managers to better manage site and help prioritize which areas should be focused on improving/maintaining.

* #### Step By Step Recipes
    Initially a feature that was considered for the site was to have a step by step mode for recipes which would display the recipe details in a easy to follow way. The idea was that when a user wanted to start cooking a recipe they would enter the step by step mode where each step would display one after another allow the user to follow the recipe while cooking. This was inspired by the way that a Google Home device with a screen would display a recipe and then using voice commands a user can move from step to step. Admittedly this was an ambitious goal but it was considered early on and the design of the database should allow this to be implemented in the future without too much revision of the code.

### Known Issues

As well as features that were not implemented some bugs also had to be left unfixed, some issues include:

* #### Like/Comment/Rate Redirect
    At the moment if the user is on the home page and likes, comments or rates a recipe the user will be redirected to that specific recipes page. When users were testing the site they would be confused as to why they would be redirected away from what they were doing. This happens because the processing of an interaction with a recipe is handled in a separate route in flask which once computed redirects to the recipe page. The interactions were developed in tandem with the recipe page itself and so anything that would cause an element to change on the page, such as the like button changing color, required the page to reload so this method worked as intended. However the home page was not considered and so when the same interaction happens on the home page the user is redirected. To change this behavior would require extensive restructuring of the way that flask works so has been left to the future.

* #### Psudo-duplicates In The Activity Feed.
    Some of the actions in the activity feed can be repeated by users, for example if a user accidentally clicks/taps the like button multiple times then each like is counted as a separate action so logged to the activity feed. This results in a feed that can be populated with what appears to be duplicate entries even thought they are separate actions. A simple filter could be added to remove any psudo-duplicates from appearing.

* #### Image Rendering Bug
    This bug is really hard to track down as it only seems to happen some of the times when a page loads from a cold start. In order to have images scale correctly they are scaled into a sort of 'frame' and shifted so that the center of the image appears in the center of the frame. This allows the image to be scaled up or down and be shown in different shapes like the circular images in the activity feed. Sometimes though the image would not scale correctly and maybe sometimes be too small or too large. When the page is refreshed then the image scales correctly and appears fine. Screenshots of the issue have been included in the X Something Something Folder [link later]. It is unclear what might be the cause of this issue.

* #### Unitless Ingredients
    As discussed in the [Unit Conversions](#unit-system-preference) section above, the user is asked to enter the name, quantity and unit for each ingredient. The ingredient is then stored as a dictionary and then when rendered on the recipe page it is reconstructed from that dictionary as '[quantity][unit] [name]' (eg. '100g Flour'). The issue with this system is that not all ingredients use a unit of measurement such as '3 Eggs' for example. A crude workaround to this problem is to have a 'none' option in the unit dropdown in the form and an exception when rendering a 'none' so you don't have things like '3none Eggs'. A more robust solution to this problem is needed but would most likely require significant changes.

* #### Coming Soon Popups
    On mobile when tapping elements that have no function yet a popup saying 'Coming Soon' was added to let users know that the functionality is not there yet. On desktop when you hover over the element the popup appears but on mobile you have to tap the element for it to appear. This is fine but the issue is that the popup will not disappear until the user taps elsewhere on the page.

* #### Stray Observations
    - The ingredients could be more consistently aligned with a tab space between the measurement and the ingredient.
    - Sometimes you have to click twice on the Select2 boxes to activate them.
    - On the home page the image of the recipe should also be a link to the recipe.
    - Sometimes the profile picture does not display correctly and can be squished.
    - The timestamps on the comments are based on Heroku's clock and not the users local clock.
    - The naviagtion is not very accessibility friendly, for example tabbing between inputs is inconsistent and does not comply with WCAG guidelines.
    -

## Technologies Used

#### Front End Technologies

The front end was built using standard HTML and CSS utilizing the Bootstrap 4 framework for structural layout on each page. JavaScript libraries were included where necessary to include more advanced elements on the site such as the Select2 boxes and the time picker. Otherwise any interactive elements of the site were built using either vanilla JavaScript or jQuery. A list of the libraries used can be found below:

##### Select2

As mentioned in the section [above](#select2-dropdown-inptus), Select2 boxes were chosen to help the user pick inputs, such as ingredients, for their recipes. Initially when designing the form the idea to limit database fragmentation was one of the main considerations. If the database becomes fragmented then it is harder for users to search for relevant recipes. Select2 expands on the basic HTML select element with a search box allowing users to more easily find what they are looking for and hopefully limit variations of the same input being added. The Select2 box is filled with a database of previous inputs which are stored and sorted by a usage counter. The database has been seeded with sample inputs but as users add their recipes, any inputs not in the database will be added so the databases will continue to grow as users add more and more recipes. Having inputs paired with usage counters allows the entries to be sorted so that popular entries will float to the top of the list.

##### Tempus Dominus

Also mentioned [above](#tempus-dominus-inptus) is the inclusion of the Tempus Dominus library. This library was added so that a time picker could be used for picking cooking times on the recipe page. While it works well it required some unusual setup in order for it to work as intended. Since the input is supposed to be used for a 'clock time' rather than a relative time the picker is set to use 24hr time with the default set to midnight (00:00). This means the picker has a limit of 23 hours and 59 minutes for the input. When the user picks a number of hours and minutes for the recipe the 'clock time' is converted to an ISO standard time interval which is then saved to the database.

##### Infinite Scrolling

Since this website involves exploration of possibly a large amount of content it was decided that infinitely scrolling pages would help make the site more engaging. Initially there was an attempt to create this kind of setup by hand but in the end the Infinite Scrolling library was added as it's implementation of this functionality was a lot cleaner and less buggy than what was previously developed. When a user reaches the end of a page there is a button to start the infinite scrolling on the page. As discussed above this interaction was implemented this way to allow the user to reach the end of a page to see the footer and to give the user the choice to start the infinite scrolling as it can be resource intensive on older devices and/or slower connections.


##### jQuery Scrollbar

The jQuery scrollbar library was included to make the scrollbar in the Select2 boxes a little cleaner as the default scrollbar would mess with the spacing in the dropdown.


## Testing and Development

Throughout development all code was written using Sublime and linted on the fly using the [Sublimelinter](https://packagecontrol.io/packages/SublimeLinter) package. Using the plugins, [HTML-Tidy](https://packagecontrol.io/packages/SublimeLinter-html-tidy), [CSSLint](https://packagecontrol.io/packages/SublimeLinter-csslint), [JSHint](https://packagecontrol.io/packages/SublimeLinter-jshint), and [flake8](https://packagecontrol.io/packages/SublimeLinter-flake8), all code was validated and checked for errors before committing to Github. Some warning and errors do remain in the committed code but details of the issue can be found in the section [below](#linter-errors). The Prettier package [JsPrettier](https://packagecontrol.io/packages/JsPrettier) was used to keep the HTML, CSS and JavaScript correctly formatted and the Black package [sublack](https://packagecontrol.io/packages/sublack) was used for Python formatting.

The website has been tested extensively during development in Chrome Beta on Kubuntu Linux. The website was tested for layout arrangements in different form factors and that it was fully responsive. The website was also tested on Chrome Beta for Android to make sure it rendered correctly on a mobile device. Some limited testing was also done in iOS Safari to test a WebKit based browser but Safari based testing has been limited as I do not own an iOS or macOS device.

## Deployment

The live site is deployed on Heroku with development being carried out on a local machine running a flask server. The live site is automatically built from the master branch of the project here on Github with any active development being pushed to separate feature branches. Once a feature is ready for deployment it is merged with the master branch and the feature branch is deleted. Heroku then detects the change on the master branch and builds the new version of the site on their servers. Environment variables set in the Heroku backend were initially imported using the Heroku CLI and any changes or additions then being made using the Heroku Dashboard. Environment variables used on the local machine are stored in a config file with the files location being an environment variable itself. To differentiate between the two, the flask app looks for the 'DEPLOYED' environment variable, if it is set then the rest of the variables are set in flask and debug is set to False, otherwise it looks for the config file on the local machine and sets debug to True.


## Resources and Media
The bulk of learning and referencing for this project used either Code Institute lessons, the Flask documentation or W3schools examples and lessons as well as any specific libraries documentation. Beyond that, any issues that could not be solved using the above resources were mostly found on Stack Overflow. A list of links to any code snippets or significant references that were used in the project can be found below:

<details>
    <summary>Design Recourses</summary>
        <ul>
            <li>https://www.furtherfood.com/submitrecipe/</li>
            <li>https://www.bbcgoodfood.com/</li>
            <li>https://tastesbetterfromscratch.com</li>
            <li>https://www.allrecipes.com</li>
            <li>https://www.facebook.com/</li>
            <li>https://www.thingiverse.com/</li>
            <li>https://www.instructables.com/</li>
            <li>https://www.nexusmods.com/mods/</li>
        </ul>
</details>

<details>
    <summary>Documentation and Tutorials</summary>
        <ul>
            <li>https://www.w3schools.com/</li>
            <li>https://getbootstrap.com/docs/4.3/</li>
            <li>https://fontawesome.com/</li>
            <li>https://docs.mongodb.com/</li>
            <li>https://select2.org/</li>
            <li>https://flask-pymongo.readthedocs.io/en/latest/</li>
            <li>https://api.jquery.com/</li>
            <li>https://developers.google.com/custom-search/docs/element</li>
            <li>https://developers.google.com/custom-search/v1/introduction</li>
            <li>http://api.mongodb.com/python/current/tutorial.html</li>
            <li>http://flask.pocoo.org/docs/1.0/tutorial/</li>
            <li>http://flask.pocoo.org/docs/0.12/patterns/flashing/</li>
            <li>https://pythonise.com/feed/flask/flask-message-flashing</li>
            <li>https://pythonprogramming.net/jquery-flask-tutorial/</li>
            <li>https://www.sitesell.com/blog/2017/02/recipe-schema.htmlkno</li>
            <li>https://www.w3schools.com/css/css_tooltip.asp</li>
            <li>https://devinpractice.com/2019/03/25/flask-mongodb-tutorial/</li>
            <li>https://www.tutorialspoint.com/flask/flask_sessions.htm</li>
            <li>http://flask.pocoo.org/snippets/54/</li>
            <li>https://medium.com/@egealpay1/flask-user-authentication-1eda0af6016c</li>
            <li>https://stackoverflow.com/questions/1860482/when-do-you-choose-to-load-your-javascript-at-the-bottom-of-the-page-instead-of</li>
            <li>https://overiq.com/flask-101/authentication-in-flask/</li>
            <li>https://pythonspot.com/login-authentication-with-flask/</li>
            <li>https://infinidum.com/2018/08/18/making-a-simple-login-system-with-flask-login/</li>
            <li>https://stackoverflow.com/questions/36835615/difference-between-input-group-and-form-group</li>
            <li>https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog</li>
            <li>https://infinite-scroll.com/api.html</li>
            <li>https://flask.palletsprojects.com/en/1.1.x/security/</li>
            <li>https://www.idiotinside.com/2015/05/10/python-auto-generate-requirements-txt/</li>
            <li>https://security.openstack.org/guidelines/dg_cross-site-scripting-xss.html</li>
            <li>https://medium.com/@abderrahman.hamila/what-sanitize-mean-and-why-sanitize-in-code-data-5c68c9f76164</li>
            <li>https://medium.com/@smirnov.am/securing-flask-web-applications-f877e374b427</li>
            <li>https://stackoverflow.com/questions/43925397/what-is-the-best-way-to-sanitize-inputs-with-flask-and-when-using-mongodb</li>
            <li>https://pythonhosted.org/Flask-Mail/</li>
            <li>https://stackoverflow.com/questions/43728500/python-flask-e-mail-form-example</li>
        </ul>
</details>

<details>
    <summary>Libraries</summary>
        <ul>
            <li>https://github.com/select2/select2</li>
            <li>https://github.com/metafizzy/infinite-scroll</li>
            <li>https://github.com/tempusdominus/bootstrap-4</li>
            <li>https://github.com/gromo/jquery.scrollbar</li>
            <li>https://github.com/ttskch/select2-bootstrap4-theme</li>
            <li>https://github.com/select2/select2-bootstrap-theme</li>
        </ul>
</details>

<details>
    <summary>Code Snippets</summary>
        <ul>
            <li>https://stackoverflow.com/questions/7271482/getting-a-list-of-values-from-a-list-of-dicts</li>
            <li>https://www.codeproject.com/Questions/1185082/How-to-create-input-field-with-a-button-click</li>
            <li>http://jsfiddle.net/omugbdm1/3/</li>
            <li>https://stackoverflow.com/questions/7020659/submit-form-using-a-button-outside-the-form-tag</li>
            <li>https://ux.stackexchange.com/questions/58302/error-message-for-invalid-username</li>
            <li>https://stackoverflow.com/questions/3736553/how-to-execute-function-after-image-is-loaded-into-a-div-with-jquery</li>
            <li>https://stackoverflow.com/questions/51404129/how-to-access-external-javascript-files-through-jinjaflask/51405432</li>
            <li>https://stackoverflow.com/questions/11178426/how-can-i-pass-data-from-flask-to-javascript-in-a-template/42158426</li>
            <li>https://stackoverflow.com/questions/16310918/css-scale-and-square-center-crop-image</li>
            <li>https://coderwall.com/p/ijrrpa/flask-flash-messages-as-bootstrap-alert</li>
            <li>https://webdesign.tutsplus.com/tutorials/a-simple-javascript-technique-for-filling-star-ratings--cms-29450</li>
            <li>https://codepen.io/jexordexan/pen/yyYEJa</li>
            <li>https://github.com/philsturgeon/codeigniter-template/blob/master/user_guide/changelog.html</li>
            <li>https://stackoverflow.com/questions/18775074/recreate-3-column-facebook-style-parcial-scrolling-then-fixed-position-css</li>
            <li>https://stackoverflow.com/questions/3666953/showing-git-branch-structure</li>
            <li>https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging</li>
            <li>https://git-scm.com/book/en/v1/Git-Tools-Stashing</li>
            <li>https://medium.com/datadriveninvestor/git-rebase-vs-merge-cc5199edd77c</li>
            <li>https://stackoverflow.com/questions/5340724/get-changes-from-master-into-branch-in-git</li>
        </ul>
</details>

<details>
    <summary>Conventions and Style Guides</summary>
        <ul>
            <li>https://stackoverflow.com/questions/3736553/how-to-execute-function-after-image-is-loaded-into-a-div-with-jquery</li>
            <li>https://google.github.io/styleguide/htmlcssguide.html#ID_and_Class_Name_Delimiters</li>
            <li>https://www.webfx.com/blog/web-design/20-html-best-practices-you-should-follow/</li>
            <li>https://code.tutsplus.com/tutorials/30-css-best-practices-for-beginners--net-6741</li>
            <li>https://code.tutsplus.com/tutorials/24-javascript-best-practices-for-beginners--net-5399</li>
            <li>https://gist.github.com/sloria/7001839</li>
            <li>https://keepachangelog.com/en/1.0.0/</li>
            <li>https://moz.com/blog/the-ultimate-guide-to-the-google-search-parameters</li>
            <li>https://uxdesign.cc/death-to-complexity-how-we-simplified-advanced-search-a9ab2940acf0</li>
            <li>https://dribbble.com/tags/advanced_search</li>
            <li>https://uxplanet.org/how-to-improve-advanced-search-ux-450df698004c</li>
            <li>https://stackoverflow.com/questions/6028211/what-is-the-standard-naming-convention-for-html-css-ids-and-classes</li>
        </ul>
</details>

<details>
    <summary>Recipes</summary>
        <ul>
            <li>https://www.bbcgoodfood.com/recipes/2060/easy-white-bread</li>
            <li>http://www.donalskehan.com/recipes/soda-bread/</li>
            <li>https://www.bbcgoodfood.com/recipes/1223/bestever-brownies</li>
            <li>https://www.jamieoliver.com/recipes/eggs-recipes/omelette/</li>
            <li>https://www.bbcgoodfood.com/recipes/dippy-eggs-marmite-soldiers</li>
            <li>https://www.safefood.eu/Recipes/Desserts/Fresh-fruit-salad.aspx</li>
            <li>https://thestayathomechef.com/pot-roast/</li>
            <li>https://www.jamieoliver.com/recipes/chicken-recipes/perfect-roast-chicken/</li>
            <li>https://www.bbcgoodfood.com/recipes/easy-chocolate-cake</li>
        </ul>
</details>


<details>
    <summary>Icon Credit</summary>
    <ul>
        <li>
            <div>
                Icons made by
                <a href="https://www.freepik.com/" title="Freepik">Freepik</a>
                from
                <a href="https://www.flaticon.com/" title="Flaticon"
                    >www.flaticon.com</a
                >
                is licensed by
                <a
                    href="http://creativecommons.org/licenses/by/3.0/"
                    title="Creative Commons BY 3.0"
                    target="_blank"
                    >CC 3.0 BY</a
                >
            </div>
        </li>
    </ul>
</details>

## Linter Errors

Below you will find any errors that remained after running the linters [HTML-Tidy](https://packagecontrol.io/packages/SublimeLinter-html-tidy), [CSSLint](https://packagecontrol.io/packages/SublimeLinter-csslint), [JSHint](https://packagecontrol.io/packages/SublimeLinter-jshint), and [flake8](https://packagecontrol.io/packages/SublimeLinter-flake8). The errors experienced in index.html and search.html are from an issue when using a Jinja input in inline JavaScript. On those pages if you search for and replace the variable {{pagemax}} with a number there are no further errors. Any other errors or warnings found that are not included here I was unaware of or did not occur on the development machine.

<details>
    <summary>app.py</summary>
    <ul>
        <li><code>156:80  warning  flake8:E501  line too long (81 > 79 characters)</code></li>
    </ul>
</details>
<details>
    <summary>static/css/style.css</summary>
    <ul>
        <li><code> 65:3  warning  csslint:Warning  Don't use IDs in selectors. (ids)</code></li>
        <li><code>144:3  warning  csslint:Warning  Adjoining classes: .btn.focus (adjoining-classes)</code></li>
        <li><code>160:5  warning  csslint:Warning  Using height with border can sometimes make elements larger than you expect. (box-model)</code></li>
        <li><code>160:5  warning  csslint:Warning  Using width with border can sometimes make elements larger than you expect. (box-model)</code></li>
        <li><code>166:3  warning  csslint:Warning  Don't use IDs in selectors. (ids)</code></li>
        <li><code>179:5  warning  csslint:Warning  Using height with border can sometimes make elements larger than you expect. (box-model)</code></li>
        <li><code>179:5  warning  csslint:Warning  Using width with border can sometimes make elements larger than you expect. (box-model)</code></li>
        <li><code>215:5  warning  csslint:Warning  Use of !important (important)</code></li>
        <li><code>239:3  warning  csslint:Warning  Don't use IDs in selectors. (ids)</code></li>
        <li><code>250:3  warning  csslint:Warning  Don't use IDs in selectors. (ids)</code></li>
        <li><code>254:3  warning  csslint:Warning  Don't use IDs in selectors. (ids)</code></li>
        <li><code>266:3  warning  csslint:Warning  Don't use IDs in selectors. (ids)</code></li>
        <li><code>324:5  warning  csslint:Warning  Don't use IDs in selectors. (ids)</code></li>
        <li><code>325:7  warning  csslint:Warning  Use of !important (important)</code></li>
        <li><code>342:5  warning  csslint:Warning  Using height with border can sometimes make elements larger than you expect. (box-model)</code></li>
        <li><code>342:5  warning  csslint:Warning  Using width with border can sometimes make elements larger than you expect. (box-model)</code></li>
    </ul>
</details>
<details>
    <summary>static/js/form.js</summary>
    <ul>
        <li><code>232:33  warning  jshint:W083  Functions declared within loops referencing an outer scoped variable may lead to confusing semantics. (fitImage, $)</code></li>
    </ul>
</details>
<details>
    <summary>templates/index.html</summary>
    <ul>
        <li><code>105:29  error    jshint:E020  Expected '}' to match '{' from line 4 and instead saw '{'.</code></li>
        <li><code>105:30  error    jshint:E020  Expected ')' to match '(' from line 4 and instead saw 'pagemax'.</code></li>
        <li><code>105:37  error    jshint:E030  Expected an identifier and instead saw '}'.</code></li>
        <li><code>105:37  warning  jshint:W030  Expected an assignment or function call and instead saw an expression.</code></li>
        <li><code>105:38  warning  jshint:W033  Missing semicolon.</code></li>
        <li><code>105:39  error    jshint:E020  Expected '}' to match '{' from line 1 and instead saw ')'.</code></li>
        <li><code>105:40  error    jshint:E021  Expected ')' and instead saw '{'.</code></li>
        <li><code>105:41  warning  jshint:W033  Missing semicolon.</code></li>
        <li><code>106:24  error    jshint:E041  Unrecoverable syntax error. (17% scanned).</code></li>
    </ul>
</details>
<details>
    <summary>templates/search.html</summary>
    <ul>
        <li><code>125:20  error    jshint:E020  Expected '}' to match '{' from line 1 and instead saw '{'.</code></li>
        <li><code>125:21  error    jshint:E058  Missing semicolon.</code></li>
        <li><code>125:21  warning  jshint:W030  Expected an assignment or function call and instead saw an expression.</code></li>
        <li><code>125:21  error    jshint:E041  Unrecoverable syntax error. (50% scanned).</code></li>
        <li><code>125:28  warning  jshint:W033  Missing semicolon.</code></li>
    </ul>
</details>
<!--

TODO List:
Add - Test out mobile view

DONE List:
Add - search page with results and stuff
Add - Logout Button in both mobile and desktop view
Fix - Stop the user voting on a recipe multiple times, that's just not fair
Add - Coming soon popups to some things that are not working
Fix - Change the mongodb to use the new fresh database and add a bunch of sample recipes to the database
Fix - Comments on the home page all open when one button is clicked, generally having multiple recipe cards needs to be fixed on the home page

NEVER List:
Fix - Popups like coming soon or the star rating on mobile only go away when you tap elsewhere on the screen, it mean they get in the way when voting on a recipe so they need to timeout when tapped.
Add - Implement advanced search result filtering (a bunch more recipes need to be added before this can be done)
Add - Category exploring page where recipes are grouped by cuisine or time
Add - Link to forgotten password form
Add - Stop sudo duplicates being added to the activity feed
Fix - fitimage sometimes needs to be reloaded for it to work correctly, find out why it does not load the first time (probably something to do with callbacks)
Fix - Add placeholder image if recipe image does not load
Fix - Handle the way that unitless ingredients are displayed

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

Just to recap quickly:

1. Finish user profile
2. Create a template for an individual recipe
3. Create homepage to list all recipes w/ links to individual recipe page for each
4. On user profile page add edit/delete button for each recipe, and possibly on individual recipe page if user owns that recipe
5. Write delete route/function -> @app.route('/delete/<recipe_id>/)
6. Write update route/function -> @app.route('/update/<recipe_id>/')
7. Create update recipe template w/ pre-filled form for user to update recipe, or add ability to edit inline on the user profile/recipe page and POST to the URL with javascript

files=`git diff --name-only`
for file in $files; do
  echo "--------------------------------"
  git diff $file > "$file.txt"
done

-->