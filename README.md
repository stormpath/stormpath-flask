# stormpath-flask

Build simple, secure web applications with Stormpath and Flask!

[![Build Status](https://travis-ci.org/stormpath/stormpath-flask.png?branch=master)](https://travis-ci.org/stormpath/stormpath-flask)


**NOTE**: This library is an early release.  It's currently lacking many
features, and only handles basic use cases.  We're working on adding lots of
cool stuff to the library which will improve it's general usefulness.  If you
have feedback, please get in touch and share your thoughts!
[randall@stormpath.com](mailto:randall@stormpath.com)


## What is Stormpath?

Stormpath (https://stormpath.com) is an API service which allows you to securely
create, manage, and scale user accounts for your applications.

If you don't already have a Stormpath account, you can create one here:
https://api.stormpath.com/register


## Purpose

This library can be used to:

- Easily add user authentication and authorization into your Flask web
  applications in a secure manner, without the need of any custom user
  management code: no users table, no user management, etc.

- Easily register and authenticate users.

- Scale your application by offloading user scaling requirements to the
  Stormpath service.

- Easily store and retrieve custom user data using JSON.

If you're building a Flask web application and would like to easily (*and
securely!*) handle user management, look no further.  Stormpath is the best of
the best, and provides you with a full fledged API service capable of handling
complex user authentication and authorization use cases, scaling to millions of
requests (and beyond!), and storing and retrieving custom user data.

Stormpath makes it easy to build user-facing applications.


## Installation

To install this library, you'll need [Pip](http://pip.readthedocs.org/en/latest/).

Once you have `pip` installed, install `Flask-Stormpath`:

```bash
$ pip install -U Flask-Stormpath
```

This will pull in all dependencies (including the latest Flask release).


## Usage

Once you have `Flask-Stormpath` installed, using it is simple.  The first thing
you'll want to do is import the libraries somewhere in your Flask application:

```python
from flask import redirect, render_template
from flask.ext.stormpath import (
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
)
from stormpath.error import Error as StormpathError
```

Next, you'll want to initialize your own `StormpathManager` instance -- this
will configure [Flask-Login](http://flask-login.readthedocs.org/en/latest/) on
the backend, and provide you with secure session management.

```python
stormpath_manager = StormpathManager(app)
stormpath_manager.login_view = '.login'
```

Next, you'll want to create a view which logs users into your Flask application
(assuming you want to have users log in via a web page somewhere).  To do this,
you can use the view below (a simple example):

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    try:
        _user = User.from_login(
            request.form.get('email'),
            request.form.get('password'),
        )
    except StormpathError:
        return render_template('login.html', error='Invalid credentials.')

    login_user(_user, remember=True)
    return redirect(request.args.get('next') or url_for('.index'))
```

The above code snippet will log a user in given a login page at `/login`.  There
are three important things that happen above, which are worth mentioning:

1. When we call `User.from_login` method, we're taking the user-supplied
   credentials (either an email address or user name, and a password), and
   checking with Stormpath's API service to see whether or not these credentials
   are valid.  If they are, we'll get a User object back, and if not, an
   exception will be raised.

2. When we call `login_user`, we're transparently creating a session behind the
   scenes, which keeps this user logged in for a while, until either the user
   logs out of the site, or the session expires.

3. Once the login has been accepted, we'll redirect users to the page they were
   trying to get to when they hit this login page, or simply redirect them to
   the 'index' view (usually a home page).

The above view can be customized for your application / use case, but is fairly
flexible.

Now that you've got a login view setup and configured, let's take a look at how
to access a user's information once a user has been logged in.  Below is an
example view, called 'dashboard', which prints some user data to the console:


```python
@app.route('/dashboard')
@login_required
def dashboard():
    print 'Current user:', user.given_name, user.surname, user.email
    return render_template('dashboard.html')
```

Once you've imported `flask.ext.stormpath.user`, a `user` object will be
available to all views which require authentication to access (notice the
`@login_required` decorator).

Once you have the user object, you can do all sorts of stuff, including modify
user data:

```python
@app.route('/dashboard')
@login_required
def dashboard():
    user.given_name = 'Randall'
    user.surname = 'Degges'
    user.custom_data['birthday'] = '06/28/1988'
    user.custom_data['banks'] = [
        {
            'name': 'Ally',
            'account_number': 'XXX',
        },
        {
            'name': 'Bank of America',
            'account_number': 'xxx',
        },
    ]

    # Save these user changes to Stormpath.
    user.save()

    return render_template('dashboard.html')
```

You can also access the `user` variable in all templates by default, for
instance, let's say you have a template named `dashboard.html`, you could do the
following:

```html
<p>Hi, {{ user.given_name }}. Your birthday is {{ user.custom_data['birthday'] }}.</p>
```

Without doing anything special!

Lastly, you can easily log users out of their accounts by calling the
`logout_user` helper:

```
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
```

This will log the current user out of their account -- simple!


## Sample Application

There is a simple sample application in development which you can find on
GitHub here: https://github.com/stormpath/stormpath-flask-sample

This application provides a simple local web server that allows you to create
users, log them in, log them out, etc.

You can use this as a reference for implementing `Flask-Stormpath` into your
Flask projects.


## Backend

This library is largely based on the excellent
[Flask-Login](http://flask-login.readthedocs.org/en/latest/) library.  Most
functionality is piggybacked off this library, including secure user sessions /
etc.

Right now we're rapidly developing this library to make it easy for Flask
developers to add user authentication to their projects without the complication
that comes along with it.

If you have features or suggestions, please let me know!
[randall@stormpath.com](mailto:randall@stormpath.com)


## Changelog

All library changes, in descending order.


### Version 0.0.1

Released on February 17, 2014.

- First release!
- Basic functionality.
- Basic docs.
- Lots to do!
