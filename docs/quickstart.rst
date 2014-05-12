.. _quickstart:
.. module:: flask.ext.stormpath


Quickstart
==========

Now that we've got all the prerequisites out of the way, let's take a look at
some code!  Integrating Flask-Stormpath into an application can take as little
as 1 minute!


Initialize Flask-Stormpath
--------------------------

To initialize Flask-Stormpath, you need to create a
:class:`StormpathManager` and provide some Flask settings.

You can do this in one of two ways:

1. Pass your Flask app into the :class:`StormpathManager` directly::

    from flask.ext.stormpath import StormpathManager

    app = Flask(__name__)
    stormpath_manager = StormpathManager(app)

2. Lazily initialize your :class:`StormpathManager` (this is useful if you have
   a factory function creating your Flask application)::

    from flask.ext.stormpath import StormpathManager

    stormpath_manager = StormpathManager()

    # some code which creates your app
    stormpath_manager.init_app(app)


Specify Your Credentials
------------------------

Now that you have your manager configured, you need to supply some basic
configuration variables to make things work::

    app.config['SECRET_KEY'] = 'someprivatestringhere'
    app.config['STORMPATH_API_KEYFILE'] = '/path/to/apiKey.properties'
    app.config['STORMPATH_APPLICATION'] = 'myapp'

Or, if you prefer to use environment variables to specify your credentials, you
can do that easily as well::

    from os import environ

    app.config['SECRET_KEY'] = 'someprivatestringhere'
    app.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
    app.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')
    app.config['STORMPATH_APPLICATION'] = environ.get('STORMPATH_APPLICATION')


.. note::
    The ``STORMPATH_API_KEY_ID`` and ``STORMPATH_API_KEY_SECRET`` variables can
    be found in the ``apiKey.properties`` file you downloaded in the previous
    step.

    The ``STORMPATH_APPLICATION`` variable should be the name of your Stormpath
    application created above.  "dronewars", for instance.

.. note::
    **Please don't hardcode your API key information into your source code!**
    To keep your credentials safe and secret, we recommend storing these
    credentials in environment variables.


Testing It Out
--------------

If you followed the two steps above, you will now have fully functional
registration, login, and logout functionality active on your site!

Don't believe me?  Test it out!  Start up your Flask web server now, and I'll
walk you through the basics:

- Navigate to ``/register``.  You will see a registration page.  Go ahead and
  enter some information.  You should be able to create a user account.  Once
  you've created a user account, you'll be automatically logged in, then
  redirected back to the root URL (``/``, by default).
- Navigate to ``/logout``.  You will now be logged out of your account, then
  redirected back to the root URL (``/``, by default).
- Navigate to ``/login``.  You will see a login page.  You can now re-enter
  your user credentials and log into the site again.

Wasn't that easy?!

.. note::
    You probably noticed that you couldn't register a user account without
    specifying a sufficiently strong password.  This is because, by default,
    Stormpath enforces certain password strength rules on your Stormpath
    Directories.

    If you'd like to change these password strength rules (or disable them), you
    can do so easily by visiting the `Stormpath dashboard`_, navigating to your
    user Directory, then changing the "Password Strength Policy".


Customize the User Registration Fields
--------------------------------------

Now that we've seen how easy it is to register, login, and logout users in your
Flask app, let's customize the fields we ask for when a user registers.

Every user you register ends up getting stored in Stormpath as an `Account`_
object.  Accounts in Stormpath have several fields you can set:

- username
- email (**required**)
- password (**required**)
- given_name (**required**) also known as 'first name'
- middle_name
- surname (**required**) also known as 'last name'

By default, the built-in registration view that Flask-Stormpath ships with gets
you a registration page that looks like this:

.. image:: /_static/registration-page.png

As you can see, it includes the ``given_name``, ``middle_name``, ``surname``,
``email``, and ``password`` fields by default.  All of these fields are
required, with the exception of ``middle_name``.

What happens if a user enters an invalid value -- or leaves a required field
blank?  They'll see something like this:

.. image:: /_static/registration-page-error.png

But what if you want to force the user to enter a value for middle name?  Doing
so is easy!  Flask-Stormpath is **highly customizable**, and allows you to
easily control which fields are accepted, and which fields are required.

To require a user to enter a middle name field, set the following value in your
Flask app config::

    app.config['STORMPATH_REQUIRE_MIDDLE_NAME'] = True

Now go ahead and give it a try -- if you attempt to create a new user and don't
specify a middle name, you'll see an error!

But what if you wanted to only accept ``email`` and ``password``?  By using the
``STORMPATH_ENABLE_*`` and ``STORMPATH_REQUIRE_*`` settings in your Flask app,
you can completely customize which fields are accepted (*and required*)!
Now, remove the ``STORMPATH_REQUIRE_MIDDLE_NAME`` setting and add the following in
its place::

    app.config['STORMPATH_ENABLE_GIVEN_NAME'] = False
    app.config['STORMPATH_ENABLE_MIDDLE_NAME'] = False
    app.config['STORMPATH_ENABLE_SURNAME'] = False

