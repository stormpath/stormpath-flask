"""Run tests for signals."""

from flask.ext.login import user_logged_in
from flask_stormpath.models import (
    User,
    user_created,
    user_deleted,
    user_updated
)

from .helpers import StormpathTestCase, SignalReceiver


class TestSignals(StormpathTestCase):
    """Test signals."""

    def test_user_created_signal(self):
        # Subscribe to signals for user creation
        signal_receiver = SignalReceiver()
        user_created.connect(signal_receiver.signal_user_receiver_function)

        # Register new account
        with self.app.test_client() as c:
            resp = c.post('/register', data={
                'given_name': 'Randall',
                'middle_name': 'Clark',
                'surname': 'Degges',
                'email': 'r@rdegges.com',
                'password': 'woot1LoveCookies!',
            })
            self.assertEqual(resp.status_code, 302)

        # Check that signal for user creation is received
        self.assertEqual(len(signal_receiver.received_signals), 1)
        received_signal = signal_receiver.received_signals[0]
        # User instance is received
        self.assertIsInstance(received_signal[1], dict)
        # Correct user instance is received
        created_user = received_signal[1]
        self.assertEqual(created_user['email'], 'r@rdegges.com')
        self.assertEqual(created_user['surname'], 'Degges')

    def test_user_logged_in_signal(self):
        # Subscribe to signals for user login
        signal_receiver = SignalReceiver()
        user_logged_in.connect(signal_receiver.signal_user_receiver_function)

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

        # Check that signal for user login is received
        self.assertEqual(len(signal_receiver.received_signals), 1)
        received_signal = signal_receiver.received_signals[0]
        # User instance is received
        self.assertIsInstance(received_signal[1], User)
        # Correct user instance is received
        logged_in_user = received_signal[1]
        self.assertEqual(logged_in_user.email, 'r@rdegges.com')
        self.assertEqual(logged_in_user.surname, 'Degges')

    def test_user_is_updated_signal(self):
        # Subscribe to signals for user update
        signal_receiver = SignalReceiver()
        user_updated.connect(signal_receiver.signal_user_receiver_function)

        with self.app.app_context():

            # Ensure all requied fields are properly set.
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )

            user.middle_name = 'Clark'
            user.save()

        # Check that signal for user update is received
        self.assertEqual(len(signal_receiver.received_signals), 1)
        received_signal = signal_receiver.received_signals[0]
        # User instance is received
        self.assertIsInstance(received_signal[1], dict)
        # Correct user instance is received
        updated_user = received_signal[1]
        self.assertEqual(updated_user['email'], 'r@rdegges.com')
        self.assertEqual(updated_user['middle_name'], 'Clark')

    def test_user_is_deleted_signal(self):
        # Subscribe to signals for user delete
        signal_receiver = SignalReceiver()
        user_deleted.connect(signal_receiver.signal_user_receiver_function)

        with self.app.app_context():

            # Ensure all requied fields are properly set.
            user = User.create(
                email = 'r@rdegges.com',
                password = 'woot1LoveCookies!',
                given_name = 'Randall',
                surname = 'Degges',
            )

            user.delete()

        # Check that signal for user deletion is received
        self.assertEqual(len(signal_receiver.received_signals), 1)
        received_signal = signal_receiver.received_signals[0]
        # User instance is received
        self.assertIsInstance(received_signal[1], dict)
        # Correct user instance is received
        deleted_user = received_signal[1]
        self.assertEqual(deleted_user['email'], 'r@rdegges.com')
