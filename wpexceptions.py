#!/usr/bin/python

''' These are the Worldpay Total defined error types that should be used in Try/Raise
'''

import logging

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class WpInvalidFunctionCallError(Error):  # use this when a function call has invalid parameters
    def __init__(self, m):
        self.message = "Invalid function call: " + m
        log.error(self.message)


class WpTransactionError(Error):  # base class for other transactions
    """Exception raised for errors in the input.
    Attributes:
        m -- explanation of the error
    """

    def __init__(self, m):
        print("m:", m)
        self.message = m


class WpTimeoutError(WpTransactionError):  # transaction timed out
    def __init__(self, m):
        self.message = "Transaction timed out: " + m
        log.error(self.message)


class WpConnectionError(WpTransactionError):  # endpoint rejected the transaction
    def __init__(self, m):
        self.message = "Transaction could not connect: " + m
        log.error(self.message)


class WpTooManyRedirectsError(WpTransactionError):  # transaction was passed around more than the set limit
    def __init__(self, m):
        self.message = "Transaction had too many redirects: " + m
        log.error(self.message)


class WpHTTPError(WpTransactionError):  # HTTP returned something other than 200
    def __init__(self, m):
        self.message = "Transaction returned HTTP error: " + m
        log.error(self.message)


class WpJSONError(WpTransactionError):  # JSON was not formed properly
    def __init__(self, m):
        self.message = "Transaction returned a JSON error: " + m
        log.error(self.message)


class WpBadResponseError(WpTransactionError):  # The REST call indicated a failure
    def __init__(self, m):
        self.message = "Transaction not processed: " + m
        log.error(self.message)


class WpInvalidEndpointError(WpTransactionError):  # REST target is invalid
    def __init__(self, m):
        self.message = "Invalid endpoint: " + m
        log.error(self.message)
