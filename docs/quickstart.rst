.. _quickstart:
.. module:: flask.ext.stormpath


Quickstart
==========

Now that we've got all the prerequisites out of the way, let's take a look at
some code!  Integrating Flask-Stormpath into an application can take as little
as **1 minute**!


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
    app.config['STORMPATH_API_KEY_FILE'] = '/path/to/apiKey.properties'
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
    application created in the Setup docs.  "dronewars", for instance.

    The ``SECRET_KEY`` variable should be a random string -- this is used by
    Flask internally for securing sessions -- make sure this isn't easily
    guessable!

.. note::
    **Please don't hardcode your API key information into your source code!**
    To keep your credentials safe and secret, we recommend storing these
    credentials in environment variables or keeping your ``apiKey.properties``
    file out of version control.


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


.. _Stormpath dashboard: https://api.stormpath.com/ui/dashboard
