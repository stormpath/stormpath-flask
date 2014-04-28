from functools import wraps

from flask import current_app
from flask.ext.login import current_user


def groups_required(groups=None, all=True):
    """
    This decorator requires that a user be part of one or more Groups before
    they are granted access.

    :param list groups: A list of Groups to restrict access to.  A group can
        be:

        - A Group object.
        - A Group name (as a string).
        - A Group href (as a string).

    :param bool all: Should we ensure the user is a member of every group
        listed?  Default: True.  If this is set to False, we'll let the user
        into the view if the user is part of at least one of the specified
        groups.

    Usage::

        @groups_required(['admins', 'developers'], all=True)
        def private_view():
            return 'hi!'
    """
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_app.login_manager._login_disabled:
                return func(*args, **kwargs)
            elif not current_user.is_authenticated():
                return current_app.login_manager.unauthorized()

            if all and not current_user.has_groups(groups):
                return current_app.login_manager.unauthorized()
            elif not current_user.has_groups(groups, all=False):
                return current_app.login_manager.unauthorized()

            return func(*args, **kwargs)

        return wrapper

    return decorator
