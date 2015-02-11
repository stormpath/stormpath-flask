"""Helper functions for dealing with Flask-Stormpath settings."""


from datetime import timedelta

from .errors import ConfigurationError


def init_settings(config):
    """
    Initialize the Flask-Stormpath settings.

    This function sets all default configuration values.

    :param dict config: The Flask app config.
    """
    # Basic Stormpath credentials and configuration.
    config.setdefault('STORMPATH_API_KEY_ID', None)
    config.setdefault('STORMPATH_API_KEY_SECRET', None)
    config.setdefault('STORMPATH_API_KEY_FILE', None)
    config.setdefault('STORMPATH_APPLICATION', None)

    # Which fields should be displayed when registering new users?
    config.setdefault('STORMPATH_ENABLE_FACEBOOK', False)
    config.setdefault('STORMPATH_ENABLE_GOOGLE', False)
    config.setdefault('STORMPATH_ENABLE_EMAIL', True)  # If this is diabled,
                                                       # only social login can
                                                       # be used.
    config.setdefault('STORMPATH_ENABLE_USERNAME', False)
    config.setdefault('STORMPATH_ENABLE_EMAIL', True)     # This MUST be True!
    config.setdefault('STORMPATH_ENABLE_PASSWORD', True)  # This MUST be True!
    config.setdefault('STORMPATH_ENABLE_GIVEN_NAME', True)
    config.setdefault('STORMPATH_ENABLE_MIDDLE_NAME', True)
    config.setdefault('STORMPATH_ENABLE_SURNAME', True)

    # If the user attempts to create a non-social account, which fields should
    # we require?  (Email and password are always required, so those are not
    # mentioned below.)
    config.setdefault('STORMPATH_REQUIRE_USERNAME', True)
    config.setdefault('STORMPATH_REQUIRE_EMAIL', True)     # This MUST be True!
    config.setdefault('STORMPATH_REQUIRE_PASSWORD', True)  # This MUST be True!
    config.setdefault('STORMPATH_REQUIRE_GIVEN_NAME', True)
    config.setdefault('STORMPATH_REQUIRE_MIDDLE_NAME', False)
    config.setdefault('STORMPATH_REQUIRE_SURNAME', True)

    # Will new users be required to verify new accounts via email before
    # they're made active?
    config.setdefault('STORMPATH_VERIFY_EMAIL', False)

    # Configure views.  These views can be enabled or disabled.  If they're
    # enabled (default), then you automatically get URL routes, working views,
    # and working templates for common operations: registration, login, logout,
    # forgot password, and changing user settings.
    config.setdefault('STORMPATH_ENABLE_REGISTRATION', True)
    config.setdefault('STORMPATH_ENABLE_LOGIN', True)
    config.setdefault('STORMPATH_ENABLE_LOGOUT', True)
    config.setdefault('STORMPATH_ENABLE_FORGOT_PASSWORD', False)
    config.setdefault('STORMPATH_ENABLE_SETTINGS', True)

    # Configure URL mappings.  These URL mappings control which URLs will be
    # used by Flask-Stormpath views.
    config.setdefault('STORMPATH_REGISTRATION_URL', '/register')
    config.setdefault('STORMPATH_LOGIN_URL', '/login')
    config.setdefault('STORMPATH_LOGOUT_URL', '/logout')
    config.setdefault('STORMPATH_FORGOT_PASSWORD_URL', '/forgot')
    config.setdefault('STORMPATH_FORGOT_PASSWORD_CHANGE_URL', '/forgot/change')
    config.setdefault('STORMPATH_SETTINGS_URL', '/settings')
    config.setdefault('STORMPATH_GOOGLE_LOGIN_URL', '/google')
    config.setdefault('STORMPATH_FACEBOOK_LOGIN_URL', '/facebook')

    # After a successful login, where should users be redirected?
    config.setdefault('STORMPATH_REDIRECT_URL', '/')

    # Cache configuration.
    config.setdefault('STORMPATH_CACHE', None)

    # Configure templates.  These template settings control which templates are
    # used to render the Flask-Stormpath views.
    config.setdefault('STORMPATH_BASE_TEMPLATE', 'flask_stormpath/base.html')
    config.setdefault('STORMPATH_REGISTRATION_TEMPLATE', 'flask_stormpath/register.html')
    config.setdefault('STORMPATH_LOGIN_TEMPLATE', 'flask_stormpath/login.html')
    config.setdefault('STORMPATH_FORGOT_PASSWORD_TEMPLATE', 'flask_stormpath/forgot.html')
    config.setdefault('STORMPATH_FORGOT_PASSWORD_EMAIL_SENT_TEMPLATE', 'flask_stormpath/forgot_email_sent.html')
    config.setdefault('STORMPATH_FORGOT_PASSWORD_CHANGE_TEMPLATE', 'flask_stormpath/forgot_change.html')
    config.setdefault('STORMPATH_FORGOT_PASSWORD_COMPLETE_TEMPLATE', 'flask_stormpath/forgot_complete.html')
    config.setdefault('STORMPATH_SETTINGS_TEMPLATE', 'flask_stormpath/settings.html')

    # Social login configuration.
    config.setdefault('STORMPATH_SOCIAL', {})

    # Cookie configuration.
    config.setdefault('STORMPATH_COOKIE_DOMAIN', None)
    config.setdefault('STORMPATH_COOKIE_DURATION', timedelta(days=365))

    # Cookie name (this is not overridable by users, at least not explicitly).
    config.setdefault('REMEMBER_COOKIE_NAME', 'stormpath_token')


def check_settings(config):
    """
    Ensure the user-specified settings are valid.

    This will raise a ConfigurationError if anything mandatory is not
    specified.

    :param dict config: The Flask app config.
    """
    if not (
        all([
            config['STORMPATH_API_KEY_ID'],
            config['STORMPATH_API_KEY_SECRET'],
        ]) or config['STORMPATH_API_KEY_FILE']
    ):
        raise ConfigurationError('You must define your Stormpath credentials.')

    if not config['STORMPATH_APPLICATION']:
        raise ConfigurationError('You must define your Stormpath application.')

    if config['STORMPATH_ENABLE_GOOGLE']:
        google_config = config['STORMPATH_SOCIAL'].get('GOOGLE')

        if not google_config or not all([
            google_config.get('client_id'),
            google_config.get('client_secret'),
        ]):
            raise ConfigurationError('You must define your Google app settings.')

    if config['STORMPATH_ENABLE_FACEBOOK']:
        facebook_config = config['STORMPATH_SOCIAL'].get('FACEBOOK')

        if not facebook_config or not all([
            facebook_config,
            facebook_config.get('app_id'),
            facebook_config.get('app_secret'),
        ]):
            raise ConfigurationError('You must define your Facebook app settings.')

    if config['STORMPATH_COOKIE_DOMAIN'] and not isinstance(config['STORMPATH_COOKIE_DOMAIN'], str):
        raise ConfigurationError('STORMPATH_COOKIE_DOMAIN must be a string.')

    if config['STORMPATH_COOKIE_DURATION'] and not isinstance(config['STORMPATH_COOKIE_DURATION'], timedelta):
        raise ConfigurationError('STORMPATH_COOKIE_DURATION must be a timedelta object.')
