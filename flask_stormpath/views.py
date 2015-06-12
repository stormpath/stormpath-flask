"""Our pluggable views."""


from facebook import get_user_from_cookie
from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
)
from flask.ext.login import login_user
from six import string_types
from stormpath.resources.provider import Provider

from . import StormpathError, logout_user
from .forms import (
    ChangePasswordForm,
    ForgotPasswordForm,
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

                    # Manually override the terms for first / last name to make
                    # errors more user friendly.
                    if field == 'given_name':
                        field = 'first name'

                    elif field == 'surname':
                        field = 'last name'

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
                data['surname'] = data['surname'] or 'Anonymous'

                # Create the user account on Stormpath.  If this fails, an
                # exception will be raised.
                account = User.create(**data)

                # If we're able to successfully create the user's account,
                # we'll log the user in (creating a secure session using
                # Flask-Login), then redirect the user to the
                # STORMPATH_REDIRECT_URL setting.
                login_user(account, remember=True)

                if 'STORMPATH_REGISTRATION_REDIRECT_URL'\
                        in current_app.config:
                    redirect_url = current_app.config[
                        'STORMPATH_REGISTRATION_REDIRECT_URL']
                else:
                    redirect_url = current_app.config['STORMPATH_REDIRECT_URL']
                return redirect(redirect_url)

            except StormpathError as err:
                flash(err.message.get('message'))

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

        except StormpathError as err:
            flash(err.message.get('message'))

    return render_template(
        current_app.config['STORMPATH_LOGIN_TEMPLATE'],
        form = form,
    )


def forgot():
    """
    Initialize 'password reset' functionality for a user who has forgotten his
    password.

    This view will render a forgot template, which prompts a user for their
    email address, then sends a password reset email.

    The URL this view is bound to, and the template that is used to render
    this page can all be controlled via Flask-Stormpath settings.
    """
    form = ForgotPasswordForm()

    # If we received a POST request with valid information, we'll continue
    # processing.
    if form.validate_on_submit():
        try:
            # Try to fetch the user's account from Stormpath.  If this
            # fails, an exception will be raised.
            account = current_app.stormpath_manager.application.send_password_reset_email(form.email.data)
            account.__class__ = User

            # If we're able to successfully send a password reset email to this
            # user, we'll display a success page prompting the user to check
            # their inbox to complete the password reset process.
            return render_template(
                current_app.config['STORMPATH_FORGOT_PASSWORD_EMAIL_SENT_TEMPLATE'],
                user = account,
            )
        except StormpathError as err:
            # If the error message contains 'https', it means something failed
            # on the network (network connectivity, most likely).
            if isinstance(err.message, string_types) and 'https' in err.message.lower():
                flash('Something went wrong! Please try again.')

            # Otherwise, it means the user is trying to reset an invalid email
            # address.
            else:
                flash('Invalid email address.')

    return render_template(
        current_app.config['STORMPATH_FORGOT_PASSWORD_TEMPLATE'],
        form = form,
    )


def forgot_change():
    """
    Allow a user to change his password.

    This can only happen if a use has reset their password, received the
    password reset email, then clicked the link in the email which redirects
    them to this view.

    The URL this view is bound to, and the template that is used to render
    this page can all be controlled via Flask-Stormpath settings.
    """
    try:
        account = current_app.stormpath_manager.application.verify_password_reset_token(request.args.get('sptoken'))
    except StormpathError as err:
        abort(400)

    form = ChangePasswordForm()

    # If we received a POST request with valid information, we'll continue
    # processing.
    if form.validate_on_submit():
        try:
            # Update this user's passsword.
            account.password = form.password.data
            account.save()

            # Log this user into their account.
            account = User.from_login(account.email, form.password.data)
            login_user(account, remember=True)

            return render_template(current_app.config['STORMPATH_FORGOT_PASSWORD_COMPLETE_TEMPLATE'])
        except StormpathError as err:
            if isinstance(err.message, string_types) and 'https' in err.message.lower():
                flash('Something went wrong! Please try again.')
            else:
                flash(err.message.get('message'))

    # If this is a POST request, and the form isn't valid, this means the
    # user's password was no good, so we'll display a message.
    elif request.method == 'POST':
        flash("Passwords don't match.")

    return render_template(
        current_app.config['STORMPATH_FORGOT_PASSWORD_CHANGE_TEMPLATE'],
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
    try:
        account = User.from_facebook(facebook_user['access_token'])
    except StormpathError as err:
        social_directory_exists = False

        # If we failed here, it usually means that this application doesn't have
        # a Facebook directory -- so we'll create one!
        for asm in current_app.stormpath_manager.application.account_store_mappings:

            # If there is a Facebook directory, we know this isn't the problem.
            if (
                getattr(asm.account_store, 'provider') and
                asm.account_store.provider.provider_id == Provider.FACEBOOK
            ):
                social_directory_exists = True
                break

        # If there is a Facebook directory already, we'll just pass on the
        # exception we got.
        if social_directory_exists:
            raise err

        # Otherwise, we'll try to create a Facebook directory on the user's
        # behalf (magic!).
        dir = current_app.stormpath_manager.client.directories.create({
            'name': current_app.stormpath_manager.application.name + '-facebook',
            'provider': {
                'client_id': current_app.config['STORMPATH_SOCIAL']['FACEBOOK']['app_id'],
                'client_secret': current_app.config['STORMPATH_SOCIAL']['FACEBOOK']['app_secret'],
                'provider_id': Provider.FACEBOOK,
            },
        })

        # Now that we have a Facebook directory, we'll map it to our application
        # so it is active.
        asm = current_app.stormpath_manager.application.account_store_mappings.create({
            'application': current_app.stormpath_manager.application,
            'account_store': dir,
            'list_index': 99,
            'is_default_account_store': False,
            'is_default_group_store': False,
        })

        # Lastly, let's retry the Facebook login one more time.
        account = User.from_facebook(facebook_user['access_token'])

    # Now we'll log the new user into their account.  From this point on, this
    # Facebook user will be treated exactly like a normal Stormpath user!
    login_user(account, remember=True)

    return redirect(request.args.get('next') or current_app.config['STORMPATH_REDIRECT_URL'])


def google_login():
    """
    Handle Google login.

    When a user logs in with Google (using Javascript), Google will redirect
    the user to this view, along with an access code for the user.

    What we do here is grab this access code and send it to Stormpath to handle
    the OAuth negotiation.  Once this is done, we log this user in using normal
    sessions, and from this point on -- this user is treated like a normal
    system user!

    The location this view redirects users to can be configured via
    Flask-Stormpath settings.
    """
    # First, we'll try to grab the 'code' query string that Google should be
    # passing to us.  If this doesn't exist, we'll abort with a 400 BAD REQUEST
    # (since something horrible must have happened).
    code = request.args.get('code')
    if not code:
        abort(400)

    # Next, we'll try to have Stormpath either create or update this user's
    # Stormpath account, by automatically handling the Google API stuff for us.
    try:
        account = User.from_google(code)
    except StormpathError as err:
        social_directory_exists = False

        # If we failed here, it usually means that this application doesn't
        # have a Google directory -- so we'll create one!
        for asm in current_app.stormpath_manager.application.account_store_mappings:

            # If there is a Google directory, we know this isn't the problem.
            if (
                getattr(asm.account_store, 'provider') and
                asm.account_store.provider.provider_id == Provider.GOOGLE
            ):
                social_directory_exists = True
                break

        # If there is a Google directory already, we'll just pass on the
        # exception we got.
        if social_directory_exists:
            raise err

        # Otherwise, we'll try to create a Google directory on the user's
        # behalf (magic!).
        dir = current_app.stormpath_manager.client.directories.create({
            'name': current_app.stormpath_manager.application.name + '-google',
            'provider': {
                'client_id': current_app.config['STORMPATH_SOCIAL']['GOOGLE']['client_id'],
                'client_secret': current_app.config['STORMPATH_SOCIAL']['GOOGLE']['client_secret'],
                'redirect_uri': request.url_root[:-1] + current_app.config['STORMPATH_GOOGLE_LOGIN_URL'],
                'provider_id': Provider.GOOGLE,
            },
        })

        # Now that we have a Google directory, we'll map it to our application
        # so it is active.
        asm = current_app.stormpath_manager.application.account_store_mappings.create({
            'application': current_app.stormpath_manager.application,
            'account_store': dir,
            'list_index': 99,
            'is_default_account_store': False,
            'is_default_group_store': False,
        })

        # Lastly, let's retry the Facebook login one more time.
        account = User.from_google(code)

    # Now we'll log the new user into their account.  From this point on, this
    # Google user will be treated exactly like a normal Stormpath user!
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
