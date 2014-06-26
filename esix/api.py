#!/usr/bin/env python3
"""
Standard functions for e621's JSON API.
"""

import json
import urllib.request

from . import config, errors


def _get_page(url):
    """Fetch the content from a given web URL.

    :param url: The URL to fetch.
    :type url: str
    :returns: Content retrieved from URL, or None if an error occured.
    :rtype: HTTPResponse
    :raises: errors.APIGetError
    """
    try:
        req = urllib.request.Request(url,
                                     headers={'User-Agent':config.USER_AGENT})
        page = urllib.request.urlopen(req)
    except (urllib.error.HTTPError, ValueError, urllib.error.URLError):
        page = None
    if page is None: raise errors.APIGetError('Unable to open URL: '+str(url))
    return page

def _post_data(data, url):
    """Post the given data object to the given URL.

    :param data: A dict or tuple of tuples with the data to post.
    :type data: dict or tuple
    :param url: The URL to post to.
    :type url: str
    :returns: Content of the response, or None if an error occured.
    :rtype: HTTPResponse
    :raises: errors.APIPostError
    """
    err = None
    try:
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
    except TypeError as e: err = e
    if err: raise errors.APIPostError('The data object is not URL-encodable.')
    try:
        req = urllib.request.Request(url,
                                     headers={'User-Agent':config.USER_AGENT})
        result = urllib.request.urlopen(req,data)
    except (urllib.error.HTTPError, ValueError, urllib.error.URLError) as e:
        err = e
    if err: raise errors.APIPostError(str(err))
    return result

def _get_data_obj(page):
    """Parse a JSON-structured HTTPResponse into a Python object.

    :param page: The JSON-encoded page content to fetch.
    :type page: HTTPResponse
    :returns: The decoded JSON object.
    :rtype: dict or list
    :raises: errors.JSONError
    """
    data = None
    try: data = json.loads(page.read().decode('utf-8'))
    except (ValueError, AttributeError): pass
    if data is None:
        raise errors.JSONError('The supplied page data is not JSON-decodable.')
    return data

def _fetch_data(url):
	"""Fetches a URL's page content, then converts it into a JSON object.

	:param url: The URL of the JSON-encoded page.
	:type url: str
	:returns: The decoded JSON object.
	:rtype: dict
	"""
	return _get_data_obj(_get_page(url))