If you refresh the registration page, you'll now see a form that only accepts
``email`` and ``password``!  Not bad, right?

.. note::
    If you explicitly disable the ``given_name`` and ``surname`` fields as shown
    above, those fields will automatically receive the value ``'Anonymous'`` (as
    they are required by Stormpath).

    We're currently working to make these fields optional on Stormpath's side.

Want to keep everything as default, except make first and last name optional for
the user?  All you'd have to do is::

    app.config['STORMPATH_REQUIRE_GIVEN_NAME'] = False
    app.config['STORMPATH_REQUIRE_SURNAME'] = False

Lastly, it's also simple to add in a ``username`` field (either required or
optional).  Just like the examples above, you can use the ``ENABLE`` and
``REQUIRE`` settings to control the registration behavior::

    app.config['STORMPATH_ENABLE_USERNAME'] = True
    app.config['STORMPATH_REQUIRE_USERNAME'] = False

And that's it!


Step 2: Create a User Registration Template
...........................................

The next step (for most people) is to build a user registration template, which
allows new users to sign up for your website.  In the example below, I'll show
you a simple, standalone HTML template which allows users to register for your
website by specifying a few fields:

- First Name
- Last Name
- Email
- Password

Here's the code (this file should be saved as `register.html` and placed inside
the `templates` directory in your Flask application)::

    <html>
      <head>
        <title>Create an Account</title>
      </head>
      <body>
        {% if error %}
          <p>{{ error }}</p>
        {% endif %}
        <form action="" method="post">
          <fieldset>
            <legend>Create an Account</legend>
            <label for="first-name">First Name</label>
            <input type="text" name="first-name" placeholder="First Name">
            <label for="last-name">Last Name</label>
            <input type="text" name="last-name" placeholder="Last Name">
            <label for="email">Email</label>
            <input type="email" name="email" placeholder="Email">
            <label for="password">Password</label>
            <input type="password" name="password" placeholder="Password">
            <input type="submit" name="Register">
          </fieldset>
        </form>
      </body>
    </html>

This simple template allows you to collect several pieces of user data that
we'll use in the next step to create a new user account.


Step 3: Create a Registration View
..................................

Now that you have a registration template, let's write our Flask view!

The example code below shows a simple `register` view which renders the
`register.html` template we created in the previous step, then uses the
user-supplied form data to create a new Stormpath user, log this user into their
new account, and send them to a dashboard page (which we have yet to code!)::

    from flask import (
        Flask,
        redirect,
        render_template,
        request,
        url_for,
    )

    from flask.ext.stormpath import (
        StormpathError,
        StormpathManager,
        User,
        login_user,
    )

    # ...

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Allow users to register for the site."""
        if request.method == 'GET':
            return render_template('register.html')

        try:
            _user = User.create(
                email = request.form.get('email'),
                password = request.form.get('password'),
                given_name = request.form.get('first-name'),
                surname = request.form.get('last-name'),
            )
        except StormpathError, err:
            return render_template('register.html', error=err.message)

        login_user(_user, remember=True)
        return redirect(url_for('.dashboard'))

.. note::
    In future versions of Flask-Stormpath, user creation will be greatly
    simplified.  This is still an early release.


Step 4: Create a Dashboard Page
...............................

Now that we have a registration view, let's go ahead and build a simple
dashboard page for logged in users.

Below is a simple HTML template, `dashboard.html`, you can use as reference::

    <html>
      <head>
        <title>Dashboard</title>
      </head>
      <body>
        <p>Hello {{ user.given_name }} {{ user.surname }}!</p>
        <p>Your email address is: {{ user.email }}.</p>
        <p>Your favorite web framework is: {{ user.custom_data['favorite_web_framework'] }}.</p
      </body>
    </html>

We'll also create a simple Flask view which renders this template, and restricts
access to this page to logged in users::

    from flask.ext.stormpath import (
        login_required,
        user,
    )

    # ...

    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Render a dashboard page for logged in users."""

        # Store some custom data in our user's account.
        user.custom_data['favorite_web_framework'] = 'Flask'
        user.save()

        return render_template('dashboard.html')

There are a few things to note here:

- You can use the `login_required` decorator to ensure that only logged in users
  can view a page.

- Your templates will automatically have access to a special `user` variable.
  This variable allows you to access the current user's User object directly.
  Want more information on a User object?  See the official Stormpath Python SDK
  documentation: https://github.com/stormpath/stormpath-sdk-python

- If a public visitor tries to access the dashboard page directly, they'll be
  redirected to the login page where they'll be prompted for their credentials
  (more on this later).

