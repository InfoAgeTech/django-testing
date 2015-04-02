from __future__ import unicode_literals

import django
from django.test.testcases import TestCase

from ..user_utils import create_user


class UserTestCase(TestCase):
    """Test case that includes a user that can be accessed on the class as
    cls.user.
    """
    @classmethod
    def setUpClass(cls):
        super(UserTestCase, cls).setUpClass()
        if django.VERSION < (1, 8):
            cls.addClassUser()

    @classmethod
    def setUpTestData(cls):
        """Django 1.8 way of adding test data to class."""
        super(UserTestCase, cls).setUpTestData()
        cls.addClassUser()

    @classmethod
    def addClassUser(cls):
        """Adds a user to the class for the test case."""
        cls.user_password = 'testinghelloworld'
        cls.user = create_user(password=cls.user_password)


class AuthenticatedUserTestCase(UserTestCase):
    """Test case that authenticates the test client."""
    authenticated_client = None

    def setUp(self):
        super(AuthenticatedUserTestCase, self).setUp()
        user_to_authenticate, user_password = self.get_user_to_authenticate()
        self.client.login(username=user_to_authenticate.username,
                          password=user_password)

    @classmethod
    def get_user_to_authenticate(cls):
        return cls.user, cls.user_password
