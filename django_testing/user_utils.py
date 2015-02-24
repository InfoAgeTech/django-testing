from django.contrib.auth import get_user_model
import uuid


def random_string(length=10):
    return uuid.uuid4().hex[:length]


def create_user(username=None, email=None, is_staff=False, is_superuser=False,
                **kwargs):
    """Creates a user for testing purposes."""
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


def create_superuser(username=None, email=None, **kwargs):
    """Creates a super user for testing purposes."""
    kwargs['is_staff'] = True
    kwargs['is_superuser'] = True
    return create_user(username=username, email=email, **kwargs)