- We're storing custom data with this user account using Stormpath's custom data
  feature.  Stormpath allows you to store up to 10MB of data per user account.

- Stormpath's custom data is a key-value store behind the scenes (Cassandra),
  which allows you to store any type of data (including complex nested JSON
  documents).


Step 5: Create a Login Page
...........................

Now that we've got a registration page and dashboard page, let's go ahead and
create a simple login page for existing users.

What we'll do here is ask for a user's email and password, then securely log
this user in with Stormpath behind the scenes.

Below is a simple `login.html` template you can use as a reference::

    <html>
      <head>
        <title>Login</title>
      </head>
      <body>
        {% if error %}
          <p>{{ error }}</p>
        {% endif %}
        <form action="" method="post">
          <fieldset>
            <legend>Login</legend>
            <label for="email">Email</label>
            <input type="email" name="email" placeholder="Email">
            <label for="password">Password</label>
            <input type="password" name="password" placeholder="Password">
            <input type="submit" name="Login">
          </fieldset>
        </form>
      </body>
    </html>

Here's a matching login view you can use, which handles the login process
seamlessly::

    # ...

    # Map our custom login view to Flask-Stormpath.
    stormpath_manager.login_view = 'login'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Allow users to log into the site."""
        if request.method == 'GET':
            return render_template('login.html')

        try:
            _user = User.from_login(
                request.form.get('email'),
                request.form.get('password'),
            )
        except StormpathError, err:
            return render_template('login.html', error=err.message)

        login_user(_user, remember=True)
        return redirect(request.args.get('next') or url_for('.dashboard'))

If the user logs in successfully, they'll be redirected to either the page they
were trying to get to, or the dashboard page (default).

By assigning our login view to `stormpath_manager.login_view`, we're telling
Flask-Stormpath to use this view we just created to log users into their
accounts.  This way, if a user tries to visit a page that requires login, the
user will be redirected to `/login` automatically.


Step 6: Create a Logout View
............................

Now that we've handled registration, login, and dashboard functionality, let's
go ahead and build a logout view that users can use to log out of your website.

Below is an example Flask view which does just this::

    from flask.ext.stormpath import logout_user

    # ...

    @app.route('/logout')
    def logout():
        """Log a user out of their account."""
        logout_user()
        return redirect(url_for('.index'))

After the user has been logged out, we'll redirect the user to the home page of
the website (which we have yet to create).


Step 7: Create a Home Page
..........................

The last thing we'll want to do create a simple home page for our website.
Below is a simple `index.html` template which provides links to the registration
and login pages::

    <html>
      <head>
        <title>Home</title>
      </head>
      <body>
        <h1>Welcome!</h1>
        <a href="{{ url_for('.register') }}">Register</a><br />
        <a href="{{ url_for('.login') }}">Login</a>
      </body>
    </html>

And of course, here's a simple Flask view you can use to render this page::

    @app.route('/')
    def index():
        """Render the home page."""
        return render_template('index.html')

That's it!


Testing Things Out
..................

Now that you've integrated Flask-Stormpath into your application, give it a try!
Run your Flask development server, visit the index page, create a new account,
log into your account, view the dashboard page, and try visiting the logout page
(`/logout`).

Not bad, right?


How Do I ... ?
--------------

This section covers common questions that come up.


Require a User to be in a Group
...............................

If you'd like to force a user to be a member of a group (or groups) before the
user is allowed to access a view, you can do so using the `groups_required`
decorator::

    from flask.ext.stormpath import groups_requied

    # ...

    @app.route('/admins_only')
    @groups_required(['admins'])
    def admins_only():
        """A top-secret view only accessible to admins."""
        # ...

If you'd like to force a user to be a member of multiple groups, just list all
the groups::

    from flask.ext.stormpath import groups_requied

    # ...

    @app.route('/admins_only')
    @groups_required(['admins', 'super_admins'])
    def admins_only():
        """A top-secret view only accessible to admins (and super-admins)."""
        # ...

Lastly, if you'd like to just make sure a user is a member of at least ONE type
of group, you can also do that by setting the optional `all` parameter to
false::

    from flask.ext.stormpath import groups_requied

    # ...

    @app.route('/dashboard')
    @groups_required(['free-users', 'paid-users', 'admins'], all=False)
    def dashboard():
        """A user dashboard viewable by free users, paid users, or admins."""
        # ...


Future Features
---------------

In the future, Flask-Stormpath will support a great deal more functionality,
including multi-tenant applications, groups of users ('admins', 'superusers',
etc.), and all sorts of complex user authentication use cases.

As new versions of this library are released, we'll be updating this
documentation to demonstrate how to use the latest and greatest features.


.. _Stormpath dashboard: https://api.stormpath.com/ui/dashboard
.. _Account: http://docs.stormpath.com/rest/product-guide/#accounts
