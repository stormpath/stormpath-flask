"""Tests for our settings stuff."""


from datetime import timedelta
from os import close, environ, remove, write
from tempfile import mkstemp

from flask_stormpath.errors import ConfigurationError
from flask_stormpath.settings import check_settings, init_settings

from .helpers import StormpathTestCase


class TestInitSettings(StormpathTestCase):
    """Ensure we can properly initialize Flask app settings."""

    def test_works(self):
        init_settings(self.app.config)

        # Ensure a couple of settings exist that we didn't explicitly specify
        # anywhere.
        self.assertEqual(self.app.config['STORMPATH_ENABLE_FACEBOOK'], False)
        self.assertEqual(self.app.config['STORMPATH_ENABLE_GIVEN_NAME'], True)


class TestCheckSettings(StormpathTestCase):
    """Ensure our settings checker is working properly."""

    def setUp(self):
        """Create an apiKey.properties file for testing."""
        super(TestCheckSettings, self).setUp()

        # Generate our file locally.
        self.fd, self.file = mkstemp()
        api_key_id = 'apiKey.id = %s\n' % environ.get('STORMPATH_API_KEY_ID')
        api_key_secret = 'apiKey.secret = %s\n' % environ.get(
            'STORMPATH_API_KEY_SECRET')
        write(self.fd, api_key_id.encode('utf-8') + b'\n')
        write(self.fd, api_key_secret.encode('utf-8') + b'\n')

    def test_requires_api_credentials(self):
        # We'll remove our default API credentials, and ensure we get an
        # exception raised.
        self.app.config['STORMPATH_API_KEY_ID'] = None
        self.app.config['STORMPATH_API_KEY_SECRET'] = None
        self.app.config['STORMPATH_API_KEY_FILE'] = None
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        # Now we'll check to see that if we specify an API key ID and secret
        # things work.
        self.app.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
        self.app.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')
        check_settings(self.app.config)

        # Now we'll check to see that if we specify an API key file things work.
        self.app.config['STORMPATH_API_KEY_ID'] = None
        self.app.config['STORMPATH_API_KEY_SECRET'] = None
        self.app.config['STORMPATH_API_KEY_FILE'] = self.file
        check_settings(self.app.config)

    def test_requires_application(self):
        # We'll remove our default Application, and ensure we get an exception
        # raised.
        self.app.config['STORMPATH_APPLICATION'] = None
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

    def test_google_settings(self):
        # Ensure that if the user has Google login enabled, they've specified
        # the correct settings.
        self.app.config['STORMPATH_ENABLE_GOOGLE'] = True
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        # Ensure that things don't work if not all social configs are specified.
        self.app.config['STORMPATH_SOCIAL'] = {}
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        self.app.config['STORMPATH_SOCIAL'] = {'GOOGLE': {}}
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        self.app.config['STORMPATH_SOCIAL']['GOOGLE']['client_id'] = 'xxx'
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        # Now that we've configured things properly, it should work.
        self.app.config['STORMPATH_SOCIAL']['GOOGLE']['client_secret'] = 'xxx'
        check_settings(self.app.config)

    def test_facebook_settings(self):
        # Ensure that if the user has Facebook login enabled, they've specified
        # the correct settings.
        self.app.config['STORMPATH_ENABLE_FACEBOOK'] = True
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        # Ensure that things don't work if not all social configs are specified.
        self.app.config['STORMPATH_SOCIAL'] = {}
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        self.app.config['STORMPATH_SOCIAL'] = {'FACEBOOK': {}}
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        self.app.config['STORMPATH_SOCIAL']['FACEBOOK']['app_id'] = 'xxx'
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        # Now that we've configured things properly, it should work.
        self.app.config['STORMPATH_SOCIAL']['FACEBOOK']['app_secret'] = 'xxx'
        check_settings(self.app.config)

    def test_cookie_settings(self):
        # Ensure that if a user specifies a cookie domain which isn't a string,
        # an error is raised.
        self.app.config['STORMPATH_COOKIE_DOMAIN'] = 1
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        # Now that we've configured things properly, it should work.
        self.app.config['STORMPATH_COOKIE_DOMAIN'] = 'test'
        check_settings(self.app.config)

        # Ensure that if a user specifies a cookie duration which isn't a
        # timedelta object, an error is raised.
        self.app.config['STORMPATH_COOKIE_DURATION'] = 1
        self.assertRaises(ConfigurationError, check_settings, self.app.config)

        # Now that we've configured things properly, it should work.
        self.app.config['STORMPATH_COOKIE_DURATION'] = timedelta(minutes=1)
        check_settings(self.app.config)

    def tearDown(self):
        """Remove our apiKey.properties file."""
        super(TestCheckSettings, self).tearDown()

        # Remove our file.
        close(self.fd)
        remove(self.file)
