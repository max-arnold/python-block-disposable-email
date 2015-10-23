# -*- coding: utf-8 -*-
"""Python client for block-disposable-email.com service.

http://www.block-disposable-email.com/cms/help-and-usage/easy-api/
"""
try:
    # PY3
    from urllib.request import urlopen
    from urllib.error import URLError
except ImportError:
    # PY2
    from urllib2 import urlopen
    from urllib2 import URLError

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

    def __init__(self, apikey, timeout=5):
        """Initialize API client."""
        self.apikey = apikey
        self.timeout = timeout

    def request(self, url, timeout=None):
        """Make HTTP GET request and return parsed JSON dict or None if error."""
        timeout = timeout or self.timeout
        try:
            res = urlopen(url, timeout=timeout)
        except URLError as e:
            return None

        try:
            return json.loads(res.read())
        except ValueError:
            return None
