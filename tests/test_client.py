# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import StringIO

from mock import patch

from bdea.client import BDEAClient, URLError


class TestBDEAClientRequest(object):

    def test_urlerror_returns_none(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.side_effect = URLError('No luck!')
            cl = BDEAClient('token')
            assert cl.request('http://www.rottentomatoes.com/') == None

    def test_invalid_json_returns_none(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('invalid json')
            cl = BDEAClient('token')
            assert cl.request('http://www.rottentomatoes.com/') == None

    def test_valid_json(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('{"blah": "blah"}')
            cl = BDEAClient('token')
            assert cl.request('http://www.rottentomatoes.com/') == {'blah': 'blah'}


class TestBDEAClientLive(object):
    TOKEN_INVALID = 'invalid-unittest-token'

    def test_invalid_token_domain_ok(self):
        res = BDEAClient(self.TOKEN_INVALID).get_status(BDEAClient.TEST_DOMAIN_OK)
        assert res.response['domain_status'] == 'ok'
        assert res.response['request_status'] == 'fail_key'

    def test_invalid_token_domain_block(self):
        res = BDEAClient(self.TOKEN_INVALID).get_status(BDEAClient.TEST_DOMAIN_BLOCK)
        assert res.response['domain_status'] == 'ok'
        assert res.response['request_status'] == 'fail_key'

    def test_invalid_token_api_status(self):
        res = BDEAClient(self.TOKEN_INVALID).get_api_status()
        assert res.response['request_status'] == 'ok'
        assert res.response['apikeystatus'] == 'inactive'
