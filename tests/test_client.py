# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import StringIO
import json

import pytest
from mock import patch

from bdea.client import BDEAClient, URLError
from bdea.client import is_disposable_domain, is_disposable_email


class TestBDEAClientRequest(object):

    def test_urlerror_returns_empty(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.side_effect = URLError('No luck!')
            cl = BDEAClient('token')
            assert cl.request('http://www.rottentomatoes.com/') == {}

    def test_invalid_json_returns_empty(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('invalid json')
            cl = BDEAClient('token')
            assert cl.request('http://www.rottentomatoes.com/') == {}

    def test_valid_json(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('{"blah": "blah"}')
            cl = BDEAClient('token')
            assert cl.request('http://www.rottentomatoes.com/') == {'blah': 'blah'}

    def test_do_not_accept_email(self):
        cl = BDEAClient('token')
        with pytest.raises(ValueError):
            cl.get_status('email@example.com')


class TestBDEAClient(object):

    def test_status_urlopen_args(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('{}')
            cl = BDEAClient('token')
            cl.get_api_status()
            url = 'http://status.block-disposable-email.com/status/?apikey=token'
            urlopen_mock.assert_called_with(url, timeout=5)

    def test_domain_urlopen_args(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('{}')
            cl = BDEAClient('token')
            cl.get_status('example.com')
            url = 'http://check.block-disposable-email.com/easyapi/json/token/example.com'
            urlopen_mock.assert_called_with(url, timeout=5)


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


class TestShortcut(object):
    RESPONSE = {
        'domain_status': 'ok',
        'execution_time': 0.0052359104156494,
        'request_status': 'success',
        'server_id': 'mirror5_vienna',
        'servertime': '2015-10-25 5:25:54',
        'version': '0.2'
    }

    def test_domain_shortcut_function(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            res = self.RESPONSE.copy()
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            assert is_disposable_domain('google.com', 'token') == False

            res.update({
                'domain_status': 'block'
            })
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            assert is_disposable_domain('mailinator.com', 'token') == True

    def test_email_shortcut_function(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            res = self.RESPONSE.copy()
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            assert is_disposable_email('email@example.com', 'token') == False

            res.update({
                'domain_status': 'block'
            })
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            assert is_disposable_email('spam@mailinator.com', 'token') == True
