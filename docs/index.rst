.. Flask-Stormpath documentation master file, created by
   sphinx-quickstart on Tue Feb 18 11:24:11 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Flask-Stormpath
===============

.. currentmodule:: flask.ext.stormpath


*User management and authentication made easy.*

Hi there, and thanks for checking out Flask-Stormpath!

Flask-Stormpath is a library which aims to make it incredibly easy to add user
management, authentication, and authorization into your Flask web applications
with very little work!

If you're not already familiar with `Stormpath <https://stormpath.com>`_ you
might want to visit their site and get acquainted with them.

Stormpath is an API company which securely handles user accounts (and custom
user data) in a fast, secure, and effective way.

This library plugs Stormpath into your Flask application, making it simple to
handle users and their data.


Why You Might Want to Use Stormpath
-----------------------------------

Stormpath is a great service, but it's not for everyone.

You might want to use Stormpath if:

- User security is a top priority.
- Scaling your userbase is a potential problem (Stormpath handles scaling your
  users completely).
- You need to store custom user data along with your user's basic information
  (email, password).
- You would like to have automatic email verification for new user accounts.
- You would like to configure and customize password strength rules.
- You'd like to keep your user data separate from your other applications to
  increase platform stability / availability.
- You are building a service oriented application, in which multiple
  independent services need access to the same user data.
- You are a big organization who would like to use Stormpath, but need to host
  it yourself (Stormpath has an on-premise system you can use internally).

You might **NOT** want to use Stormpath if:

- You are building an application that does not need user accounts.
- Your application is meant for internal-only usage.
- You aren't worried about user data / security much.
- You aren't worried about application availability / redundancy.
- You want to roll your own custom user authentication.

If you don't need Stormpath, you might want to check out `Flask-Login
<http://flask-login.readthedocs.org/en/latest/>`_ (which Flask-Stormpath uses
behind the scenes to handle sessions).

Want to use Stormpath?  OK, great!  Let's get started!


Getting Started with Stormpath
------------------------------

Now that you've decided to use Stormpath, the first thing you'll want to use is
create a new Stormpath account: https://api.stormpath.com/register

Once you've created a new account, create a new API key pair by logging into
your dashboard and clicking the 'Create an API Key' button.  This will generate
a new API key for you, and prompt you to download your keypair.

.. note::
    Please keep the API keypair file you just downloaded safe!  These two keys
    allow you to make Stormpath API requests, and should be properly protected,
    backed up, etc.

Next, you'll want to create a new Stormpath Application.

Stormpath allows you to provision any number of 'Applications'.  The general
rule is that you should create one Application per website.  In this case,
you'll want to create a single Application.

To do this, click the 'Applications' tab in the Stormpath dashboard, then click
'Register an Application' and follow the on-screen instructions.

.. note::
    Use the default options when creating an Application, this way you'll be
    able to create users in your new Application without issue.

Now that you've create an Application, you're completely ready to move on to
plugging Flask-Stormpath into your project!


Installation
------------

To install Flask-Stormpath, you'll need `pip
<http://pip.readthedocs.org/en/latest/>`_.  You can install (or upgrade)
Flask-Stormpath by running::

    $ pip install -U Flask-Stormpath

This will automatically install all project dependencies.

.. note::
    Flask-Stormpath is currently *only* compatible with Python 2.7.  We will be
    adding Python 3 support in the near future.


Configuration
-------------

Once you've got Flask-Stormpath installed, the next thing you need to do is
configure your existing Flask application to work with it.

.. note::
    If you'd like to skip ahead, we've built an entire sample application you
    can download and play with which includes all of the configuration /
    integration we'll be covering throughout this guide.  You can find our
    sample application at: https://github.com/stormpath/stormpath-flask-sample


Step 1: Create a StormpathManager
.................................

The base of all Flask-Stormpath configuration is the `StormpathManager` class.
You can initialize this in one of two ways:

You can either configure it with your Flask app directly::

    from flask.ext.stormpath import StormpathManager

    app = Flask(__name__)
    stormpath_manager = StormpathManager(app)

Or you can lazily initialize your `StormpathManager` (this is useful if you
have a factory function creating your Flask application)::

    from flask.ext.stormpath import StormpathManager

    stormpath_manager = StormpathManager()

    # some code which creates your app
    stormpath_manager.init_app(app)


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
        redirect,
        render_template,
        url_for,
    )

    from flask.ext.stormpath import (
        StormpathError,
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
            _user = stormpath_manager.applications.accounts.create({
                'first_name': request.form.get('first-name'),
                'last_name': request.form.get('last-name'),
                'email': request.form.get('email'),
                'password': request.form.get('password'),
            })
            _user.__class__ = User
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
      </body>
    </html>

We'll also create a simple Flask view which renders this template, and restricts
access to this page to logged in users::

    from flask.ext.stormpath import login_required

    # ...

    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Render a dashboard page for logged in users."""
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
    stormpath_manager.login_view = login

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Allow users to log into the site."""
        if request.method == 'GET':
            return render_template('login.html')

        try:
            _user = User.from_login(
                request.form.get('email'),
                request.form.get('password')
        except StormpathError, err:
            return render_template('login.html', error=err.message)

        login_user(_user, remember=True)
        return redirect(request.args.get('next') or url_for('.dashboard'))

If the user logs in successfully, they'll be redirected to either the page they
were trying to get to, or the dashboard page (default).

By assigning our login view to `stormpath_manager.login_view`, we're telling
Flask-Stormpath to use this view we just created to log users into their
accounts.


Table of Contents

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
