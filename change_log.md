-----------------models.py Changes-------------------
User image_url and header_image_url -> not nullable

Added session.commit to User signup method

Added autoincrement=True to message id column and user id column

Added nullable=False and default='' to user.bio


-----------------style/sheets Changes-------------------

Added navbar styling for buttons and their hover. -> style.css

-----------------app.py Changes-------------------

Changed template to create.html for add_message().


-----------------templates/users Changes-------------------
Added each followed_user bio to card-bio -> following.html

Added each follower bio to card-bio -> followers.html

Added user bio to user detail page -> detail.html

Added inline styling for header image -> detail.html

Added user bio to users page and search -> index.html


-----------------templates Changes-------------------

Added form for logout POST request. Updated styling classes. -> base.html


-----------------Notes-------------------

Uncertain method for ordering messages on individual user page (users/show.html)


-----------------Understanding Login Strategy-------------------
Logged in user is being tracked in the session and then loaded into the g object everytime a request is made.

The g object is a way to store information that the request can then access. It does not persist across requests.

add_user_to_g is a view function that gets the current user from the session and stores it in g. This creates easy access/reference to the current user.

@app.before_request runs before every request, it acts as a setup for the request and does the authentication before the view function is called

