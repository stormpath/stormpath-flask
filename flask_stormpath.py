# -*- coding: utf-8 -*-
"""

    flask-stormpath
    ---------------

    This module provides secure user authentication and authorization for Flask
    via Stormpath (https://stormpath.com/).  It lets you log users in and out
    of your application in a database-independent fashion, along with allowing
    you to store variable user information in a JSON data store.

    No user table required! :)

    :copyright: (c) 2012 - 2014 Stormpath, Inc.
    :license: Apache, see LICENSE for more details.
"""


__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__author__ = 'Stormpath, Inc.'
__license__ = 'Apache'
__copyright__ = '(c) 2012 - 2014 Stormpath, Inc.'


from flask import (
    _app_ctx_stack as stack,
    current_app,
)

from flask.ext.login import (
    LoginManager,
    _get_user,
    login_required,
    login_user,
    logout_user,
)

from stormpath.client import Client
from stormpath.error import Error as StormpathError
from stormpath.resources.account import Account

from werkzeug.local import LocalProxy


# A proxy for the current user.
user = LocalProxy(lambda: _get_user())


class User(Account):
    """
    The base User object.

    This can be used as described in the Stormpath Python SDK documentation:
    https://github.com/stormpath/stormpath-sdk-python
    """
    def __repr__(self):
        return u'User <"%s" ("%s")>' % (self.username or self.email, self.href)

    def get_id(self):
        """
        Return the unique user identifier (in our case, the Stormpath resource
        href).
        """
        return unicode(self.href)

    def is_active(self):
        """
        A user account is active if, and only if, their account status is
        'ENABLED'.
        """
        return self.status == 'ENABLED'

    def is_anonymous(self):
        """
        We don't support anonymous users, so this is always False.
        """
        return False

    def is_authenticated(self):
        """
        All users will always be authenticated, so this will always return
        True.
        """
        return True

    @classmethod
    def create(self, email, password, given_name, surname, username=None, middle_name=None, custom_data=None):
        """
        Create a new User.

        Required Params
        ---------------

        :param str email: This user's unique email address.
        :param str password: This user's password, in plain text.
        :param str given_name: This user's first name (Randall).
        :param str surname: This user's last name (Degges).

        Optional Params
        ---------------

        :param str username: If no username is supplied, it will default to the
            user's email address.  Stormpath users can log in with either an
            email or username (both are interchangable).

        :param str middle_name: This user's middle name (Clark).

        :param dict custom_data: Any custom JSON data you'd like stored with
            this user.  Must be 10MB or less.

        If something goes wrong we'll raise an exception -- most likely -- a
        StormpathError (flask.ext.stormpath.StormpathError).
        """
        _user = current_app.stormpath_manager.application.accounts.create({
            'email': email,
            'password': password,
            'given_name': given_name,
            'surname': surname,
            'username': username,
            'middle_name': middle_name,
            'custom_data': custom_data,
        })
        _user.__class__ = User

        return _user

    @classmethod
    def from_login(self, login, password):
        """
        Create a new User class given a login (email address or username), and
        password.

        If something goes wrong, this will raise an exception -- most likely --
        a StormpathError (flask.ext.stormpath.StormpathError).
        """
        _user = current_app.stormpath_manager.application.authenticate_account(
            login,
            password,
        ).account
        _user.__class__ = User

        return _user


def _user_context_processor():
    """
    Insert a special variable named `user` into all templates.

    This makes it easy for developers to add users and their data into
    templates without explicitly passing the user each each time.

    With this, you can now write templates that do stuff like this::

        {% if user %}
            <p>Hi, {{ user.given_name }}!</p>
            <p>Your email is: {{ user.email }}</p>
        {% endif %}

    This lets you do powerful stuff, since the User object is nothing more than
    a Stormpath Account behind the scenes.  See the Python SDK documentation
    for more information about Account objects:
    https://github.com/stormpath/stormpath-sdk-python
    """
    return {'user': _get_user()}


class StormpathManager(object):
    """
    This object is used to hold the settings used to communicate with
    Stormpath.  Instances of :class:`StormpathManager` are not bound to
    specific apps, so you can create one in the main body of your code and
    then bind it to your app in a factory function.
    """
    def __init__(self, app=None):
        self.app = app

        # If the user specifies an app, let's configure Flask-Login with our
        # desired settings.
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize this application.

        We'll use this opportunity to configure Flask-Login.
        """
        app.login_manager = LoginManager(app)
        app.login_manager.session_protection = 'strong'
        app.login_manager.user_callback = self.load_user
        app.stormpath_manager = self

        # Ensure the 'user' context is available in templates.
        app.context_processor(_user_context_processor)

        self.app = app

    @property
    def client(self):
        """
        Lazily load the Stormpath Client object we need to access the raw
        Stormpath SDK.
        """
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'stormpath_client'):

                # If the user is specifying their credentials via a file path,
                # we'll use this.
                if self.app.config.get('STORMPATH_API_KEYFILE'):
                    ctx.stormpath_client = Client(
                        api_key_file_location = self.app.config.get('STORMPATH_API_KEYFILE'),
                    )

                # If the user isn't specifying their credentials via a file
                # path, it means they're using environment variables, so we'll
                # try to grab those values.
                else:
                    ctx.stormpath_client = Client(
                        id = self.app.config.get('STORMPATH_API_KEY_ID'),
                        secret = self.app.config.get('STORMPATH_API_KEY_SECRET'),
                    )

            return ctx.stormpath_client

    @property
    def login_view(self):
        """
        Return the user's Flask-Login login view, behind the scenes.
        """
        return current_app.login_manager.login_view

    @login_view.setter
    def login_view(self, value):
        """
        Proxy any changes to the user's login view to Flask-Login, behind the
        scenes.
        """
        self.app.login_manager.login_view = value

    @property
    def application(self):
        """
        Lazily load the Stormpath Application object we need to handle user
        authentication, etc.
        """
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'stormpath_application'):
                #ctx.stormpath_application = ctx.stormpath_client.applications.search(
                ctx.stormpath_application = self.client.applications.search(
                    self.app.config.get('STORMPATH_APPLICATION')
                )[0]

            return ctx.stormpath_application

    @staticmethod
    def load_user(account_href):
        """
        Given an Account href (a valid Stormpath Account URL), return the
        associated User account object (or None).

        :returns: The User object or None.
        """
        user = current_app.stormpath_manager.client.accounts.get(account_href)

        try:
            user._ensure_data()
            user.__class__ = User

            return user
        except StormpathError:
            return None
