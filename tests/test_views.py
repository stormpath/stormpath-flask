"""Run tests against our custom views."""


from flask.ext.stormpath.models import User

from .helpers import StormpathTestCase


class TestRegister(StormpathTestCase):

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
