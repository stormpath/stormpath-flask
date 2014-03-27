"""
Flask-Stormpath
---------------

The simplest and most secure way to handle user authentication and
authorization with Flask, via Stormpath (https://stormpath.com).

Flask-Stormpath on GitHub: https://github.com/stormpath/stormpath-flask
Documentation on RTFD: http://flask-stormpath.readthedocs.org/en/latest/
"""


from subprocess import call

from setuptools import (
    Command,
    setup,
)


class RunTests(Command):
    """Run our unit / integration tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run our tests!"""
        errno = call(['py.test'])
        raise SystemExit(errno)


setup(
    name = 'Flask-Stormpath',
    version = '0.0.1',
    url = 'https://github.com/stormpath/stormpath-flask',
    license = 'Apache',
    author = 'Stormpath, Inc.',
    author_email = 'python@stormpath.com',
    description = 'Simple and secure user authentication for Flask via Stormpath.',
    long_description = __doc__,
    py_modules = ['flask_stormpath'],
    cmdclass = {'test': RunTests},
    zip_safe = False,
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'Flask',
        'Flask-Login==0.2.9',
        'stormpath==1.1.0',
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
