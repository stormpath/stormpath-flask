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
    Blueprint,
    _app_ctx_stack as stack,
    current_app,
)

from flask.ext.login import (
    LoginManager,
    current_user,
    _get_user,
    login_required,
    login_user,
    logout_user,
)

from stormpath.client import Client
from stormpath.error import Error as StormpathError

from werkzeug.local import LocalProxy

from .context_processors import _user_context_processor
from .decorators import groups_required
from .models import User
from .settings import setup
from .views import register


# A proxy for the current user.
user = LocalProxy(lambda: _get_user())


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

        This method will handle:

            - Configuring application settings.
            - Configuring Flask-Stormpath.
            - Adding ourself to the user's app (so the user can reference this
              extension later on, if they want).
        """
        # Initialize all of the Flask-Stormpath configuration variables and
        # settings.
        setup(app.config)

        app.login_manager = LoginManager(app)
        app.login_manager.session_protection = 'strong'
        app.login_manager.user_callback = self.load_user
        app.stormpath_manager = self

        blueprint = Blueprint('flask_stormpath', 'flask_stormpath', template_folder='templates')
        app.register_blueprint(blueprint)

        if app.config['STORMPATH_ENABLE_REGISTRATION']:
            app.add_url_rule(
                app.config['STORMPATH_REGISTRATION_URL'],
                'stormpath.register',
                register,
                methods = ['GET', 'POST'],
            )

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
                if self.app.config['STORMPATH_API_KEY_FILE']:
                    ctx.stormpath_client = Client(
                        api_key_file_location = self.app.config['STORMPATH_API_KEY_FILE'],
                    )

                # If the user isn't specifying their credentials via a file
                # path, it means they're using environment variables, so we'll
                # try to grab those values.
                else:
                    ctx.stormpath_client = Client(
                        id = self.app.config['STORMPATH_API_KEY_ID'],
                        secret = self.app.config['STORMPATH_API_KEY_SECRET'],
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
                    self.app.config['STORMPATH_APPLICATION']
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
