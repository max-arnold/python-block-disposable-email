# -*- coding: utf-8 -*-
import json
import pytest
from io import StringIO
from unittest.mock import patch
from django.conf import settings
from django.core.exceptions import ValidationError

from bdea.django_validators import disposable_email_validator

settings.configure(
    DEBUG=True,
    BDEA_APIKEY='bdea-apikey'
)


class TestDjangoValidator(object):
    RESPONSE = {
        'domain_status': 'ok',
        'execution_time': 0.0052359104156494,
        'request_status': 'success',
        'server_id': 'mirror5_vienna',
        'servertime': '2015-10-25 5:25:54',
        'version': '0.2'
    }

    def test_valid_email(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            res = self.RESPONSE.copy()
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            disposable_email_validator('email@example.com')

    def test_disposable_email(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            res = self.RESPONSE.copy()
            res.update({
                'domain_status': 'block'
            })
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            with pytest.raises(ValidationError):
                disposable_email_validator('email@example.com')

    def test_urlopen_args(self):
        with patch('bdea.client.urlopen') as urlopen_mock:
            res = self.RESPONSE.copy()
            urlopen_mock.return_value = StringIO('{}'.format(json.dumps(res)))
            disposable_email_validator('email@example.com')
            url = 'http://check.block-disposable-email.com/easyapi/json/bdea-apikey/example.com'
            urlopen_mock.assert_called_with(url, timeout=5)
