# -*- coding: utf-8 -*-
from .auth import AuthenticatedUserTestCase
from django.utils import unittest


class BaseUrlTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('NOTE: {0} are running which will slow down the speed '
              'of the tests since it queries all the view mixins as '
              'well.'.format(cls.__name__))
        super(BaseUrlTestCase, cls).setUpClass()


class UnauthenticatedUrlTestCase(BaseUrlTestCase):
    pass


class AuthenticatedUserUrlTestCase(AuthenticatedUserTestCase,
                                   BaseUrlTestCase):

    def status_code_200_response_test(self, url):
        """Test that a response returns a successful 200 response."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
