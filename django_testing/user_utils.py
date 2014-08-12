import uuid

from django.contrib.auth import get_user_model


User = get_user_model()
random_string = lambda len = None: uuid.uuid4().hex[:len or 10]


def create_user(username=None, email=None, **kwargs):

    if not username:
        username = random_string()

    if not email:
        email = '{0}@{1}.com'.format(random_string(), random_string())

    if 'first_name' not in kwargs:
        kwargs['first_name'] = random_string()

    if 'last_name' not in kwargs:
        kwargs['last_name'] = random_string()

    return User.objects.create_user(username=username, email=email, **kwargs)
