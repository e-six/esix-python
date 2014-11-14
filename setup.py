#!/usr/bin/env python3
"""
Copyright (c)2014 Alex Schaeffer
"""

from setuptools import setup
import esix

setup(name='esix',
      version=esix.__version__,
      description='High level frontend for the e621 JSON API.',
      url='https://bitbucket.org/AMV_Ph34r/python-esix',
      author=esix.__author__,
      author_email="AMVPh34r@gmail.com",
      install_requires=['requests'],
      license='MIT',
      packages=['esix'])
