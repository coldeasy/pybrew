#!/usr/bin/env python
from distutils.core import setup

from pybrew import __version__

setup(name='Python Brewer',
      version=__version__,
      description='Brewtomator',
      author='Colin Deasy',
      author_email='coldeasy@gmail.com',
      packages=['pybrew'],
      )
