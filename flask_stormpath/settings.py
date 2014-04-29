"""Helper functions for dealing with Flask-Stormpath settings."""


def setup(config):
    """
    Initialize the Flask-Stormpath settings.

    This function sets all default configuration values.
    """
    # Basic Stormpath credentials and configuration.
    config.setdefault('STORMPATH_API_KEY_ID', None)
    config.setdefault('STORMPATH_API_KEY_SECRET', None)
    config.setdefault('STORMPATH_API_KEY_FILE', None)
    config.setdefault('STORMPATH_APPLICATION', None)

    # Which fields should be used to register new users?
    config.setdefault('STORMPATH_FACEBOOK', False)
    config.setdefault('STORMPATH_GOOGLE', False)
    config.setdefault('STORMPATH_EMAIL', True)  # If this is diabled, only
                                                # social login can be used.
    config.setdefault('STORMPATH_USERNAME', False)
    config.setdefault('STORMPATH_GIVEN_NAME', True)
    config.setdefault('STORMPATH_MIDDLE_NAME', True)
    config.setdefault('STORMPATH_SURNAME', True)

    # If this is set to True, users will be required to specify their password
    # twice when creating a new account.  If this is set to False (default),
    # users will only be prompted to enter their password once.
    config.setdefault('STORMPATH_PASSWORD_TWICE', False)

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
    config.setdefault('STORMPATH_ENABLE_FORGOT_PASSWORD', True)
    config.setdefault('STORMPATH_ENABLE_SETTINGS', True)

    # Configure URL mappings.  These URL mappings control which URLs will be
    # used by Flask-Stormpath views.
    config.setdefault('STORMPATH_REGISTRATION_URL', '/register')
    config.setdefault('STORMPATH_LOGIN_URL', '/login')
    config.setdefault('STORMPATH_LOGOUT_URL', '/logout')
    config.setdefault('STORMPATH_FORGOT_PASSWORD_URL', '/forgot')
    config.setdefault('STORMPATH_SETTINGS_URL', '/settings')

    # After a successful login, where should users be redirected?
    config.setdefault('STORMPATH_REDIRECT_URL', '/')

    # Configure templates.  These template settings control which templates are
    # used to render the Flask-Stormpath views.
    config.setdefault('STORMPATH_ENABLE_REGISTRATION', 'register.html')
    config.setdefault('STORMPATH_ENABLE_LOGIN', 'login.html')
    config.setdefault('STORMPATH_ENABLE_LOGOUT', 'logout.html')
    config.setdefault('STORMPATH_ENABLE_FORGOT_PASSWORD', 'forgot.html')
    config.setdefault('STORMPATH_ENABLE_SETTINGS', 'settings.html')

    # Social login configuration.
    config.setdefault('STORMPATH_SOCIAL', {})
