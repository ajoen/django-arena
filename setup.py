import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-arena',
    version='0.1',
    packages=['arena',],
    include_package_data=True,
    license='Apache License, Version 2.0',
    description='Flexible forum application for django 1.5+',
    long_description=README,
    url='https://github.com/ajoen/django-arena/',
    author='ajoen Labs',
    author_email='onur+django_arena@ajoen.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License, Version 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)