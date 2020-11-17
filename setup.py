#!/usr/bin/env python

import unittest

from setuptools import find_packages, setup

from corona_cli_germany.version import get_version


def collect_tests():
    ''' Sets up unit testing
    '''
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.', pattern='test_*.py')
    return test_suite


def main():
    setup(name='corona-cli-germany',
          version=get_version(),
          description='Corona CLI for Germany. Reports daily cases.',
          author='Constantin Diez',
          author_email='qd.eng.contact@gmail.com',
          url='https://github.com/lasso-codie/corona-cli-germany',
          license="MIT",
          install_requires=[
              "rich",
              "requests",
              "flask",
          ],
          packages=find_packages(),
          package_data={
              '': ['*.png', '*.html', '*.js', '*.so', '*.dll', '*.txt', '*.css'],
          },
          test_suite='setup.collect_tests',
          zip_safe=False,
          )


if __name__ == "__main__":
    main()
