
from django.test import TestCase
from django_testing.user_utils import create_user


class SingleUserTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SingleUserTestCase, cls).setUpClass()
        cls.user = create_user()

    @classmethod
    def tearDownClass(cls):
        super(SingleUserTestCase, cls).tearDownClass()
        cls.user.delete()
