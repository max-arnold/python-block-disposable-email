# -*- coding: utf-8 -*-
from bdea.client import BDEAResponse


class TestBDEAStatus(object):

    RESPONSE = {
        'domain_status': 'ok',
        'execution_time': 0.0052359104156494,
        'request_status': 'success',
        'server_id': 'mirror5_vienna',
        'servertime': '2015-10-25 5:25:54',
        'version': '0.2'
    }

    def test_empty_response_status_false(self):
        res = BDEAResponse({})
        assert res.status() == False

    def test_empty_response_means_domain_is_not_disposable(self):
        res = BDEAResponse({})
        assert res.is_disposable() == False

    def test_status_true(self):
        res = BDEAResponse(self.RESPONSE)
        assert res.status() == True

    def test_status_false(self):
        for rs in ('fail_key',
                   'fail_server',
                   'fail_input_domain',
                   'fail_parameter_count',
                   'fail_key_low_credits'):
            res = self.RESPONSE.copy()
            res['request_status'] = rs
            assert BDEAResponse(res).status() == False

    def test_disposable_domain(self):
        res = self.RESPONSE.copy()
        res.update({
            'request_status': 'success',
            'domain_status': 'block'
        })
        assert BDEAResponse(res).is_disposable() == True

        res.update({
            'request_status': 'fail_input_domain',
            'domain_status': 'ok'
        })
        assert BDEAResponse(res).is_disposable() == True

    def test_nondisposable_domain(self):
        assert BDEAResponse(self.RESPONSE).is_disposable() == False

    def test_request_status_nondisposable_domain(self):
        for rs in ('fail_key',
                   'fail_server',
                   'fail_parameter_count',
                   'fail_key_low_credits'):
            res = self.RESPONSE.copy()
            res.update({
                'request_status': rs,
                'domain_status': 'ok'
            })
            assert BDEAResponse(res).is_disposable() == False
