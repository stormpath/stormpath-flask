.. _changelog:


Change Log
==========

All library changes, in descending order.


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
