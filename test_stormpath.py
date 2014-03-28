"""
Our Flask-Stormpath tests.

Why are these in a single file instead of a directory?  Honestly, it's because
this extension is so simple, it didn't warrant a proper directory / module.  So
we'll just follow Flask conventions and have single file stuff going on.
"""


from os import (
    environ,
    remove,
)
from unittest import TestCase
from uuid import uuid4

from flask import (
    Flask,
    request,
)
from flask.ext.stormpath import (
    StormpathManager,
    User,
    _user_context_processor,
    groups_required,
    login_user,
    logout_user,
)

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


class TestStormpathManager(TestCase):
    """Our StormpathManager test suite."""

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
            'surname': 'Degges',
            'email': 'randall@stormpath.com',
            'username': 'randall',
            'password': 'woot1LoveCookies!',
        })
        self.user.__class__ = User

        keyfile = open('apiKey.properties', 'wb')
        keyfile.write('apiKey.id = %s\n' % environ.get('STORMPATH_API_KEY_ID'))
        keyfile.write('apiKey.secret = %s\n' % environ.get('STORMPATH_API_KEY_SECRET'))
        keyfile.close()

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'woot'
        self.app.config['STORMPATH_API_KEYFILE'] = 'apiKey.properties'
        self.app.config['STORMPATH_APPLICATION'] = self.application_name
        StormpathManager(self.app)

    def test_init(self):
        sm = StormpathManager()
        self.assertEqual(sm.app, None)

        sm = StormpathManager(self.app)
        self.assertEqual(sm.app, self.app)

    def test_init_app(self):
        StormpathManager(self.app)
        self.assertEqual(self.app.login_manager.session_protection, 'strong')

    def test_client(self):
        with self.app.app_context():
            self.assertIsInstance(self.app.stormpath_manager.client, Client)

    def test_login_view(self):
        def test_view():
            return 'hi'

        with self.app.app_context():
            self.app.stormpath_manager.login_view = test_view

    def tearDown(self):
        remove('apiKey.properties')
        self.application.delete()
        self.client.directories.search(self.application_name)[0].delete()


class TestGroupsRequired(TestCase):
    """Our groups_required decorator test suite."""

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
            'surname': 'Degges',
            'email': 'randall@stormpath.com',
            'username': 'randall',
            'password': 'woot1LoveCookies!',
        })
        self.user.__class__ = User

        self.admin_group = self.application.groups.create({
            'name': 'admins',
        })
        self.developers_group = self.application.groups.create({
            'name': 'developers',
        })

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'woot'
        self.app.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
        self.app.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')
        self.app.config['STORMPATH_APPLICATION'] = self.application_name

        StormpathManager(self.app)

    def test_unauthenticated(self):
        with self.app.test_client() as c:
            @self.app.route('/')
            @groups_required(['admins'])
            def test_view():
                return 'hi'

            self.assertEqual(c.get('/').status_code, 401)

    def test_unauthorized(self):
        with self.app.test_client() as c:

            @self.app.route('/login', methods=['POST'])
            def login():
                user = User.from_login(
                    request.form.get('email'),
                    request.form.get('password'),
                )
                login_user(user, remember=True)
                return 'logged in'

            @self.app.route('/')
            @groups_required(['admins', 'developers'])
            def test_view():
                return 'hi'

            resp = c.post('/login', data=dict(
                email = self.user.email,
                password = 'woot1LoveCookies!',
            ))
            self.assertEqual(resp.status_code, 200)

            self.assertEqual(c.get('/').status_code, 401)

            self.user.add_group('developers')
            self.assertEqual(c.get('/').status_code, 401)

    def test_authorized(self):
        with self.app.test_client() as c:

            @self.app.route('/login', methods=['POST'])
            def login():
                user = User.from_login(
                    request.form.get('email'),
                    request.form.get('password'),
                )
                login_user(user, remember=True)
                return 'logged in'

            @self.app.route('/logout')
            def logout():
                logout_user()

            @self.app.route('/')
            @groups_required([
                self.admin_group.href,
                self.developers_group
            ], all=False)
            def test_view():
                return 'hi'

            @self.app.route('/another_test')
            @groups_required(['admins', 'developers'], all=True)
            def another_test_view():
                return 'hi'

            resp = c.post('/login', data=dict(
                email = self.user.email,
                password = 'woot1LoveCookies!',
            ))
            self.assertEqual(resp.status_code, 200)

            self.assertEqual(c.get('/').status_code, 401)
            self.assertEqual(c.get('/another_test').status_code, 401)

            # Add the user to the admins group.
            self.user.add_group('admins')

            self.assertEqual(c.get('/').status_code, 200)
            self.assertEqual(c.get('/another_test').status_code, 401)

            # Add the user to the developers group.
            self.user.add_group('developers')
            self.assertEqual(c.get('/another_test').status_code, 200)

    def tearDown(self):
        self.application.delete()
        self.client.directories.search(self.application_name)[0].delete()
