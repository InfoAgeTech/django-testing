# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup


classifiers = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='django-testing',
    version='0.0.1',
    description='testing for django',
    author='Troy Grosfield',
    maintainer='Troy Grosfield',
    url='https://github.com/infoagetech/django-testing',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
    setup_requires=[
        'django >= 1.6',
    ],
    classifiers=classifiers
)
