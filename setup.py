# -*- coding: utf-8 -*-
"""This module contains the tool of collective.recipe.pip."""
import codecs
import os

from setuptools import setup, find_packages


def read(*rnames):
    """Read the file name."""
    with codecs.open(os.path.join(os.path.dirname(__file__), *rnames), encoding='utf-8') as fd:
        return fd.read()

version = '0.3.3'

long_description = (
    read('README.rst')
    + '\n' +
    read('CONTRIBUTORS.rst')
    + '\n' +
    read('CHANGES.rst')
)

entry_point = 'collective.recipe.pip:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = [
    'zope.testing', 'zc.buildout', 'mr.scripty', 'manuel', 'z3c.coverage', 'zope.interface']

setup(
    name='collective.recipe.pip',
    version=version,
    description="zc.buildout recipe to parse pip config files ang use parsed info in a buildout.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
    keywords='zc.buildout buildout recipe',
    author='Anatoly Bubenkov',
    author_email='bubenkoff@gmail.com',
    url='http://github.com/collective/collective.recipe.pip',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
        'pip',
        # -*- Extra requirements: -*-
    ],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    test_suite='collective.recipe.pip.testing.test_docs.test_suite',
    entry_points=entry_points,
    dependency_links=[
        'https://github.com/minddistrict/mr.scripty/archive/4bbfa2b48b7bc8a215c80a19e61ac39d0c9545aa.zip#egg=mr.scripty'
    ]
)
