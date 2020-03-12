# -*- coding: utf-8 -*-
from io import StringIO
import json

import pytest
from unittest.mock import patch

from bdea.client import BDEAClient, URLError
from bdea.client import is_disposable_domain, is_disposable_email


class TestBDEAClientRequest(object):

    def test_urlerror_returns_empty(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.side_effect = URLError('No luck!')
            cl = BDEAClient('apikey')
            assert cl.request('http://www.rottentomatoes.com/') == {}

    def test_invalid_json_returns_empty(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('invalid json')
            cl = BDEAClient('apikey')
            assert cl.request('http://www.rottentomatoes.com/') == {}

    def test_valid_json(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('{"blah": "blah"}')
            cl = BDEAClient('apikey')
            assert cl.request('http://www.rottentomatoes.com/') == {'blah': 'blah'}

    def test_do_not_accept_email(self):
        cl = BDEAClient('apikey')
        with pytest.raises(ValueError):
            cl.get_domain_status('email@example.com')


class TestBDEAClient(object):

    def test_status_urlopen_args(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('{}')
            cl = BDEAClient('apikey')
            cl.get_api_status()
            url = 'http://status.block-disposable-email.com/status/?apikey=apikey'
            urlopen_mock.assert_called_with(url, timeout=5)

    def test_domain_urlopen_args(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            urlopen_mock.return_value = StringIO('{}')
            cl = BDEAClient('apikey')
            cl.get_domain_status('example.com')
            url = 'http://check.block-disposable-email.com/easyapi/json/apikey/example.com'
            urlopen_mock.assert_called_with(url, timeout=5)


class TestBDEAClientLive(object):
    APIKEY_INVALID = 'invalid-unittest-apikey'
    APIKEY_VALID = 'YOUR-OWN-VALID-APIKEY'

    def test_invalid_apikey_domain_ok(self):
        res = BDEAClient(self.APIKEY_INVALID).get_domain_status(BDEAClient.TEST_DOMAIN_OK)
        assert res.response['domain_status'] == 'ok'
        assert res.response['request_status'] == 'fail_key'

    def test_invalid_apikey_domain_block(self):
        res = BDEAClient(self.APIKEY_INVALID).get_domain_status(BDEAClient.TEST_DOMAIN_BLOCK)
        assert res.response['domain_status'] == 'ok'
        assert res.response['request_status'] == 'fail_key'

    def test_invalid_apikey_api_status(self):
        res = BDEAClient(self.APIKEY_INVALID).get_api_status()
        assert res.response['request_status'] == 'ok'
        assert res.response['apikeystatus'] == 'inactive'

    @pytest.mark.xfail
    def test_valid_apikey_api_status(self):
        res = BDEAClient(self.APIKEY_VALID).get_api_status()
        assert res.response['request_status'] == 'ok'
        assert res.response['apikeystatus'] == 'active'

    @pytest.mark.xfail
    def test_valid_apikey_domain_ok(self):
        res = BDEAClient(self.APIKEY_VALID).get_domain_status(BDEAClient.TEST_DOMAIN_OK)
        assert res.response['domain_status'] == 'ok'
        assert res.response['request_status'] == 'success'

    @pytest.mark.xfail
    def test_valid_apikey_domain_block(self):
        res = BDEAClient(self.APIKEY_VALID).get_domain_status(BDEAClient.TEST_DOMAIN_BLOCK)
        assert res.response['domain_status'] == 'block'
        assert res.response['request_status'] == 'success'


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
            assert is_disposable_domain('google.com', 'apikey') == False

            res.update({
                'domain_status': 'block'
            })
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            assert is_disposable_domain('mailinator.com', 'apikey') == True

    def test_email_shortcut_function(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            res = self.RESPONSE.copy()
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            assert is_disposable_email('email@example.com', 'apikey') == False

            res.update({
                'domain_status': 'block'
            })
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            assert is_disposable_email('spam@mailinator.com', 'apikey') == True
