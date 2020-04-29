#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Package setup
#
# ------------------------------------------------


# imports
# -------
import re
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


# config
# ------
class Config:
    def __init__(self, fi):
        with open(fi) as meta:
            for m in re.findall(r'(__[a-z]+__).*=.*[\'"](.+)[\'"]', meta.read()):
                setattr(self, m[0], m[1])
        return


config = Config('flask_continuum/__init__.py')


# requirements
# ------------
with open('requirements.txt', 'r') as reqs:
    requirements = list(map(lambda x: x.rstrip(), reqs.readlines()))

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-runner'
]


# readme
# ------
with open('README.rst') as readme_file:
    readme = readme_file.read()


# exec
# ----
setup(
    name=config.__pkg__,
    version=config.__version__,
    description=config.__info__,
    long_description=readme,
    author=config.__author__,
    author_email=config.__email__,
    url=config.__url__,
    packages=find_packages(exclude=['tests']),
    license="MIT",
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=requirements,
    keywords=[config.__pkg__, 'flask', 'versioning', 'history', 'provenance', 'continuum'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        # "Programming Language :: Python :: 2",
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    tests_require=test_requirements
)
