from __future__ import unicode_literals

from django.test import Client
from django.test.testcases import TestCase

from ..user_utils import create_user


class UnauthenticatedUserTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(UnauthenticatedUserTestCase, cls).setUpClass()
        cls.user_client = Client()


class AuthenticatedUserTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(AuthenticatedUserTestCase, cls).setUpClass()
        user_password = 'testinghelloworld'
        cls.user = create_user(password=user_password)
        cls.user_client = Client()
        cls.user_client.login(username=cls.user.username,
                              password=user_password)
