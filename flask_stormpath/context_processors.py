"""Custom context processors to make template development simpler."""


from flask import current_app
from flask.ext.login import _get_user


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


def inject_base_template():
    """
    Insert a special variable named `stormpath_base_template` into all
    templates.

    This makes it possible for developers to create their own base template,
    from which all other templates extend.  This is not possible normally, as
    the Jinja2 `extends` tag doesn't allow for dictionary lookups :(

    With this, you can now write templates that start off like this::

        {% extends stormpath_base_template %}

    And then you can control what template is the base template by setting the
    `STORMPATH_BASE_TEMPLATE` setting via your Flask config::

        app.config['STORMPATH_BASE_TEMPLATE'] = 'my_custom_base_template.html'

    This makes writing your own authentication pages much simpler.
    """
    return {'stormpath_base_template': current_app.config['STORMPATH_BASE_TEMPLATE']}
