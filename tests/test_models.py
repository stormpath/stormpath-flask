"""Tests for our data models."""


from os import environ
from unittest import TestCase
from uuid import uuid4

from flask import Flask
from flask.ext.stormpath import StormpathManager
from flask.ext.stormpath.models import User
from stormpath.client import Client
from stormpath.resources.account import Account


class TestUser(TestCase):
    """Our User test suite."""

    def setUp(self):
        """Generate some useful test data to make running our tests easier."""
        # Create a Stormpath Client so we can provision necessary resources.
        self.client = Client(
            id = environ.get('STORMPATH_API_KEY_ID'),
            secret = environ.get('STORMPATH_API_KEY_SECRET'),
        )

        # Reserve a globally unique Application name that all test data will be
        # created under.  This is made random to prevent test collisions where
        # a test suite is running concurrently, and destroying test data
        # unexpectedly.
        self.application_name = 'flask-stormpath-tests-%s' % uuid4().hex

        # Create an Application that will be used to run all tests.
        self.application = self.client.applications.create({
            'name': self.application_name,
            'description': 'This application is ONLY used for testing the Flask-Stormpath library. Please do not use this for anything serious.',
        }, create_directory=True)

        # Initialize a Flask application.
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'woot'
        self.app.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
        self.app.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')
        self.app.config['STORMPATH_APPLICATION'] = self.application_name

        # Initialize Flask-Stormpath.
        StormpathManager(self.app)

    def test_subclass(self):
        with self.app.app_context():
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )

            # Ensure that our lazy construction of the subclass works as
            # expected for users (a `User` should be a valid Stormpath
            # `Account`.
            self.assertTrue(user.writable_attrs)
            self.assertIsInstance(user, Account)
            self.assertIsInstance(user, User)

    def test_repr(self):
        with self.app.app_context():

            # Ensure `email` is shown in the output if no `username` is
            # specified.
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertTrue(user.email in user.__repr__())

            # Delete this user.
            user.delete()

            # Ensure `username` is shown in the output if specified.
            user = User.create(
                username = 'omgrandall',
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertTrue(user.username in user.__repr__())

            # Ensure Stormpath `href` is shown in the output.
            self.assertTrue(user.href in user.__repr__())

    def test_get_id(self):
        with self.app.app_context():
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.get_id(), user.href)

    def test_is_active(self):
        with self.app.app_context():

            # Ensure users are active by default.
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.is_active(), True)

            # Ensure users who have their accounts explicitly disabled actually
            # return a proper status when `is_active` is called.
            user.status = User.STATUS_DISABLED
            self.assertEqual(user.is_active(), False)

            # Ensure users who have not verified their accounts return a proper
            # status when `is_active` is called.
            user.status = User.STATUS_UNVERIFIED
            self.assertEqual(user.is_active(), False)

    def test_is_anonymous(self):
        with self.app.app_context():

            # There is no way we can be anonymous, as Stormpath doesn't support
            # anonymous users (that is a job better suited for a cache or
            # something).
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.is_anonymous(), False)

    def test_is_authenticated(self):
        with self.app.app_context():

            # This should always return true.  If a user account can be
            # fetched, that means it must be authenticated.
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.is_authenticated(), True)

    def test_create(self):
        with self.app.app_context():

            # Ensure all requied fields are properly set.
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.email, 'r@rdegges.com')
            self.assertEqual(user.given_name, 'Randall')
            self.assertEqual(user.surname, 'Degges')
            self.assertEqual(user.username, 'r@rdegges.com')
            self.assertEqual(user.middle_name, None)
            self.assertEqual(dict(user.custom_data), {})

            # Delete this user.
            user.delete()

            # Ensure all optional parameters are properly set.
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
                username = 'rdegges',
                middle_name = 'Clark',
                custom_data = {
                    'favorite_shows': ['Code Monkeys', 'The IT Crowd'],
                    'friends': ['Sami', 'Alven'],
                    'favorite_place': {
                        'city': 'Santa Cruz',
                        'state': 'California',
                        'reason': 'Beautiful landscape.',
                        'amount_of_likage': 99.9999,
                    },
                },
            )
            self.assertEqual(user.username, 'rdegges')
            self.assertEqual(user.middle_name, 'Clark')
            self.assertEqual(dict(user.custom_data), {
                'favorite_shows': ['Code Monkeys', 'The IT Crowd'],
                'friends': ['Sami', 'Alven'],
                'favorite_place': {
                    'city': 'Santa Cruz',
                    'state': 'California',
                    'reason': 'Beautiful landscape.',
                    'amount_of_likage': 99.9999,
                },
            })

    def test_from_login(self):
        with self.app.app_context():

            # First we'll create a user.
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
                username = 'rdegges',
            )
            original_href = user.href

            # Now we'll try to retrieve that user by specifing the user's
            # `email` and `password`.
            user = User.from_login(
                'r@rdegges.com',
                'woot1LoveCookies!',
            )
            self.assertEqual(user.href, original_href)

            # Now we'll try to retrieve that user by specifying the user's
            # `username` and `password`.
            user = User.from_login(
                'rdegges',
                'woot1LoveCookies!',
            )
            self.assertEqual(user.href, original_href)

    def tearDown(self):
        """Destroy all data created during tests."""
        self.application.delete()
        self.client.directories.search(self.application_name)[0].delete()
