#!/usr/bin/env python3
"""
High level frontend for the e621 JSON API.
"""

__version__ = "1.2.3"
__author__ = "Alex Schaeffer"
__copyright__ = "Copyright (c)2014, " + __author__

__all__ = ["api", "config", "errors", "post", "comment",
           "user", "tag", "pool", "takedown", "forum"]

from . import *
