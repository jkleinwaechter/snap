#!/usr/bin/python
'''These are the request objects used to search/get/update transactions
    Reference
        http://apidocs.securenet.com/docs/transactions.html?lang=JSON

    Main Classes
        SearchTransactionsRequest - find transactions meeting provided criteria
        GetTransactionRequest - Retrieve an individual transaction by its transaction id
        UpdateTransactionRequest - Update an existing transaction
'''

import logging

from wptotal import worldpay

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


class SearchTransactionsRequest(object):
    '''This is the main class to be used when performing a search transaction'''

    def __init__(self):
        log.debug("SearchTransactionsRequest class:")
        # Required
        self.developerApplication = {}  # supplied by serialize. No need to fill this in
        # Conditional
        self.startDate = ""
        self.endDate = ""
        # Optional
        self.transactionId = 0
        self.orderId = 0.0  # Fix - is this really decimal or should it be number?
        self.amount = 0.0
        self.customerId = ""

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "developerApplication": self.developerApplication,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "transactionId": self.transactionId,
            "orderId": self.orderId,
            "amount": self.amount,
            "customerId": self.customerId

        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d


class UpdateTransactionRequest(object):
    '''This is the main class to be used when updating a transaction'''

    def __init__(self):
        log.debug("UpdateTransactionRequest class:")
        # Required
        self.developerApplication = {}  # supplied by serialize. No need to fill this in
        self.referenceTransactionId = 0
        # Conditional
        self.signatureImage = ""  # !!Doc!! say array of bytes, but suspect it is reaaly a binary blob - fix
        self.email = ""
        self.emailReceipt = False
        self.levelTwoData = {}
        self.levelThreeData = {}

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "developerApplication": self.developerApplication,
            "developerApplication": self.developerApplication,
            "referenceTransactionId": self.referenceTransactionId,
            "levelTwoData": self.levelTwoData,
            "levelThreeData": self.levelThreeData,
            "signatureImage": self.signatureImage,
            "email": self.email,
            "emailReceipt": self.emailReceipt,
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachLevelTwoData(self, ltd):
        ''' attach a LevelTwoData object to the current object. ltd is the LevelThreeData object'''
        self.levelTwoData = ltd.serialize()

    def attachLevelThreeData(self, ltd):
        ''' attach a LevelThreeData object to the current object. ltd is the LevelThreeData object'''
        self.levelThreeData = ltd.serialize()
