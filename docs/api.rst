.. _api:


API
===

.. module:: flask_stormpath

This part of the documentation documents all the public classes, functions, and
API details in Flask-Stormpath.  This documentation is auto generated, and is
always a good up-to-date reference.


Configuration
-------------

.. autoclass:: StormpathManager

    .. automethod:: client
    .. automethod:: application
    .. automethod:: login_view
    .. automethod:: load_user


Models
------

.. autoclass:: User

    .. automethod:: get_id
    .. automethod:: is_active
    .. automethod:: is_anonymous
    .. automethod:: is_authenticated
    .. automethod:: from_login


Decorators
----------

.. autofunction:: groups_required
.. autofunction:: login_required


Request Context
---------------

.. autofunction:: user
