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

The :class:`StormpathManager` is what initializes Stormpath, grabs
configuration information, and manages sessions / user state.  It is the base
of all Flask-Stormpath functionality.


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


Enforce User Authentication
---------------------------

Now that we've seen how easy it is to register, login, and logout users in your
Flask app, let's see how simple it is to restrict views to logged-in users only.

Let's say you have a simple view which should only be accessible to users who
have logged in.  Below is a code sample which shows how easy it is to restrict
access to your view::

    from flask.ext.stormpath import login_required

    @app.route('/secret')
    @login_required
    def secret():
        return 'secret information here'

The :func:`login_required` decorator makes it really easy to enforce user
authentication on your views.

If you try to visit the ``/secret`` URL and you're not logged in, you'll be
redirected to: ``/login?next=%2Fsecret``.  If you then enter your credentials
and log in -- you'll be immediately redirected back to the page you were trying
to access: ``/secret``.


Customize Redirect Logic
------------------------

As you might have already noticed by playing around with the registration and
login pages -- when you first register or log into an account, you'll be
immediately redirected to the URL ``/``.

This is actually a configurable setting -- you can easily modify this default
redirect URL by adding the following config setting::

    app.config['STORMPATH_REDIRECT_URL'] = '/dashboard'

This allows you to build nicer apps as you can do stuff like redirect newly
registered users to a tutorial, dashboard, or something similar.

.. note::
    If a user visits a page which has restricted access, they'll be redirected
    to the login page.  Once the user logs in, they'll be immediately redirected
    back to whatever page they were initially trying to access (this behavior
    overrides the ``STORMPATH_REDIRECT_URL`` setting).


Access User Data
----------------

Let's take a quick look at how we can access user data from a custom view.

Let's say we've defined a simple view that should simply display a user's email
address.  We can make use of the magical :class:`user` context variable to do
this::

    from flask.ext.stormpath import login_required, user

    @app.route('/email')
    @login_required
    def name():
        return user.email

The :class:`user` context allows you to directly interact with the current
:class:`User` model.  This means you can perform *any* action on the
:class:`User` model directly.

For more information on what you can do with a :class:`User` model, please see
the Python SDK documentation: http://docs.stormpath.com/python/product-guide/#accounts

Let's say you want to change a user's ``given_name`` (*first name*).  You could
easily accomplish this with the following code::

    >>> user.given_name = 'Randall'
    >>> user.save()

As you can see above, you can directly modify :class:`User` attributes, then
persist any changes by running ``user.save()``.


Working With Custom User Data
-----------------------------

In addition to managing basic user fields, Stomrpath also allows you to store up
to 10MB of JSON information with each user account!

This could be compared to a user profile.  Instead of defining a database table
for users, and another database table for user profile information -- with
Stormpath you don't need either!

Let's take a look at how easy it is to store custom data on a :class:`User`
model::

    >>> user.custom_data['somefield'] = 'somevalue'
    >>> user.custom_data['anotherfield'] = {'json': 'data'}
    >>> user.custom_data['woot'] = 10.202223
    >>> user.save()

    >>> user.custom_data['woot']
    10.202223

    >>> del user.custom_data['woot']
    >>> user.save()

    >>> user.custom_data['woot']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'woot'

As you can see above -- storing custom information on a :class:`User` account is
extremely simple!


Customize User Registration Fields
----------------------------------

In many cases you might want to change the fields you collect when a user
registers.  Let's customize the fields we ask for when a user registers!

Every user you register ends up getting stored in Stormpath as an `Account`_
object.  Accounts in Stormpath have several fields you can set:

- username
- email (**required**)
- password (**required**)
- given_name (**required**) also known as "first name"
- middle_name
- surname (**required**) also known as "last name"

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


Customize User Login Fields
---------------------------

If you visit your login page (``/login``), you will see (*by default*), two
input boxes: one for ``email`` and one for ``password``.

