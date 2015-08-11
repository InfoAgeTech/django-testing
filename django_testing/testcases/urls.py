from __future__ import unicode_literals

from django.core.urlresolvers import RegexURLPattern


class HttpResponseTestMixin(object):
    """Test mixin for testing different http responses by url."""

    def response_test_get(self, url, data=None, expected_status_code=200,
                          **kwargs):
        """Helper for http GET requests.  Default status code is 200.

        :param url: the url the test hits.
        :param data: the data use to pass to the url. This becomes
            querystring params. See:
            https://docs.djangoproject.com/en/1.6/topics/testing/overview/#django.test.client.Client.get
        :param expected_status_code: the status code to assert from the request
        :param kwargs: any other pieces of data to pass to the GET request
        """
        return self.response_test(method='get',
                                  url=url,
                                  expected_status_code=expected_status_code,
                                  data=data,
                                  **kwargs)

    def response_test_post(self, url, data=None, expected_status_code=302,
                           **kwargs):
        """Helper for http POST requests.  Default status code is 302,
        redirect.

        :param url: the url the test hits.
        :param data: the data use to pass to the url. This is POST data
            https://docs.djangoproject.com/en/1.6/topics/testing/overview/#django.test.client.Client.post
        :param expected_status_code: the status code to assert from the request
        :param kwargs: any other pieces of data to pass to the GET request
        """
        return self.response_test(method='post',
                                  url=url,
                                  expected_status_code=expected_status_code,
                                  data=data,
                                  **kwargs)

    def response_test(self, method, url, expected_status_code, data=None,
                      **kwargs):
        """Helper for HTTP method tests.

        :param method: string that can be ONE of the following http methods:
            GET, POST, HEAD, PUT, DELETE.
        :param url: the url the test hits.
        :param expected_status_code: the status code to assert from the request
        """
        if data is not None:
            kwargs['data'] = data

        # Gets the function off self.client for the specific http method.
        # Method == "get" will return the self.client's "get(...)" method.
        http_method_func = getattr(self.client, method.lower())
        response = http_method_func(url, **kwargs)
        is_correct_status_code = response.status_code == expected_status_code

        if not is_correct_status_code and \
           response.context and \
           'form' in response.context:

            error_message = 'AssertionError: {0} != {1}: \n{2}'.format(
                response.status_code,
                expected_status_code,
                response.context['form']._errors
            )
        elif not is_correct_status_code and response.status_code == 302:
            error_message = ('AssertionError: {0} != {1}: \nUnexpected '
                             'redirect to: {2}').format(
                response.status_code,
                expected_status_code,
                response.url
            )
        else:
            error_message = None

        self.assertEqual(response.status_code, expected_status_code,
                         msg=error_message)
        return response


class UrlTestCaseMixin(HttpResponseTestMixin):
    """Url Test case for urls.

    The consuming TestCase must implement one of the following attributes:

    * expected_url_tests: a list of test names to test urls
    * urlpatterns: this is a tuple of url patterns (likely coming from urls.py)
    * url_names = a collection of string url names to test.

    If the test case needs to ignore url patterns, then set the test case
    attribute:

    * exclude_urlpatterns: urlpatterns to exclude from the testcase
    * exclude_url_names: url names to exclude

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

        exclude_urlpatterns = getattr(cls, 'exclude_urlpatterns', [])

        if exclude_urlpatterns and \
           isinstance(exclude_urlpatterns[0], RegexURLPattern):
            # There's only one set of url patterns to exclude
            exclude_patterns = exclude_urlpatterns

        else:
            # There are multiple lists of url patterns to exclude
            exclude_patterns = []
            for p in exclude_urlpatterns:
                exclude_patterns += p

        exclude_url_names = [p.name for p in exclude_patterns]
        exclude_url_names.extend(getattr(cls, 'exclude_url_names', []))
        exclude_url_names = list(set(exclude_url_names))

        if hasattr(cls, 'urlpatterns'):

            url_pattern_names = []

            def get_url_pattern_names(urllist, depth=0):
                for entry in urllist:
                    if hasattr(entry, 'url_patterns'):
                        get_url_pattern_names(entry.url_patterns, depth + 1)
                    elif entry.name not in exclude_url_names:
                        url_pattern_names.append(entry.name)

            get_url_pattern_names(cls.urlpatterns)

            return url_pattern_names

    def test_all_views_tested(self, *args, **kwargs):
        """This test ensures that all urls have a test written for them."""

        if not hasattr(self, 'expected_url_tests'):
            raise Exception('"expected_url_tests" or "urlpatterns" must be '
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

        msg = ('{0} is missing tests for the following {1} url names:\n\n '
               '* {2}\n\nTest method names should following the pattern '
               '"test_{{url_name}}_view".')
        msg = msg.format(
            self.__class__.__name__,
            len(missing_url_names),
            '\n * '.join(missing_url_names)
        )
        self.assertEqual(missing_tests, set([]), msg=msg)
