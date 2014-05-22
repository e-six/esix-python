#!/usr/bin/env python3
"""
File-manipulating functions for the e621 API.
"""

import hashlib
import json
import os
import shutil
import win32api, win32con

from . import api, config, errors, post


def get_file_md5(filename):
    """Calculate the md5 checksum of a file.

    :param filename: The path of the file to check.
    :type filename: str
    :returns: The file's md5 checksum.
    :rtype: str
    """
    f = open(filename,'rb')
    md5 = hashlib.md5(f.read()).hexdigest()
    f.close()
    return md5

def file_exists(folder,name):
    """Returns whether or not a file exists in a given folder.

    :param folder: The local folder to search.
    :type folder: str
    :param name: The filename to look for.
    :type name: str
    :returns: True if the file exists, False otherwise.
    :rtype: bool
    """
    return os.path.isfile(folder+name)

def file_md5_exists(folder,md5):
    """Returns whether or not a file with a given md5 checksum is in a folder.

    :param folder: The local folder to search.
    :type folder: str
    :param md5: The checksum to look for.
    :type md5: str
    :returns: The file's name if it exists, False otherwise.
    :rtype: str or bool
    """
    for f in os.listdir(folder):
        try:
            if get_file_md5(folder+f) == md5:
                return f
        except PermissionError: pass
    return False

def get_post_data(folder,filename):
    """Fetch locally stored post metadata from a file.

    :param folder: The folder the image is stored in.
    :type folder: str
    :param filename: The name of the image file.
    :type filename: str
    :returns: A post object with all stored information, None on error.
    :rtype: post.Post object
    """
    if folder != "./" and not folder.endswith("/"):
        folder += "/"
    md5 = get_file_md5(folder+filename)
    try: data = json.load(open(folder+'.metadata/'+md5))
    except Exception as err: data = None
    return post.Post(post_data=data)

def store_post_data(post_obj,folder):
    """Save a post's information locally.

    :param post_obj: The post object.
    :type post_obj: post.Post object
    :param folder: The folder in which metadata will be stored
        (in a .metadata/ subfolder)
    :type folder: str
    :returns: Whether or not the operation was successful.
    :rtype: bool
    """
    if folder != './' and not folder.endswith('/'): folder += '/'
    if not os.path.exists(folder+'.metadata/'):
        os.makedirs(folder+'.metadata/')
        try:
            win32api.SetFileAttributes(folder+'.metadata/',
                                       win32con.FILE_ATTRIBUTE_HIDDEN)
        except: pass
    try:
        with open(folder+'.metadata/'+post_obj.md5,'w') as meta_file:
            meta_file.write(json.dumps(post_obj._data))
        return True
    except: return False

def search_local_tags(folder,query):
    """Search a local folder's existing metadata for specified tags.

    :param folder: The folder to search.
    :type folder: str
    :param query: The tag or tags to search for.
    :type query: str
    :returns: A list of matching images found in the folder.
    :rtype: list
    """
    raise errors.APIException('Not ready. Need to support multiple tags.')
    if folder != '' and not folder.endswith('/'): folder += '/'
    matches = []
    if not os.path.isdir(folder+'.metadata'): return []
    meta_folder = folder+'.metadata/'
    for f in os.listdir(meta_folder):
        with open(meta_folder+f) as file_data:
            img_data = json.load(file_data)
        if 'tags' not in img_data: continue
        img_tags = img_data['tags'].split()
        if tag.lower() in img_tags:
            matches.append(f+'.'+img_data['file_ext'])
    return matches

def download_image(post_obj,dest='./',name_format="{md5}.{file_ext}",
                   overwrite=False,write_metadata=False):
    """Downloads a given post object as an image.

    :param post_obj: The post to download.
    :type post_obj: post.Post object
    :param dest: The folder to download to. Default is script directory.
    :type dest: str
    :param name_format: The format of the filename, post data keywords
        should be surrounded by {}. Default {md5}.{file_ext}
    :type name_format: str
    :param overwrite: If True, will overwrite existing files with the
        same name. Default False.
    :type overwrite: bool
    :returns: Whether or not the download succeeded.
    :rtype: bool
    """
    name_format = name_format.replace("{","%(").replace("}",")s")
    if dest != './' and not dest.endswith('/'): dest += '/'
    if type(post_obj) is not post.Post or post_obj.file_url is None:
        raise errors.PostError('Post is not a valid object or does not exist.')
    filename = name_format % post_obj._data
    if not filename.endswith("."+post_obj.file_ext):
        filename += "." + post_obj.file_ext
    file = api._get_page(post_obj.file_url)
    if file and (not file_exists(dest,filename) or overwrite):
        if 'text/html' in file.headers.get('Content-Type'): return False
        with open(dest+filename,'wb') as out_file:
            shutil.copyfileobj(file,out_file)
        if write_metadata: store_post_data(post_obj,dest)
        return True
    return False
