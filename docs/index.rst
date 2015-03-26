Flask-Stormpath
===============

Flask-Stormpath is an extension for `Flask`_ that makes it *incredibly* simple
to add users and user data to your application.  It aims to completely abstract
away all user registration, login, authentication, and authorization problems,
and make building secure websites painless.  And the best part?  **You don't
even need a database!**

.. note::
    Unfortunately, this library will NOT work on Google App Engine due to the
    `requests <http://stackoverflow.com/questions/9604799/can-python-requests-library-be-used-on-google-app-engine>`_
    module not working :(


User's Guide
------------

This part of the documentation will show you how to get started with
Flask-Stormpath.  If you're a new Flask-Stormpath user, start here!

.. toctree::
   :maxdepth: 2

   about
   setup
   quickstart
   product
   help


API Reference
-------------

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api


Additional Notes
----------------

This part of the documentation covers changes between versions and upgrade
information, to help you migrate to newer versions of Flask-Stormpath easily.

Flask-Stormpath is made available under the `Apache License, Version 2.0`_.  In
short, you can do pretty much whatever you want!

.. toctree::
   :maxdepth: 2

   changelog
   upgrading


.. _Flask: http://flask.pocoo.org/
.. _Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0.html
