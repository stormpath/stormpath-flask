Flask-Stormpath
===============

.. module:: flask.ext.stormpath


Flask-Stormpath is an extension for `Flask`_ that makes it *incredibly* simple
to add users and user data to your application.  It aims to completely abstract
away all user registration, login, authentication, and authorization problems,
and make building secure websites painless.  And the best part?  **You don't
even need a database!**


User's Guide
------------

This part of the documentation will show you how to get started with
Flask-Stormpath.  If you're a new Flask-Stormpath user, start here!

.. toctree::
   :maxdepth: 2

   about
   setup
   quickstart
   contexts
   config
   models
   queries
   binds
   signals


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








*User management and authentication made easy.*

Hi there, and thanks for checking out Flask-Stormpath!

Flask-Stormpath is a library which aims to make it incredibly easy to add user
management, authentication, and authorization into your Flask web applications
with very little work!

If you're not already familiar with `Stormpath <https://stormpath.com>`_ you
might want to visit their site and get acquainted with them.

Stormpath is an API company which securely handles user accounts (and custom
user data) in a fast, secure, and effective way.

This library plugs Stormpath into your Flask application, making it simple to
handle users and their data.


.. _Flask: http://flask.pocoo.org/
.. _Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0.html
