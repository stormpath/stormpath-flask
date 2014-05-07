"""Run tests against our custom context processors."""


from unittest import TestCase

from flask.ext.stormpath import User, user
from flask.ext.stormpath.context_processors import user_context_processor

from .helpers import bootstrap_app, bootstrap_client, bootstrap_flask_app


class TestUserContextProcessor(TestCase):

    def setUp(self):
        # Initialize a new Stormpath Client for future usage.
        self.client = bootstrap_client()

        # Create a new Stormpath application, for future usage.
        self.application = bootstrap_app(self.client)

        # Create a Flask app for testing.
        self.app = bootstrap_flask_app(self.application)

        # Create a new Stormpath user account.
        with self.app.app_context():
            self.user = User.create(
                given_name = 'Randall',
                surname = 'Degges',
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
            )

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

    def tearDown(self):
        pass
