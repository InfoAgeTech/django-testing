# -*- coding: utf-8 -*-
from django.test.client import Client
from django.utils import unittest
from ..user_utils import create_user


class UnauthenticatedUserTestCase(unittest.TestCase):
    pass


class AuthenticatedUserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(AuthenticatedUserTestCase, cls).setUpClass()
        user_password = 'testinghelloworld'
        cls.user = create_user(password=user_password)
        cls.client = Client()
        cls.client.login(username=cls.user.username, password=user_password)
