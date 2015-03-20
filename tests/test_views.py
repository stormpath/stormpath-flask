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
                'email': 'r@rdegges.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 200)

            # Ensure that valid fields will result in a success.
            resp = c.post('/register', data={
                'given_name': 'Randall',
                'middle_name': 'Clark',
                'surname': 'Degges',
                'email': 'r@rdegges.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

    def test_disable_all_except_mandatory(self):
        # Here we'll disable all the fields except for the mandatory fields:
        # email and password.
        self.app.config['STORMPATH_ENABLE_GIVEN_NAME'] = False
        self.app.config['STORMPATH_ENABLE_MIDDLE_NAME'] = False
        self.app.config['STORMPATH_ENABLE_SURNAME'] = False

        with self.app.test_client() as c:

            # Ensure that missing fields will cause a failure.
            resp = c.post('/register', data={
                'email': 'r@rdegges.com',
            })
            self.assertEqual(resp.status_code, 200)

            # Ensure that valid fields will result in a success.
            resp = c.post('/register', data={
                'email': 'r@rdegges.com',
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
                'email': 'r@rdegges.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

            # Find our user account that was just created, and ensure the given
            # name and surname fields were set to our default string.
            user = User.from_login('r@rdegges.com', 'woot1LoveCookies!')
            self.assertEqual(user.given_name, 'Anonymous')
            self.assertEqual(user.surname, 'Anonymous')

    def test_error_messages(self):
        with self.app.test_client() as c:

            # Ensure that an error is raised if an invalid password is
            # specified.
            resp = c.post('/register', data={
                'given_name': 'Randall',
                'surname': 'Degges',
                'email': 'r@rdegges.com',
                'password': 'hilol',
            })
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('Account password minimum length not satisfied.' in resp.data)
            self.assertFalse("developerMessage" in resp.data.decode('utf-8'))

            resp = c.post('/register', data={
                'given_name': 'Randall',
                'surname': 'Degges',
                'email': 'r@rdegges.com',
                'password': 'hilolwoot1',
            })
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('Password requires at least 1 uppercase character.' in resp.data)
            self.assertFalse("developerMessage" in resp.data.decode('utf-8'))

            resp = c.post('/register', data={
                'given_name': 'Randall',
                'surname': 'Degges',
                'email': 'r@rdegges.com',
                'password': 'hilolwoothi',
            })
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('Password requires at least 1 numeric character.' in resp.data)
            self.assertFalse("developerMessage" in resp.data.decode('utf-8'))


class TestLogin(StormpathTestCase):
    """Test our login view."""

    def test_email_login(self):
        # Create a user.
        with self.app.app_context():
            User.create(
                given_name = 'Randall',
                surname = 'Degges',
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
            )

        # Attempt a login using email and password.
        with self.app.test_client() as c:
            resp = c.post('/login', data={
                'login': 'r@rdegges.com',
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
                email = 'r@rdegges.com',
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
                email = 'r@rdegges.com',
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
            self.assertTrue('Invalid username or password.' in resp.data)
            self.assertFalse("developerMessage" in resp.data.decode('utf-8'))


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
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
            )

        with self.app.test_client() as c:
            # Log this user in.
            resp = c.post('/login', data={
                'login': 'r@rdegges.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

            # Log this user out.
            resp = c.get('/logout')
            self.assertEqual(resp.status_code, 302)