While this is fine for most purposes, sometimes you might want to let users log
in with a ``username`` **or** ``email`` (especially if your site collects
``username`` during registration).

Doing this is simple: by enabling the ``STORMPATH_ENABLE_USERNAME`` setting
you'll not only make the ``username`` field available on the registration page,
but also on the login page (so users can log in by entering either their
``username`` or ``email`` and ``password``).

To enable ``username`` support, just set the following config variable::

    app.config['STORMPATH_ENABLE_USERNAME'] = True

You should now see the following on your login page:

.. image:: /_static/login-page.png

.. note::
    In the example above we didn't set the ``STORMPATH_REQUIRE_USERNAME`` field
    to ``True`` -- if we did, this would ensure that when a new user registers
    for the site, they **must** pick a ``username``.

    The ``STORMPATH_REQUIRE_USERNAME`` field has no effect on the login page.


Customize User Registration, Login, and Logout Routes
-----------------------------------------------------

By default, Flask-Stormpath automatically enables three separate views and
routes:

- ``/register`` - the registration view
- ``/login`` - the login view
- ``/logout`` - the logout view

Customizing the built-in URL routes is quite simple.  There are several config
variables you can change to control these URL mappings.  To change them, just
modify your app's config.

- ``STORMPATH_REGISTRATION_URL`` -- default: ``/register``
- ``STORMPATH_LOGIN_URL`` -- default: ``/login``
- ``STORMPATH_LOGOUT_URL`` -- default: ``/logout``

If you were to modify your config such that::

    app.config['STORMPATH_REGISTRATION_URL'] = '/welcome'

Then visit ``/welcome``, you'd see your registration page there, instead!


Customize the Templates
-----------------------

Although I personally find our registration and login pages to be incredibly
good looking -- I realize that you might not share my same design passion!

Flask-Stormpath was built with customizability in mind, and makes it very easy
to build your own custom registration and login templates.

Let's start by looking at the built-in templates:
https://github.com/stormpath/stormpath-flask/tree/develop/flask_stormpath/templates/flask_stormpath

Here's a quick rundown of what each template is for:

- ``base.html`` is the base template that the registration and login templates
  extend.  It provides a basic `bootstrap`_ based layout, with a couple of
  blocks for customizing the child templates.
- ``facebook_login_form.html`` is a simple standalone template that includes a
  Facebook login button (*for social login, which is covered later on in the
  guide*).
- ``google_login_form.html`` is a simple standalone template that includes a
  Google login button (*for social login, which is covered later on in the
  guide*).
- ``login.html`` is the login page.  It has some logic to flash error messages
  to the user if something fails, and also dynamically determines which input
  boxes to display based on the app's settings.
- ``register.html`` is the registration page.  It has some logic to flash error
  messages to the user if something fails, and also dynamically determines
  which input boxes to display based on the app's settings.

If you're comfortable with `Jinja2`_, you can copy these templates to your
project directly, and customize them yourself.  If you're not already a super
Flask guru, continue reading!


The Most Basic Templates
........................

Let's say you want to build your own, fully customized registration and login
templates -- no problem!

The first thing you need to do is create two templates in the ``templates``
directory of your project.

