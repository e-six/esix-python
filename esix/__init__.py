#!/usr/bin/env python3
"""
High level frontend for the e621 JSON API.
"""

__version__ = "1.3.2"
__author__ = "Alex Schaeffer"
__copyright__ = "Copyright (c)2017, " + __author__

__all__ = ["api", "config", "errors", "post", "comment", "user",
           "tag", "pool", "takedown", "forum", "ticket"]

from . import *
