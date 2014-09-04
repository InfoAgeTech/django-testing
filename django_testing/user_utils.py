import uuid

from django.contrib.auth import get_user_model


def random_string(length=10):
    return uuid.uuid4().hex[:length]


def create_user(username=None, email=None, is_staff=False, is_superuser=False,
                **kwargs):

    if not username:
        username = random_string()

    if not email:
        email = '{0}@{1}.com'.format(random_string(), random_string())

    if 'first_name' not in kwargs:
        kwargs['first_name'] = random_string()

    if 'last_name' not in kwargs:
        kwargs['last_name'] = random_string()

    kwargs['username'] = username
    kwargs['email'] = email

    if 'password' not in kwargs:
        kwargs['password'] = 'password'

    User = get_user_model()

    if is_superuser:
        return User.objects.create_superuser(**kwargs)

    user = User.objects.create_user(**kwargs)

    if is_staff:
        user.is_staff = True
        user.save()

    return user
