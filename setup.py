#!/usr/bin/env python2

from setuptools import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import os
import sys

project_dir = 'djangohttpdigest'

setup(
    name = "djangohttpdigest",
    version = '0.2.3',
    url = 'http://devel.almad.net/trac/django-http-digest/',
    author = 'Lukas Linhart',
    author_email = 'bugs@almad.net',
    description = 'Support for HTTP digest in Django web framework',
    packages = ['djangohttpdigest'],
    scripts = [],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
