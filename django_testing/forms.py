from django.http.request import QueryDict
from django.utils.http import urlencode


def get_form_with_post_data(form_class, data, **kwargs):
    """Gets a form instance with posted data.
    
    :param form_class: the form class to create the instance for
    :param data: the dict data to pass to the form
    """
    data = QueryDict(urlencode(data))
    return form_class(data=data, **kwargs)
