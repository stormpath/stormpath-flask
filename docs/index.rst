.. Flask-Stormpath documentation master file, created by
   sphinx-quickstart on Tue Feb 18 11:24:11 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Flask-Stormpath
===============

.. currentmodule:: flask.ext.stormpath


*User management made easy.*

Hi there, and thanks for checking out Flask-Stormpath!

Flask-Stormpath is a library which aims to make it incredibly easy to add user
management, authentication, and authorization into your Flask web applications
with very little work!

If you're not already familiar with `Stormpath <https://stormpath.com>` you
might want to visit their site and get acquainted with them.

Stormpath is an API company which securely handles user accounts (and custom
user data) in a fast, secure, and effective way.

This library plugs Stormpath into your Flask application, making it simple to
handle users and their data.


Why You Might Want to Use Stormpath
-----------------------------------

Stormpath is a great service, but it's not for everyone.

You might want to use Stormpath if:

- User security is a top priority.
- Scaling your userbase is a potential problem (Stormpath handles scaling your
  users completely).
- You need to store custom user data along with your user's basic information
  (email, password).
- You would like to have automatic email verification for new user accounts.
- You would like to configure and customize password strength rules.
- You'd like to keep your user data separate from your other application to
  increase platform stability / availability.
- You are a big organization who would like to use Stormpath, but need to host
  it yourself (Stormpath has an on-premise system you can use internally).

You might **NOT** want to use Stormpath if:

- You are building an application that does not need user accounts.
- Your application is meant for internal-only usage.
- You aren't worried about user data / security much.
- You aren't worried about application availability / redundancy.
- You want to roll your own custom user authentication.

If you don't need Stormpath, you might want to check out `Flask-Login
<http://flask-login.readthedocs.org/en/latest/>` (which Flask-Stormpath uses
behind the scenes to handle sessions).

Want to use Stormpath?  OK, great!  Let's get started!


Table of Contents

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
