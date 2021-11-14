"""Custom Exceptions"""

class InvalidAuthToken(Exception):
    """
    InvalidAuthToken class
    Exception that can be raised when the Jira auth token
    given as parameter is Invalid.
    """

class FailedToUpdate(Exception):
    """
    FailedToUpdate class
    Exception that can be raised when the Jira failed to update
    given comment.
    """

class FailedToAssigned(Exception):
    """
    FailedToAssigned class
    Exception that can be raised when the Jira assignee
    failed to assign ticket.
    """

class FailedToCopyFile(Exception):
    """
    FailedToCopyFile class
    Exception that can be raised when the file copy from remote to local
    failed.
    """
