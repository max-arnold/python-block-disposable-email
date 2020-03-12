# -*- coding: utf-8 -*-
from bdea.client import BDEAStatusResponse


class TestBDEAStatusResponse(object):

    RESPONSE = {
        'apikeystatus': 'active',
        'commercial_credit_status': 'exhausted',
        'commercial_credit_status_percent': 0,
        'credits': '0',
        'credits_time': '2015-10-24 13:15:08',
        'request_status': 'ok',
        'servertime': '2015-10-24 13:38:38',
        'version': '1.3'
    }

    def test_empty_response_is_not_valid(self):
        res = BDEAStatusResponse({})
        assert res.status() == False

    def test_empty_response_means_zero_credits(self):
        res = BDEAStatusResponse({})
        assert res.credits() == 0

    def test_empty_response_means_exausted_credits(self):
        res = BDEAStatusResponse({})
        assert res.credit_status() == 'exhausted'

    def test_request_status_and_apikey_status(self):
        res = self.RESPONSE.copy()
        res.update({
            'request_status': 'ok',
            'apikeystatus': 'active'
        })
        assert BDEAStatusResponse(res).status() == True

        res.update({
            'request_status': 'ok',
            'apikeystatus': 'inactive'
        })
        assert BDEAStatusResponse(res).status() == False

        res.update({
            'request_status': 'fail',
            'apikeystatus': 'active'
        })
        assert BDEAStatusResponse(res).status() == False

    def test_credit_status(self):
        res = self.RESPONSE.copy()
        for ccs in ('good', 'low', 'exhausted'):
            res.update({
                'request_status': 'ok',
                'apikeystatus': 'active',
                'commercial_credit_status': ccs
            })
            assert BDEAStatusResponse(res).credit_status() == ccs

    def test_credits(self):
        res = self.RESPONSE.copy()
        res.update({
            'request_status': 'ok',
            'apikeystatus': 'active',
            'credits': '100'
        })
        assert BDEAStatusResponse(res).credits() == 100
