from django.contrib.auth import get_user_model
from django.utils import unittest
from django_testing.user_utils import create_user


class SingleUserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(SingleUserTestCase, cls).setUpClass()
        cls.user = create_user()

    @classmethod
    def tearDownClass(cls):
        super(SingleUserTestCase, cls).tearDownClass()
        try:
            cls.user.delete()
        except:
            # Don't care if this fails.
            pass