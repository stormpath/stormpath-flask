"""Run tests against our custom context processors."""


from flask_stormpath import User, user
from flask_stormpath.context_processors import user_context_processor
from stormpath.error import Error

from .helpers import StormpathTestCase


class TestUserContextProcessor(StormpathTestCase):

    def setUp(self):
        """Provision a single user account for testing."""
        # Call the parent setUp method first -- this will bootstrap our tests.
        super(TestUserContextProcessor, self).setUp()

        # Create our Stormpath user.
        with self.app.app_context():
            self.user = User.create(
                given_name = 'Randall',
                surname = 'Degges',
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
            )

    def tearDown(self):
        super(TestUserContextProcessor, self).tearDown()
        try:
            self.user.delete()
        except Error:
            # Resource not found - ignore.
            pass

    def test_raw_works(self):
        with self.app.test_client() as c:
            c.post('/login', data={
                'login': self.user.email,
                'password': 'woot1LoveCookies!',
            })

            self.assertIsInstance(user_context_processor(), dict)
            self.assertTrue(user_context_processor().get('user'))
            self.assertIsInstance(user_context_processor()['user'], User)

    def test_works(self):
        with self.app.test_client() as c:
            c.post('/login', data={
                'login': self.user.email,
                'password': 'woot1LoveCookies!',
            })

            self.assertEqual(user.href, self.user.href)
