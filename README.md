# stormpath-flask

Build simple, secure web applications with Stormpath and Flask!

[![Build Status](https://travis-ci.org/stormpath/stormpath-flask.png?branch=master)](https://travis-ci.org/stormpath/stormpath-flask)


**NOTE**: This library is an early release.  It's currently lacking many
features, and only handles basic use cases.  We're working on adding lots of
cool stuff to the library which will improve it's general usefulness.  If you
have feedback, please get in touch and share your thoughts!
[python@stormpath.com](mailto:python@stormpath.com)


## Documentation

You can find this project's documentation on ReadTheDocs:
http://flask-stormpath.readthedocs.org/en/latest/


## Sample Application

If you'd like to hop directly into some code, we've built a sample application,
which demonstrates how Flask-Stormpath can be used to build a very simple
user-facing website with user registration, login, dashboard, etc.

You can find the project on GitHub here:
https://github.com/stormpath/stormpath-flask-sample

This application provides a simple local web server that allows you to create
users, log them in, log them out, etc.

You can use this as a reference for implementing `Flask-Stormpath` into your
Flask projects.


## Backend

This library is largely based on the excellent
[Flask-Login](http://flask-login.readthedocs.org/en/latest/) library.  Most
functionality is piggybacked off this library, including secure user sessions /
etc.

Right now we're rapidly developing this library to make it easy for Flask
developers to add user authentication to their projects without the complication
that comes along with it.

If you have features or suggestions, please let me know!
[python@stormpath.com](mailto:python@stormpath.com)
