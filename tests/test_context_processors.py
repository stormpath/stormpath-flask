"""Run tests against our custom context processors."""


from os import environ
from unittest import TestCase

from flask import Flask
from flask.ext.stormpath import StormpathManager, User, user
from flask.ext.stormpath.context_processors import user_context_processor

from .helpers import bootstrap_app, bootstrap_client


class TestUserContextProcessor(TestCase):

    def setUp(self):
        # Initialize a new Stormpath Client for future usage.
        self.client = bootstrap_client()

        # Create a new Stormpath application, for future usage.
        self.application = bootstrap_app(self.client)

        # Create a Flask app for testing.
        self.app = Flask(__name__)
        self.app.config['DEBUG'] = True
        self.app.config['SECRET_KEY'] = 'woot'
        self.app.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
        self.app.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')
        self.app.config['STORMPATH_APPLICATION'] = self.application.name
        self.app.config['WTF_CSRF_ENABLED'] = False
        StormpathManager(self.app)

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