First, copy the following code into ``templates/register.html``::

    <form method="post">
      {{ form.hidden_tag() }}

      {# This bit of code displays a list of error messages if anything bad happens. #}
      {% with messages = get_flashed_messages() %}
        {% if messages %}
          <ul>
            {% for message in messages %}
              <li>{{ message }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}

      {# This block of code renders the desired input boxes for registering users.  #}
      {% if config['STORMPATH_ENABLE_USERNAME'] %}
        {% if config['STORMPATH_REQUIRE_USERNAME'] %}
          {{ form.username(placeholder='Username', required='true') }}
        {% else %}
          {{ form.username(placeholder='Username') }}
        {% endif %}
      {% endif %}
      {% if config['STORMPATH_ENABLE_GIVEN_NAME'] %}
        {% if config['STORMPATH_REQUIRE_GIVEN_NAME'] %}
          {{ form.given_name(placeholder='First Name', required='true') }}
        {% else %}
          {{ form.given_name(placeholder='First Name') }}
        {% endif %}
      {% endif %}
      {% if config['STORMPATH_ENABLE_MIDDLE_NAME'] %}
        {% if config['STORMPATH_REQUIRE_MIDDLE_NAME'] %}
          {{ form.middle_name(placeholder='Middle Name', required='true') }}
        {% else %}
          {{ form.middle_name(placeholder='Middle Name') }}
        {% endif %}
      {% endif %}
      {% if config['STORMPATH_ENABLE_SURNAME'] %}
        {% if config['STORMPATH_REQUIRE_SURNAME'] %}
          {{ form.surname(placeholder='Last Name', required='true') }}
        {% else %}
          {{ form.surname(placeholder='Last Name') }}
        {% endif %}
      {% endif %}
      {{ form.email(placeholder='Email', required='true', type='email') }}
      {{ form.password(placeholder='Password', required='true', type='password') }}

      <button type="submit">Create Account</button>
    </form>

The simple template you see above is the most basic possible registration page.
It's using `Flask-WTF`_ to render the form fields, but everything other than
that is all standard -- nothing special happening.

Next, copy the following code into ``templates/login.html``::

    {# Display errors (if there are any). #}
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    {# Render the login form. #}
    <form method="post">
      {{ form.hidden_tag() }}
      {% if config['STORMPATH_ENABLE_USERNAME'] %}
        {{ form.login(placeholder='Username or Email', required='true') }}
      {% else %}
        {{ form.login(placeholder='Email', required='true') }}
      {% endif %}
      {{ form.password(placeholder='Password', required='true') }}
      <button type="submit">Log In</button>
    </form>

    {# If social login is enabled, display social login buttons. #}
    {% if config['STORMPATH_ENABLE_FACEBOOK'] or config['STORMPATH_ENABLE_GOOGLE'] %}
      <p>Or, log in using a social provider.</p>
      {% if config['STORMPATH_ENABLE_FACEBOOK'] %}
        {% include "flask_stormpath/facebook_login_form.html" %}
      {% endif %}
      {% if config['STORMPATH_ENABLE_GOOGLE'] %}
        {% include "flask_stormpath/google_login_form.html" %}
      {% endif %}
    {% endif %}

This is the most basic login template possible (it also includes support for
social login, which is covered later in this guide).


Update Template Paths
.....................

Now that you've got the simplest possible templates ready to go, let's activate
them!  In your app's config, you'll need to specify the path to your new
templates like so::

    app.config['STORMPATH_REGISTRATION_TEMPLATE'] = 'register.html'
    app.config['STORMPATH_LOGIN_TEMPLATE'] = 'login.html'

That will tell Flask-Stormpath to render the templates you created above instead
of the built-in ones!

Now, if you open your browser and checkout ``/register`` and ``/login``, you
should see something like the following:

.. image:: /_static/registration-page-basic.png

.. image:: /_static/login-page-basic.png

**BAM!**  That wasn't so bad, was it?  You now have your own customized
registration and login templates -- all you need to do now is design them the
way you want!


Disable the Built-in Views
--------------------------

If for some reason you want to write your own registration, login, and logout
views (not recommended), you can easily disable all of the automatic
functionality described above by modifying your app config and adding the
following::

    app.config['STORMPATH_ENABLE_REGISTRATION'] = False
    app.config['STORMPATH_ENABLE_LOGIN'] = False
    app.config['STORMPATH_ENABLE_LOGOUT'] = False


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


.. _Stormpath dashboard: https://api.stormpath.com/ui/dashboard
.. _Account: http://docs.stormpath.com/rest/product-guide/#accounts
.. _bootstrap: http://getbootstrap.com/
.. _Jinja2: http://jinja.pocoo.org/docs/
.. _Flask-WTF: https://flask-wtf.readthedocs.org/en/latest/
