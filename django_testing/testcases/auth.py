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
        cls.user_password = 'testinghelloworld'
        cls.user = create_user(password=cls.user_password)
        cls.user_client = Client()
        user_to_authenticate, user_password = cls.get_user_to_authenticate()
        cls.user_client.login(username=user_to_authenticate.username,
                              password=user_password)

    @classmethod
    def get_user_to_authenticate(cls):
        return cls.user, cls.user_password
