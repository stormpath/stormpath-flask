.. _changelog:


Change Log
==========

All library changes, in descending order.


Version 0.4.5
-------------

**Not yet released.**

- Upgrading Stormpath dependency to latest release.
- Upgrading oauth2client dependency to latest release.
- Upgrading blinker dependency to latest release.
- Upgrading Flask-Login dependency to latest release.
- Adding Python 3 support.


Version 0.4.4
-------------

**Released on August 31, 2015.**

- Upgrading the Stormpath dependency to the latest release.


Version 0.4.3
-------------

**Released on August 25, 2015.**

- Adding in some test fixes.
- Adding in signals for user creation, updating, and deleting.
- Upgrading the Stormpath library to the latest release.


Version 0.4.2
-------------

**Released on June 12, 2015.**

- Adding notes about ``TESTING = True`` for clarity.
- Fixing error handling error in the 'forgot password' feature.  If a user tried
  to change their password to something that didn't match the password strength
  rules, they'd get a 500.


Version 0.4.1
-------------

**Released on May 19, 2015.**

- Adding 'profile' scope as a default requested scope for Google login.  This
  allows us to get a user's first and last name in addition to their email
  address.  Thanks to `@stauffec <https://github.com/stauffec>`_ for the
  contribution!


Version 0.4.0
-------------

**Released on April 15, 2015.**

- Adding new setting: ``STORMPATH_REGISTRATION_REDIRECT_URL``.  This lets users
  specify where they'd like to redirect a *newly registered user*.


Version 0.3.9
-------------

**Released on March 27, 2015.**

- Removing python 3 compatibility (*due to pip bug with Facebook SDK*).  This
  will be back soon once we find a workaround.


Version 0.3.8
-------------

**Released on March 26, 2015.**

- Making the library 100% python 3 compatible!
- Fixing issue with error messages being flashed incorrectly.


Version 0.3.7
-------------

**Released on March 2, 2015.**

- Fixing exception handling error during password reset when an invalid email
  address is entered.  Thanks `@roengraft <https://github.com/roengraft>`_ for
  the report!


Version 0.3.6
-------------

**Released on February 16, 2015.**

- Fixing minor issues in error handling in our registration and login views.
- Adding tests for error handling in our registration and login views.


Version 0.3.5
-------------

**Released on February 11, 2015.**

- Upgrading dependencies.


Version 0.3.4
-------------

**Released on February 11, 2015.**

- Upgrading our Stormpath python dependency.  Lots of bugfixes / improvements
  included.
- Allowing users to customize the base Stormpath template via a new setting:
  ``STORMPATH_BASE_TEMPLATE``.


Version 0.3.3
-------------

**Released on January 28, 2015.**

- Upgrading our Stormpath python dependency.  This gets us lots of bugfixes /
  speed improvements.


Version 0.3.2
-------------

**Released on January 27, 2015.**

- Fixing issue with singletons.  We were previously NOT using a client
  singleton, which means in-memory caching would not work :(


Version 0.3.1
-------------

**Released on December 23, 2014.**

- Fixing critical issue where version info caused startup errors.  The
  resolution is to remove dynamic versioning that depends on ``setup.py``.


Version 0.3.0
-------------

**Released on December 8, 2014.**

- Fixing minor issue with user agent.
- Updating stormpath dependency to latest release.
- Adding support for caching (*with local memory, memcached, and redis*).
- Adding caching docs.
- Dynamically handling library versions.


Version 0.2.9
-------------

**Released on November 7, 2014.**

- Adding support for Google login's `hd` attribute.


Version 0.2.8
-------------

**Released on September 20, 2014.**

- Fixing bug in forgot() view -- the user object passed to the template wasn't
  an actual user object.


Version 0.2.7
-------------

**Released on September 10, 2014.**

- Adding the ability to set a user's status when calling ``User.create()``.


Version 0.2.6
-------------

**Released on July 14, 2014.**

- Adding in easy 'Password Reset' functionality.  If a developer enables this
  functionality, users can easily reset their passwords securely.  This feature
  is disabled by default.


Version 0.2.5
-------------

**Released on June 24, 2014.**

- Fixing bug in built-in registration view.  When new users registered, the
  first name would be inserted into the last name field.


Version 0.2.4
-------------

**Released on June 16, 2014.**

- Fixing bug which affected the login page when `STORMPATH_ENABLE_REGISTRATION`
  was disabled.
- Fixing bug which affected the registration page when `STORMPATH_ENABLE_LOGIN`
  was disabled.


Version 0.2.3
-------------

**Released on May 22, 2014.**

- Adding a proper user agent.


Version 0.2.2
-------------

**Released on May 20, 2014.**

- Adding new setting: ``STORMPATH_COOKIE_DOMAIN``.  This allows users to specify
  which domain(s) the session cookie will be good for.
- Adding new setting: ``STORMPATH_COOKIE_DURATION``.  This allows users to
  specify how long a session will last (as a ``timedelta`` object).
- Adding docs on expiring sessions / cookies.


Version 0.2.1
-------------

**Released on May 16, 2014.**

- Fixing bug in package: templates weren't being included.


Version 0.2.0
-------------

**Released on May 14, 2014.**

- Adding customizable user settings.
- Adding support for social login via Gacebook.
- Adding support for social login via Facebook.
- Adding an automatic logout view.
- Adding an automatic login view.
- Adding an automatic registration view.
- Adding built-in routes for logout / login / register.
- Adding customizable registration / login pages.
- Adding built in templates for registration and login (with social included).
- Adding new documentation.


Version 0.1.0
-------------

**Released on March 26, 2014.**

- Adding a simple way to create new user accounts via ``User.create()``.
- Adding documentation for new ``User.create()`` method.
- Adding a groups_required decorator, which makes it easy to assert Group
  membership in views.
- Adding docs for new groups_required decorator.
- Using the lastest Python SDK as a dependency.


Version 0.0.1
-------------

**Released on February 19, 2014.**

- First release!
- Basic functionality.
- Basic docs.
- Lots to do!
