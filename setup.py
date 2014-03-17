#!/usr/bin/env python
from distutils.core import setup

setup(name='Python Brewer',
      version='0.2',
      description='Brewtomator',
      author='Colin Deasy',
      author_email='coldeasy@gmail.com',
      packages=['pybrew', 'pybrew.server', 'pybrew.workers'],
      package_dir={'pybrew': 'src/pybrew'}
      )
