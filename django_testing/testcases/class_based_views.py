from django.test.client import RequestFactory


class ClassBasedViewTestResponse(object):
    """Gets a response from a class based view via the request factory."""

    def get_response(self, view, url, user, data=None, method='get',
                     request_kwargs=None, view_kwargs=None, **kwargs):
        """
        Get a response for a class based view.

        :param view: the class based view
        :param url: the url to test
        :param user: the request authenticated user
        :param data: dict of data to send with the request
        :param method: the http view method to test ('get', 'post', etc)
        :param request_kwargs: the kwargs to apply to the request method
        :param view_kwargs: dict of args to apply to the view
        """
        if view_kwargs is None:
            view_kwargs = {}

        if request_kwargs is None:
            request_kwargs = {}

        factory = RequestFactory()
        factory_func = getattr(factory, method)

        request = factory_func(url, data=data or {}, **request_kwargs)
        request.user = user

        return view.as_view()(request, **view_kwargs)

    def get_post_response(self, view, url, user, data=None,
                          request_kwargs=None, view_kwargs=None, **kwargs):
        """Gets the post response for a class based view."""
        kwargs['method'] = 'post'
        return self.get_response(view=view,
                                 url=url,
                                 user=user,
                                 data=data,
                                 request_kwargs=request_kwargs,
                                 view_kwargs=view_kwargs,
                                 **kwargs)

    def get_ajax_response(self, view, url, user, data=None, method='get',
                          request_kwargs=None, view_kwargs=None, **kwargs):
        """
        Gets a class base view's ajax response.
        """
        if request_kwargs is None:
            request_kwargs = {}

        request_kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        return self.get_response(view=view,
                                 url=url,
                                 user=user,
                                 data=data,
                                 method=method,
                                 request_kwargs=request_kwargs,
                                 view_kwargs=view_kwargs,
                                 **kwargs)

    def get_ajax_post_response(self, view, url, user, data=None,
                               request_kwargs=None, view_kwargs=None,
                               **kwargs):
        """
        Gets a class base view's ajax response.
        """
        kwargs['method'] = 'post'
        return self.get_ajax_response(view=view,
                                      url=url,
                                      user=user,
                                      data=data,
                                      request_kwargs=request_kwargs,
                                      view_kwargs=view_kwargs,
                                      **kwargs)
