#!/usr/bin/env python

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import os
import sys

project_dir = 'djangohttpdigest'

# Dynamically calculate the version based on django.VERSION.
version = __import__('djangohttpdigest').__versionstr__
setup(
    name = "djangohttpdigest",
    version = version,
    url = 'http://devel.almad.net/trac/django-http-digest/',
    author = 'Lukas Linhart',
    author_email = 'bugs@almad.net',
    description = 'Support for HTTP digest in Django web framework',
    packages = ['djangohttpdigest'],
    scripts = [],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.5",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
