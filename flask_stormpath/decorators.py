"""
Custom decorators to make handling authentication and authorization
simpler.
"""


from functools import wraps

from flask import current_app
from flask_login import current_user


def groups_required(groups, all=True):
    """
    This decorator requires that a user be part of one or more Groups before
    they are granted access.

    :param list groups: (required) A list of Groups to restrict access to.  A
        group can be:

        - A Group object.
        - A Group name (as a string).
        - A Group href (as a string).

    :param bool all: (optional) Should we ensure the user is a member of every
        group listed?  Default: True.  If this is set to False, we'll let the
        user into the view if the user is part of at least one of the specified
        groups.

    Usage::

        @groups_required(['admins', 'developers'])
        def private_view():
            '''Only admins and developers will be able to visit this page.'''
            return 'hi!'
    """
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # If authentication stuff is disabled, do nothing.
            if current_app.login_manager._login_disabled:
                return func(*args, **kwargs)

            # If the user is NOT authenticated, this user is unauthorized.
            elif not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            # If the user authenticated, and the all flag is set, we need to
            # see if the user is a member of *ALL* groups.
            if all and not current_user.has_groups(groups):
                return current_app.login_manager.unauthorized()

            # If the all flag is NOT set, we need to make sure the user is a
            # member of at least one group.
            elif not current_user.has_groups(groups, all=False):
                return current_app.login_manager.unauthorized()

            # Lastly, if the user has successfully passsed all authentication /
            # authorization challenges, we'll allow them in.
            return func(*args, **kwargs)

        return wrapper

    return decorator
