"""
Test helpers.

These utilities are meant to simplify our tests, and abstract away common test
operations.
"""


from os import environ
from uuid import uuid4

from flask import Flask
from flask.ext.stormpath import StormpathManager
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

    :param obj client: A Stormpath Client resource.
    :rtype: obj
    :returns: A new Stormpath Application, fully initialized.
    """
    return client.applications.create({
        'name': 'flask-stormpath-tests-%s' % uuid4().hex,
        'description': 'This application is ONLY used for testing the Flask-Stormpath library. Please do not use this for anything serious.',
    }, create_directory=True)


def bootstrap_flask_app(app):
    """
    Create a new, fully initialized Flask app.

    :param obj app: A Stormpath Application resource.
    :rtype: obj
    :returns: A new Flask app.
    """
    a = Flask(__name__)
    a.config['DEBUG'] = True
    a.config['SECRET_KEY'] = uuid4().hex
    a.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
    a.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')
    a.config['STORMPATH_APPLICATION'] = app.name
    a.config['WTF_CSRF_ENABLED'] = False
    StormpathManager(a)

    return a
