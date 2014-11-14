#!/usr/bin/env python3
"""
Exception handlers for the API.
"""

class APIException(Exception):
    """
    Base class for all API exceptions.
    """
    pass

class JSONError(APIException):
    """
    Error caused during JSON parsing, generally due to incorrect JSON format.
    """
    pass

class APIError(APIException):
    """
    An error caused during any interaction with the server.
    May signify a problem with the server, or user's connection.
    """
    pass

class APIGetError(APIError):
    """
    Error while fetching the requested page.
    """
    pass

class APIPostError(APIError):
    """
    Error while posting data to a page.
    """
    pass

class SiteLoadError(APIError):
    """
    Error that occurs when the site is under heavy load and cannot return data.
    """
    pass

class APILoginError(APIError):
    """
    An error occured attempting to log in. Either the credentials were
    incorrect or the server is unreachable.
    """
    pass

class APIUnauthorizedError(APIError):
    """
    The apptempted operation requires the user to either be logged in,
    or have higher permissions.
    """
    pass

class PostError(APIException):
    """
    Error trying to retrieve post information.
    """
    pass

class PostNotFoundError(PostError):
    """
    The requested post could not be found.
    """
    pass

class BadPostError(PostError):
    """
    A post object is not structured correctly, or data is missing.
    """
    pass

class PoolError(APIException):
    """
    Error trying to retrieve pool information.
    """
    pass

class PoolNotFoundError(PoolError):
    """
    The requested pool could not be found.
    """
    pass

class BadPoolError(PoolError):
    """
    A pool object is not structured correctly, or data is missing.
    """
    pass

class CommentError(APIException):
    """
    Error trying to retrieve comment information.
    """
    pass

class CommentNotFoundError(CommentError):
    """
    The requested comment could not be found.
    """
    pass

class BadCommentError(CommentError):
    """
    A comment object is not structured correctly, or data is missing.
    """
    pass

class UserError(APIException):
    """
    Error trying to retrieve user information.
    """
    pass

class UserNotFoundError(UserError):
    """
    The requested user could not be found.
    """
    pass

class BadUserError(UserError):
    """
    A user objct is not structured correctly, or data is missing.
    """
    pass

class TagError(APIException):
    """
    Error trying to retrieve tag information.
    """
    pass

class TagNotFoundError(TagError):
    """
    The requested tag could not be found.
    """
    pass

class BadTagError(TagError):
    """
    A tag objct is not structured correctly, or data is missing.
    """
    pass

class TakedownError(APIException):
    """
    Error trying to retrieve takedown information.
    """
    pass

class TakedownNotFoundError(TakedownError):
    """
    The requested takedown could not be found.
    """
    pass

class BadTakedownError(TakedownError):
    """
    A takedown object is not structured correctly, or data is missing.
    """
    pass

class ForumError(APIException):
    """
    Error trying to retrieve forum post/thread information.
    """
    pass

class ForumPostNotFoundError(ForumError):
    """
    The requested forum post cannot be found.
    """
    pass

class BadForumPostError(ForumError):
    """
    A forum post object is not structured correctly, or data is missing.
    """
    pass

class TicketError(APIException):
    """
    Error trying to retrieve ticket information.
    """
    pass

class TicketNotFoundError(TagError):
    """
    The requested ticket could not be found.
    """
    pass

class BadTicketError(TagError):
    """
    A ticket objct is not structured correctly, or data is missing.
    """
    pass

class FileError(APIException):
    """
    An error occured during the handling of local files.
    """
    pass

class FileNotFoundError(FileError):
    """
    The requested file could not be found.
    """
    pass

class FileDownloadError(FileError):
    """
    The requested image could not be downloaded.
    """
    pass
