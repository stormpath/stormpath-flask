"""Custom context processors to make template development simpler."""


from flask import current_app
from flask_login import _get_user


def user_context_processor():
    """
    Insert a special variable named `user` into all templates.

    This makes it easy for developers to add users and their data into
    templates without explicitly passing the user each each time.

    With this, you can now write templates that do stuff like this::

        {% if user %}
            <p>Hi, {{ user.given_name }}!</p>
            <p>Your email is: {{ user.email }}</p>
        {% endif %}

    This lets you do powerful stuff, since the User object is nothing more than
    a Stormpath Account behind the scenes.  See the Python SDK documentation
    for more information about Account objects:
    https://github.com/stormpath/stormpath-sdk-python
    """
    return {'user': _get_user()}
