"""Our pluggable views."""


from facebook import get_user_from_cookie
from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
)
from flask.ext.login import login_user
from stormpath.resources.provider import Provider

from . import (
    StormpathError,
    logout_user,
)
from .forms import (
    LoginForm,
    RegistrationForm,
)
from .models import User


def register():
    """
    Register a new user with Stormpath.

    This view will render a registration template, and attempt to create a new
    user account with Stormpath.

    The fields that are asked for, the URL this view is bound to, and the
    template that is used to render this page can all be controlled via
    Flask-Stormpath settings.
    """
    form = RegistrationForm()

    # If we received a POST request with valid information, we'll continue
    # processing.
    if form.validate_on_submit():
        fail = False

        # Iterate through all fields, grabbing the necessary form data and
        # flashing error messages if required.
        data = form.data
        for field in data.keys():
            if current_app.config['STORMPATH_ENABLE_%s' % field.upper()]:
                if current_app.config['STORMPATH_REQUIRE_%s' % field.upper()] and not data[field]:
                    fail = True
                    flash('%s is required.' % field.replace('_', ' ').title())

        # If there are no missing fields (per our settings), continue.
        if not fail:

            # Attempt to create the user's account on Stormpath.
            try:

                # Since Stormpath requires both the given_name and surname
                # fields be set, we'll just set the both to 'Anonymous' if
                # the user has # explicitly said they don't want to collect
                # those fields.
                data['given_name'] = data['given_name'] or 'Anonymous'
                data['surname'] = data['given_name'] or 'Anonymous'

                # Create the user account on Stormpath.  If this fails, an
                # exception will be raised.
                account = User.create(**data)

                # If we're able to successfully create the user's account,
                # we'll log the user in (creating a secure session using
                # Flask-Login), then redirect the user to the
                # STORMPATH_REDIRECT_URL setting.
                login_user(account, remember=True)

                return redirect(current_app.config['STORMPATH_REDIRECT_URL'])
            except StormpathError, err:
                flash(err.user_message)

    return render_template(
        current_app.config['STORMPATH_REGISTRATION_TEMPLATE'],
        form = form,
    )


def login():
    """
    Log in an existing Stormpath user.

    This view will render a login template, then redirect the user to the next
    page (if authentication is successful).

    The fields that are asked for, the URL this view is bound to, and the
    template that is used to render this page can all be controlled via
    Flask-Stormpath settings.
    """
    form = LoginForm()

    # If we received a POST request with valid information, we'll continue
    # processing.
    if form.validate_on_submit():
        try:
            # Try to fetch the user's account from Stormpath.  If this
            # fails, an exception will be raised.
            account = User.from_login(form.login.data, form.password.data)

            # If we're able to successfully retrieve the user's account,
            # we'll log the user in (creating a secure session using
            # Flask-Login), then redirect the user to the ?next=<url>
            # query parameter, or the STORMPATH_REDIRECT_URL setting.
            login_user(account, remember=True)

            return redirect(request.args.get('next') or current_app.config['STORMPATH_REDIRECT_URL'])
        except StormpathError, err:
            flash(err.user_message)

    return render_template(
        current_app.config['STORMPATH_LOGIN_TEMPLATE'],
        form = form,
    )


def facebook_login():
    """
    Handle Facebook login.

    When a user logs in with Facebook, all of the authentication happens on the
    client side with Javascript.  Since all authentication happens with
    Javascript, we *need* to force a newly created and / or logged in Facebook
    user to redirect to this view.

    What this view does is:

        - Read the user's session using the Facebook SDK, extracting the user's
          Facebook access token.
        - Once we have the user's access token, we send it to Stormpath, so that
          we can either create (or update) the user on Stormpath's side.
        - Then we retrieve the Stormpath account object for the user, and log
          them in using our normal session support (powered by Flask-Login).

    Although this is slighly complicated, this gives us the power to then treat
    Facebook users like any other normal Stormpath user -- we can assert group
    permissions, authentication, etc.

    The location this view redirects users to can be configured via
    Flask-Stormpath settings.
    """
    # First, we'll try to grab the Facebook user's data by accessing their
    # session data.
    facebook_user = get_user_from_cookie(
        request.cookies,
        current_app.config['STORMPATH_SOCIAL']['FACEBOOK']['app_id'],
        current_app.config['STORMPATH_SOCIAL']['FACEBOOK']['app_secret'],
    )

    # Now, we'll try to have Stormpath either create or update this user's
    # Stormpath account, by automatically handling the Facebook Graph API stuff
    # for us.
    account = User.from_facebook(facebook_user['access_token'])

    # Now we'll log the new user into their account.  From this point on, this
    # Facebook user will be treated exactly like a normal Stormpath user!
    login_user(account, remember=True)

    return redirect(request.args.get('next') or current_app.config['STORMPATH_REDIRECT_URL'])


def logout():
    """
    Log a user out of their account.

    This view will log a user out of their account (destroying their session),
    then redirect the user to the home page of the site.
   """
    logout_user()
    return redirect('/')
