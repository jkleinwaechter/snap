#!/usr/bin/python
'''These are the request objects used to make tokenization calls.
    Reference
        https://www.worldpay.com/us/developers/apidocs/tokenization.html

    Main Classes
        TokenRequest - used for creating a token
'''

import logging

from wptotal import worldpay

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


class TokenRequest(object):
    '''This is the class to use for creating tokens for both card and check
    '''

    def __init__(self):
        log.debug("TokenRequest class:")
        # Required
        self.developerApplication = {}  # supplied by serialize. No need to fill this in
        self.publicKey = ""
        self.card = {}  # call attachCard to fill this in
        # Optional
        self.addToVault = False  # set to True if you want to store the token in the vaulr
        self.customerId = ""  # if not set, the tokenization call will return one

    def serialize(self):
        self.developerApplication = worldpay.devAppId
        self.publicKey = worldpay.publicKey
        s = {
            "developerApplication": self.developerApplication,
            "publicKey": self.publicKey,
            "addToVault": self.addToVault,
            "customerId": self.customerId,
            "card": self.card
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an emoty value
        return d

    def attachCard(self, c):
        '''attach a Card object to this object. C is the Card object'''
        self.card = c.serialize()
