"""
Test helpers.

These utilities are meant to simplify our tests, and abstract away common test
operations.
"""


from os import environ
from uuid import uuid4

from stormpath.client import Client


def bootstrap_client():
    """
    Create a new Stormpath Client from environment variables.

    :rtype: obj
    :returns: A new Stormpath Client, fully initialized.
    """
    return Client(
        id = environ.get('STORMPATH_API_KEY_ID'),
        secret = environ.get('STORMPATH_API_KEY_SECRET'),
    )


def bootstrap_app(client):
    """
    Create a new, uniquely named, Stormpath Application.

    This application can be used in tests that run concurrently, as each
    application has a unique namespace.

    .. note::
        This will *also* create a Stormpath directory of the same name, so that
        you can use this application to create users immediately.

    :rtype: obj
    :returns: A new Stormpath Application, fully initialized.
    """
    return client.applications.create({
        'name': 'flask-stormpath-tests-%s' % uuid4().hex,
        'description': 'This application is ONLY used for testing the Flask-Stormpath library. Please do not use this for anything serious.',
    }, create_directory=True)
