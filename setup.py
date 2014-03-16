#!/usr/bin/env python
from distutils.core import setup

setup(name='Python Brewer',
      version='0.1',
      description='Brewtomator',
      author='Colin Deasy',
      author_email='coldeasy@gmail.com',
      packages=['pybrew', 'pybrew.server'],
      package_dir={'pybrew': 'src/pybrew'}
      )
