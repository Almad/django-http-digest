"""
Support for HTTP digest client.
"""

from md5 import md5
from django.test.client import Client

__all__ = ["HttpDigestClient"]

class HttpDigestClient(Client):
    """ Extend Django's client for HTTP digest support """
