"""
Our Flask-Stormpath tests.

Why are these in a single file instead of a directory?  Honestly, it's because
this extension is so simple, it didn't warrant a proper directory / module.  So
we'll just follow Flask conventions and have single file stuff going on.
"""


from unittest import TestCase

from flask.ext.stormpath import User

from stormpath.client import Client
from stormpath.resources.account import Account


class TestUser(TestCase):
    """Our User test suite."""

    def setUp(self):
        self.client = Client(id='woot', secret='woot')

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
