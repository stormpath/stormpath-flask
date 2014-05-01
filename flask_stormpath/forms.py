"""Helper forms which make handling common operations simpler."""


from flask.ext.wtf import Form
from wtforms.fields import (
    PasswordField,
    StringField,
)
from wtforms.validators import (
    InputRequired,
    ValidationError,
)


class RegistrationForm(Form):
    """
    Register a new user.

    This class is used to provide safe user registration.  The only required
    fields are `email` and `password` -- everything else is optional (and can
    be configured by the developer to be used or not).

    .. note::
        This form only includes the fields that are available to register
        users with Stormpath directly -- this doesn't include support for
        Stormpath's social login stuff.

        Since social login stuff is handled separately (registration happens
        through Javascript) we don't need to have a form for registering users
        that way.
    """
    username = StringField('Username')
    given_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    surname = StringField('Last Name')
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class LoginForm(Form):
    """
    Log in an existing user.

    This class is used to provide safe user login.  A user can log in using
    either `username` and `password` or `email` and `password`.

    .. note::
        This form only includes the fields that are available to log users in
        with Stormpath directoy -- this doesn't include support for Stormpath's
        social login stuff.

        Since social login stuff is handled separately (login happens through
        Javascript) we don't need to have a form for logging in users that way.
    """
    username = StringField('Username')
    email = StringField('Email')
    password = PasswordField('Password', validators=[InputRequired()])

    def validate_email(self, form, field):
        if (not field.data) and (not form.username.data):
            raise ValidationError('Either username or email must be specified.')

    def validate_username(self, form, field):
        if (not field.data) and (not form.email.data):
            raise ValidationError('Either username or email must be specified.')
