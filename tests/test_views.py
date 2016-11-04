"""Run tests against our custom views."""


from flask.ext.stormpath.models import User

from .helpers import StormpathTestCase


class TestRegister(StormpathTestCase):
    """Test our registration view."""

    def test_default_fields(self):
        # By default, we'll register new users with first name, last name,
        # email, and password.
        with self.app.test_client() as c:

            # Ensure that missing fields will cause a failure.
            resp = c.post('/register', data={
                'email': 'r@testmail.stormpath.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 200)

            # Ensure that valid fields will result in a success.
            resp = c.post('/register', data={
                'username': 'rdegges',
                'given_name': 'Randall',
                'middle_name': 'Clark',
                'surname': 'Degges',
                'email': 'r@testmail.stormpath.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

    def test_disable_all_except_mandatory(self):
        # Here we'll disable all the fields except for the mandatory fields:
        # email and password.
        self.app.config['STORMPATH_ENABLE_USERNAME'] = False
        self.app.config['STORMPATH_ENABLE_GIVEN_NAME'] = False
        self.app.config['STORMPATH_ENABLE_MIDDLE_NAME'] = False
        self.app.config['STORMPATH_ENABLE_SURNAME'] = False

        with self.app.test_client() as c:

            # Ensure that missing fields will cause a failure.
            resp = c.post('/register', data={
                'email': 'r@testmail.stormpath.com',
            })
            self.assertEqual(resp.status_code, 200)

            # Ensure that valid fields will result in a success.
            resp = c.post('/register', data={
                'email': 'r@testmail.stormpath.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

    def test_require_settings(self):
        # Here we'll change our backend behavior such that users *can* enter a
        # first and last name, but they aren't required server side.
        # email and password.
        self.app.config['STORMPATH_REQUIRE_GIVEN_NAME'] = False
        self.app.config['STORMPATH_REQUIRE_SURNAME'] = False

        with self.app.test_client() as c:

            # Ensure that registration works *without* given name and surname
            # since they aren't required.
            resp = c.post('/register', data={
                'email': 'r@testmail.stormpath.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

            # Find our user account that was just created, and ensure the given
            # name and surname fields were set to our default string.
            user = User.from_login('r@testmail.stormpath.com', 'woot1LoveCookies!')
            self.assertEqual(user.given_name, 'Anonymous')
            self.assertEqual(user.surname, 'Anonymous')

    def test_error_messages(self):
        with self.app.test_client() as c:

            # Ensure that an error is raised if an invalid password is
            # specified.
            resp = c.post('/register', data={
                'given_name': 'Randall',
                'surname': 'Degges',
                'email': 'r@testmail.stormpath.com',
                'password': 'hilol',
            })
            self.assertEqual(resp.status_code, 200)

            self.assertTrue('Account password minimum length not satisfied.' in resp.data.decode('utf-8'))
            self.assertFalse('developerMessage' in resp.data.decode('utf-8'))

            resp = c.post('/register', data={
                'given_name': 'Randall',
                'surname': 'Degges',
                'email': 'r@testmail.stormpath.com',
                'password': 'hilolwoot1',
            })
            self.assertEqual(resp.status_code, 200)

            self.assertTrue('Password requires at least 1 uppercase character.' in resp.data.decode('utf-8'))
            self.assertFalse('developerMessage' in resp.data.decode('utf-8'))

            resp = c.post('/register', data={
                'given_name': 'Randall',
                'surname': 'Degges',
                'email': 'r@testmail.stormpath.com',
                'password': 'hilolwoothi',
            })
            self.assertEqual(resp.status_code, 200)

            self.assertTrue('Password requires at least 1 numeric character.' in resp.data.decode('utf-8'))
            self.assertFalse('developerMessage' in resp.data.decode('utf-8'))

    def test_redirect_to_login_and_register_url(self):
        # Setting redirect URL to something that is easy to check
        stormpath_redirect_url = '/redirect_for_login_and_registration'
        self.app.config['STORMPATH_REDIRECT_URL'] = stormpath_redirect_url

        with self.app.test_client() as c:
            # Ensure that valid registration will redirect to
            # STORMPATH_REDIRECT_URL
            resp = c.post(
                '/register',
                data=
                {
                    'given_name': 'Randall',
                    'middle_name': 'Clark',
                    'surname': 'Degges',
                    'email': 'r@testmail.stormpath.com',
                    'password': 'woot1LoveCookies!',
                })

            self.assertEqual(resp.status_code, 302)
            location = resp.headers.get('location')
            self.assertTrue(stormpath_redirect_url in location)

    def test_redirect_to_register_url(self):
        # Setting redirect URLs to something that is easy to check
        stormpath_redirect_url = '/redirect_for_login'
        stormpath_registration_redirect_url = '/redirect_for_registration'
        self.app.config['STORMPATH_REDIRECT_URL'] = stormpath_redirect_url
        self.app.config['STORMPATH_REGISTRATION_REDIRECT_URL'] = \
            stormpath_registration_redirect_url

        with self.app.test_client() as c:
            # Ensure that valid registration will redirect to
            # STORMPATH_REGISTRATION_REDIRECT_URL if it exists
            resp = c.post(
                '/register',
                data=
                {
                    'given_name': 'Randall',
                    'middle_name': 'Clark',
                    'surname': 'Degges',
                    'email': 'r@testmail.stormpath.com',
                    'password': 'woot1LoveCookies!',
                })

            self.assertEqual(resp.status_code, 302)
            location = resp.headers.get('location')
            self.assertFalse(stormpath_redirect_url in location)
            self.assertTrue(stormpath_registration_redirect_url in location)


class TestLogin(StormpathTestCase):
    """Test our login view."""

    def test_email_login(self):
        # Create a user.
        with self.app.app_context():
            User.create(
                given_name = 'Randall',
                surname = 'Degges',
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
            )

        # Attempt a login using email and password.
        with self.app.test_client() as c:
            resp = c.post('/login', data={
                'login': 'r@testmail.stormpath.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

    def test_username_login(self):
        # Create a user.
        with self.app.app_context():
            User.create(
                username = 'rdegges',
                given_name = 'Randall',
                surname = 'Degges',
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
            )

        # Attempt a login using username and password.
        with self.app.test_client() as c:
            resp = c.post('/login', data={
                'login': 'rdegges',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

    def test_error_messages(self):
        # Create a user.
        with self.app.app_context():
            User.create(
                username = 'rdegges',
                given_name = 'Randall',
                surname = 'Degges',
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
            )

        # Ensure that an error is raised if an invalid username or password is
        # specified.
        with self.app.test_client() as c:
            resp = c.post('/login', data={
                'login': 'rdegges',
                'password': 'hilol',
            })
            self.assertEqual(resp.status_code, 200)

            #self.assertTrue('Invalid username or password.' in resp.data.decode('utf-8'))
            self.assertTrue('Login attempt failed because the specified password is incorrect.' in resp.data.decode('utf-8'))
            self.assertFalse('developerMessage' in resp.data.decode('utf-8'))

    def test_redirect_to_login_and_register_url(self):
        # Create a user.
        with self.app.app_context():
            User.create(
                username = 'rdegges',
                given_name = 'Randall',
                surname = 'Degges',
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
            )

        # Setting redirect URL to something that is easy to check
        stormpath_redirect_url = '/redirect_for_login_and_registration'
        self.app.config['STORMPATH_REDIRECT_URL'] = stormpath_redirect_url

        with self.app.test_client() as c:
            # Attempt a login using username and password.
            resp = c.post(
                '/login',
                data={'login': 'rdegges', 'password': 'woot1LoveCookies!',})

            self.assertEqual(resp.status_code, 302)
            location = resp.headers.get('location')
            self.assertTrue(stormpath_redirect_url in location)

    def test_redirect_to_register_url(self):
        # Create a user.
        with self.app.app_context():
            User.create(
                username = 'rdegges',
                given_name = 'Randall',
                surname = 'Degges',
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
            )

        # Setting redirect URLs to something that is easy to check
        stormpath_redirect_url = '/redirect_for_login'
        stormpath_registration_redirect_url = '/redirect_for_registration'
        self.app.config['STORMPATH_REDIRECT_URL'] = stormpath_redirect_url
        self.app.config['STORMPATH_REGISTRATION_REDIRECT_URL'] = \
            stormpath_registration_redirect_url

        with self.app.test_client() as c:
            # Attempt a login using username and password.
            resp = c.post(
                '/login',
                data={'login': 'rdegges', 'password': 'woot1LoveCookies!',})

            self.assertEqual(resp.status_code, 302)
            location = resp.headers.get('location')
            self.assertTrue('redirect_for_login' in location)
            self.assertFalse('redirect_for_registration' in location)


class TestLogout(StormpathTestCase):
    """Test our logout view."""

    def test_logout_works_with_anonymous_users(self):
        with self.app.test_client() as c:
            resp = c.get('/logout')
            self.assertEqual(resp.status_code, 302)

    def test_logout_works(self):
        # Create a user.
        with self.app.app_context():
            User.create(
                given_name = 'Randall',
                surname = 'Degges',
                email = 'r@testmail.stormpath.com',
                password = 'woot1LoveCookies!',
            )

        with self.app.test_client() as c:
            # Log this user in.
            resp = c.post('/login', data={
                'login': 'r@testmail.stormpath.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

            # Log this user out.
            resp = c.get('/logout')
            self.assertEqual(resp.status_code, 302)
