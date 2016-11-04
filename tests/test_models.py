"""Tests for our data models."""


from flask_stormpath.models import User
from stormpath.resources.account import Account

from .helpers import StormpathTestCase


class TestUser(StormpathTestCase):
    """Our User test suite."""

    def test_subclass(self):
        with self.app.app_context():
            user = User.create(
                email = 'r@testmail.stormpath.com',
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
                email = 'r@testmail.stormpath.com',
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
                email = 'r@testmail.stormpath.com',
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
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.get_id(), user.href)

    def test_is_active(self):
        with self.app.app_context():

            # Ensure users are active by default.
            user = User.create(
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.is_active, True)

            # Ensure users who have their accounts explicitly disabled actually
            # return a proper status when `is_active` is called.
            user.status = User.STATUS_DISABLED
            self.assertEqual(user.is_active, False)

            # Ensure users who have not verified their accounts return a proper
            # status when `is_active` is called.
            user.status = User.STATUS_UNVERIFIED
            self.assertEqual(user.is_active, False)

    def test_is_anonymous(self):
        with self.app.app_context():

            # There is no way we can be anonymous, as Stormpath doesn't support
            # anonymous users (that is a job better suited for a cache or
            # something).
            user = User.create(
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.is_anonymous, False)

    def test_is_authenticated(self):
        with self.app.app_context():

            # This should always return true.  If a user account can be
            # fetched, that means it must be authenticated.
            user = User.create(
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.is_authenticated, True)

    def test_create(self):
        with self.app.app_context():

            # Ensure all requied fields are properly set.
            user = User.create(
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )
            self.assertEqual(user.email, 'r@testmail.stormpath.com')
            self.assertEqual(user.given_name, 'Randall')
            self.assertEqual(user.surname, 'Degges')
            self.assertEqual(user.username, 'r@testmail.stormpath.com')
            self.assertEqual(user.middle_name, None)
            self.assertEqual(
                dict(user.custom_data),
                {
                    'created_at': user.custom_data.created_at,
                    'modified_at': user.custom_data.modified_at,
                })

            # Delete this user.
            user.delete()

            # Ensure all optional parameters are properly set.
            user = User.create(
                email = 'r@testmail.stormpath.com',
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
                'created_at': user.custom_data.created_at,
                'modified_at': user.custom_data.modified_at,
            })

    def test_from_login(self):
        with self.app.app_context():

            # First we'll create a user.
            user = User.create(
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
                username = 'rdegges',
            )
            original_href = user.href

            # Now we'll try to retrieve that user by specifing the user's
            # `email` and `password`.
            user = User.from_login(
                'r@testmail.stormpath.com',
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
