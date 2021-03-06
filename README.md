Python client for block-disposable-email.com
============================================

Installation
------------

    pip install block-disposable-email

Simple usage (email)
--------------------

    from bdea.client import is_disposable_email

    if is_disposable_email('spam@mailinator.com', 'example_apikey_12345'):
        print("Email is disposable")
    else:
        print("Email is valid")


Simple usage (domain)
---------------------

    from bdea.client import is_disposable_domain

    if is_disposable_domain('mailinator.com', 'example_apikey_12345'):
        print("Domain is disposable")
    else:
        print("Domain is valid")


Django validator
----------------

Add your apikey to Django settings.py:

     BDEA_APIKEY = 'example_apikey_12345'

Add validator to your EmailField:

    from django import forms
    from bdea.django_validators import disposable_email_validator

    class EmailField(forms.EmailField):
        default_validators = forms.EmailField.default_validators + [disposable_email_validator]


Advanced usage
--------------

    from bdea.client import BDEAClient

    cl = BDEAClient('example_apikey_12345', timeout=5)

    # examine API status
    res = cl.get_api_status()
    print(res.status(), res.credit_status(), res.credits())

    # get raw API response
    print(res.response)

    # validate domain
    res = cl.get_domain_status('mailinator.com')
    print(res.is_disposable(), res.status())

    # get raw API response
    print(res.response)


Development
-----------

To bootstrap your development environment, install virtualenvwrapper and run the following commands from project directory:

    mkvirtualenv disposable
    setvirtualenvproject
    pip install -r requirements/dev.txt
    pip install -e ./

To run tests use py.test, or run the following command:

    tox
