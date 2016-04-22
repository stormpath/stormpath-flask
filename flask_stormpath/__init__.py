# -*- coding: utf-8 -*-
"""
    flask-stormpath
    ---------------

    This module provides secure user authentication and authorization for Flask
    via Stormpath (https://stormpath.com/).  It lets you log users in and out
    of your application in a database-independent fashion, along with allowing
    you to store variable user information in a JSON data store.

    No user table required! :)

    :copyright: (c) 2012 - 2015 Stormpath, Inc.
    :license: Apache, see LICENSE for more details.
"""


__version__ = '0.4.5'
__version_info__ = __version__.split('.')
__author__ = 'Stormpath, Inc.'
__license__ = 'Apache'
__copyright__ = '(c) 2012 - 2015 Stormpath, Inc.'


from flask import (
    Blueprint,
    __version__ as flask_version,
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

from .context_processors import user_context_processor
from .decorators import groups_required
from .models import User
from .settings import check_settings, init_settings
from .views import (
    google_login,
    facebook_login,
    forgot,
    forgot_change,
    login,
    logout,
    register,
)


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
        """
        Initialize this extension.

        :param obj app: (optional) The Flask app.
        """
        self.app = app

        # If the user specifies an app, let's configure go ahead and handle all
        # configuration stuff for the user's app.
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

        :param obj app: The Flask app.
        """
        # Initialize all of the Flask-Stormpath configuration variables and
        # settings.
        init_settings(app.config)

        # Check our user defined settings to ensure Flask-Stormpath is properly
        # configured.
        check_settings(app.config)

        # Initialize the Flask-Login extension.
        self.init_login(app)

        # Initialize all URL routes / views.
        self.init_routes(app)

        # Initialize our blueprint.  This lets us do cool template stuff.
        blueprint = Blueprint('flask_stormpath', 'flask_stormpath', template_folder='templates')
        app.register_blueprint(blueprint)

        # Ensure the `user` context is available in templates.  This makes it
        # really easy for developers to grab user data for display purposes in
        # templates.
        app.context_processor(user_context_processor)

        # Store a reference to the Flask app so we can use it later if
        # necessary!
        self.app = app

    def init_login(self, app):
        """
        Initialize the Flask-Login extension.

        We use Flask-Login for managing sessions (primarily), so setting it up
        is necessary.

        :param obj app: The Flask app.
        """
        app.config['REMEMBER_COOKIE_DURATION'] = app.config['STORMPATH_COOKIE_DURATION']
        app.config['REMEMBER_COOKIE_DOMAIN'] = app.config['STORMPATH_COOKIE_DOMAIN']

        app.login_manager = LoginManager(app)
        app.login_manager.user_callback = self.load_user
        app.stormpath_manager = self

        if app.config['STORMPATH_ENABLE_LOGIN']:
            app.login_manager.login_view = 'stormpath.login'

        # Make this Flask session expire automatically.
        app.config['PERMANENT_SESSION_LIFETIME'] = app.config['STORMPATH_COOKIE_DURATION']

    def init_routes(self, app):
        """
        Initialize our built-in routes.

        If the user has enabled the built-in views / routes, they will be
        enabled here.

        This behavior is fully customizable in the user's settings.

        :param obj app: The Flask app.
        """
        if app.config['STORMPATH_ENABLE_REGISTRATION']:
            app.add_url_rule(
                app.config['STORMPATH_REGISTRATION_URL'],
                'stormpath.register',
                register,
                methods = ['GET', 'POST'],
            )

        if app.config['STORMPATH_ENABLE_LOGIN']:
            app.add_url_rule(
                app.config['STORMPATH_LOGIN_URL'],
                'stormpath.login',
                login,
                methods = ['GET', 'POST'],
            )

        if app.config['STORMPATH_ENABLE_FORGOT_PASSWORD']:
            app.add_url_rule(
                app.config['STORMPATH_FORGOT_PASSWORD_URL'],
                'stormpath.forgot',
                forgot,
                methods = ['GET', 'POST'],
            )
            app.add_url_rule(
                app.config['STORMPATH_FORGOT_PASSWORD_CHANGE_URL'],
                'stormpath.forgot_change',
                forgot_change,
                methods = ['GET', 'POST'],
            )

        if app.config['STORMPATH_ENABLE_LOGOUT']:
            app.add_url_rule(
                app.config['STORMPATH_LOGOUT_URL'],
                'stormpath.logout',
                logout,
            )

        if app.config['STORMPATH_ENABLE_GOOGLE']:
            app.add_url_rule(
                app.config['STORMPATH_GOOGLE_LOGIN_URL'],
                'stormpath.google_login',
                google_login,
            )

        if app.config['STORMPATH_ENABLE_FACEBOOK']:
            app.add_url_rule(
                app.config['STORMPATH_FACEBOOK_LOGIN_URL'],
                'stormpath.facebook_login',
                facebook_login,
            )

    @property
    def client(self):
        """
        Lazily load the Stormpath Client object we need to access the raw
        Stormpath SDK.
        """
        ctx = stack.top.app
        if ctx is not None:
            if not hasattr(ctx, 'stormpath_client'):

                # Create our custom user agent.  This allows us to see which
                # version of this SDK are out in the wild!
                user_agent = 'stormpath-flask/%s flask/%s' % (__version__, flask_version)

                # If the user is specifying their credentials via a file path,
                # we'll use this.
                if self.app.config['STORMPATH_API_KEY_FILE']:
                    ctx.stormpath_client = Client(
                        api_key_file_location = self.app.config['STORMPATH_API_KEY_FILE'],
                        user_agent = user_agent,
                        cache_options = self.app.config['STORMPATH_CACHE'],
                    )

                # If the user isn't specifying their credentials via a file
                # path, it means they're using environment variables, so we'll
                # try to grab those values.
                else:
                    ctx.stormpath_client = Client(
                        id = self.app.config['STORMPATH_API_KEY_ID'],
                        secret = self.app.config['STORMPATH_API_KEY_SECRET'],
                        user_agent = user_agent,
                        cache_options = self.app.config['STORMPATH_CACHE'],
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
        ctx = stack.top.app
        if ctx is not None:
            if not hasattr(ctx, 'stormpath_application'):
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
