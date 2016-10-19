#!/usr/bin/python

'''These are the request objects used to make batch affecting calls
    Reference:
        https://www.worldpay.com/us/developers/apidocs/settlement.html

    Main Classes
        BatchRequest - used for close, get, and get by id batch operations
'''
import logging

from wptotal import worldpay

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


class BatchRequest(object):
    '''This is the main class used to clase a batch. It is used to close, get and get by id'''

    def __init__(self):
        log.debug("BatchRequest class:")
        self.developerApplication = {}  # supplied by serialize. No need to fill this in

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "developerApplication": self.developerApplication
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an emoty value
        return d
