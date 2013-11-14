# -*- coding: utf-8 -*-


class UrlTestCaseMixin(object):
    """Url Test case for urls.

    The consuming TestCase must implement one of the following attributes:

    * expected_url_tests: a list of test names to test urls
    * urlpatterns: this is a tuple of url patterns (likely coming from urls.py)
    * url_names = a collection of string url names to test.

    Example:

    from user_connections.urls import urlpatterns

    class UserConnectionGetUrlTests(BaseUrlTestCase):
        urlpatterns = urlpatterns
    """

    @classmethod
    def setUpClass(cls):
        super(UrlTestCaseMixin, cls).setUpClass()
        cls.actual_url_test_names = [t for t in cls.__dict__.keys()
                                     if t.startswith('test_')]

        if not hasattr(cls, 'expected_url_tests'):

            cls.url_names = cls.get_url_names()

            if hasattr(cls, 'url_names') and cls.url_names:
                cls.expected_url_tests = [u'test_{0}_view'.format(n)
                                          for n in cls.url_names]

    @classmethod
    def get_url_names(cls):
        if hasattr(cls, 'url_names') and cls.url_names:
            return cls.url_names

        if hasattr(cls, 'urlpatterns'):
            return [p.name for p in cls.urlpatterns if hasattr(p, 'name')]

    def test_all_views_tested(self):
        """This test ensures that all urls have a test written for them."""

        if not hasattr(self, 'expected_url_tests'):
            raise Exception(u'"expected_url_tests" or "urlpatterns" must be '
                             'implemented by TestCase {0}'.format(
                                                    self.__class__.__name__))

        missing_tests = set(self.expected_url_tests).difference(
                                                    self.actual_url_test_names)
        missing_url_names = []
        for t in missing_tests:
            if not t.startswith('test_'):
                continue

            if t.endswith('_view'):
                missing_url_names.append(t[5:-5])
            else:
                missing_url_names.append(t[5:])

        self.assertEqual(missing_tests, set([]),
            msg=u'{0} is missing tests for the following url names: {1}\n\n'
                 'Test method names should following the pattern '
                 '"test_{{url_name}}_view".'.format(
                                            self.__class__.__name__,
                                            u', '.join(missing_url_names)))

    def status_code_200_response_test(self, url):
        """Test that a response returns a successful 200 response."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
