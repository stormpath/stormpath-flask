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
        self.client = Client(
            id = environ.get('STORMPATH_API_KEY_ID'),
            secret = environ.get('STORMPATH_API_KEY_SECRET'),
        )
        self.application_name = 'flask-stormpath-tests-%s' % uuid4().hex

        # Try to delete our test application / directory first, this way if we
        # mess something up while developing test code (like I have many times
        # now), we won't get issues and have to manually remove these resources.
        try:
            self.client.applications.search(self.application_name)[0].delete()
            self.client.directories.search(self.application_name)[0].delete()
        except:
            pass

        self.application = self.client.applications.create({
            'name': self.application_name,
            'description': 'This application is ONLY used for testing the Flask-Stormpath library. Please do not use this for anything serious.',
        }, create_directory=True)
        self.user = self.application.accounts.create({
            'given_name': 'Randall',
            'middle_name': 'Clark',
            'surname': 'Degges',
            'email': 'randall@stormpath.com',
            'username': 'randall',
            'password': 'woot1LoveCookies!',
        })
        self.user.__class__ = User

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'woot'
        self.app.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
        self.app.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')
        self.app.config['STORMPATH_APPLICATION'] = self.application_name
        StormpathManager(self.app)

    def test_repr(self):
        self.assertTrue('randall' in self.user.__repr__())

    def test_subclass(self):
        account = Account(client=self.client, properties={
            'given_name': 'Randall',
            'surname': 'Degges',
            'email': 'randall@stormpath.com',
            'password': 'woot1LoveCookies!',
        })
        self.assertEqual(type(account), Account)

        user = account
        user.__class__ = User
        self.assertTrue(user.writable_attrs)

    def test_get_id(self):
        self.assertEqual(self.user.get_id(), self.user.href)

    def test_is_active(self):
        self.assertEqual(self.user.is_active(), self.user.status == 'ENABLED')

    def test_is_anonymous(self):
        self.assertEqual(self.user.is_anonymous(), False)

    def test_is_authenticated(self):
        self.assertEqual(self.user.is_authenticated(), True)

    def test_create(self):
        with self.app.app_context():

            # Ensure all defaults fields are properly set.
            user = User.create(
                email = 'woot@lol.com',
                password = 'Ilovec00kies!!',
                given_name = 'Cookie',
                surname = 'Monster',
            )
            self.assertEqual(user.email, 'woot@lol.com')
            self.assertEqual(user.given_name, 'Cookie')
            self.assertEqual(user.surname, 'Monster')
            self.assertEqual(user.username, 'woot@lol.com')
            self.assertEqual(user.middle_name, None)
            self.assertEqual(dict(user.custom_data), {})

            # Ensure we can the middle name and username fields to custom
            # entities.
            user = User.create(
                username = 'powerful',
                email = 'woot@lolcakes.com',
                password = 'Ilovec00kies!!',
                given_name = 'Austin',
                surname = 'Powers',
                middle_name = 'Danger',
            )
            self.assertEqual(user.username, 'powerful')
            self.assertEqual(user.middle_name, 'Danger')

            # Ensure we can set custom data when we create a user.
            user = User.create(
                email = 'snoop.dogg@snoopyrecords.com',
                password = 'Rast4F4rian!4LIFE',
                given_name = 'Snoop',
                surname = 'Dogg',
                custom_data = {
                    'favorite_state': 'California',
                    'favorite_genre': 'reggae',
                    'bank_details': {
                        'name': 'Bank of America',
                        'amount': 9999999.99,
                        'branch': {
                            'name': 'Bank of Venice',
                            'address': '111 9th Street',
                            'city': 'Venice',
                            'state': 'CA',
                        },
                    },
                },
            )
            self.assertEqual(dict(user.custom_data), {
                'favorite_state': 'California',
                'favorite_genre': 'reggae',
                'bank_details': {
                    'name': 'Bank of America',
                    'amount': 9999999.99,
                    'branch': {
                        'name': 'Bank of Venice',
                        'address': '111 9th Street',
                        'city': 'Venice',
                        'state': 'CA',
                    },
                },
            })

    def test_from_login(self):
        with self.app.app_context():
            user = User.from_login(
                'randall@stormpath.com',
                'woot1LoveCookies!',
            )
            self.assertEqual(user.href, self.user.href)

            user = User.from_login(
                'randall',
                'woot1LoveCookies!',
            )
            self.assertEqual(user.href, self.user.href)

    def tearDown(self):
        self.application.delete()
        self.client.directories.search(self.application_name)[0].delete()
