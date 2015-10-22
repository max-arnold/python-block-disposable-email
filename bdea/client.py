# -*- coding: utf-8 -*-
"""Python client for block-disposable-email.com service.

http://www.block-disposable-email.com/cms/help-and-usage/easy-api/
"""
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

import json


class BDEAResponse(object):

    """API response."""

    def __init__(self, response):
        """Initialize response."""
        self.response = response


class BDEAStatusResponse(object):

    """API status response."""

    def __init__(self, response):
        """Initialize status response."""
        self.response = response


class BDEAClient(object):

    """API client."""

    API_URL = ('http://check.block-disposable-email.com/'
               'easyapi/json/{apikey}/{domain}')
    STATUS_API_URL = ('http://status.block-disposable-email.com/'
                      'status/?apikey={apikey}')

    TEST_DOMAIN_OK = 'ok.bdea.cc'
    TEST_DOMAIN_BLOCK = 'block.bdea.cc'

    def __init__(self, apikey):
        """Initialize API client."""
        self.apikey = apikey
