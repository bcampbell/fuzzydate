#from distutils.core import setup
from setuptools import setup

setup(
    name='fuzzydate',
    version='0.1.0',
    author='Ben Campbell',
    author_email='ben@scumways.com',
    packages=['fuzzydate', 'fuzzydate.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/fuzzydate/',
    license='LICENSE.txt',
    description='Date parser',
    long_description=open('README.txt').read(),
    test_suite='fuzzydate.test.tests'
)
