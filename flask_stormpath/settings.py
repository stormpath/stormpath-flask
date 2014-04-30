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
    config.setdefault('STORMPATH_REQUIRE_SURNAME', False)

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
    config.setdefault('STORMPATH_REGISTRATION_TEMPLATE', 'register.html')
    config.setdefault('STORMPATH_LOGIN_TEMPLATE', 'login.html')
    config.setdefault('STORMPATH_LOGOUT_TEMPLATE', 'logout.html')
    config.setdefault('STORMPATH_FORGOT_PASSWORD_TEMPLATE', 'forgot.html')
    config.setdefault('STORMPATH_SETTINGS_TEMPLATE', 'settings.html')

    # Social login configuration.
    config.setdefault('STORMPATH_SOCIAL', {})
