''' This is the optional interface for importing test data from a csv file.
    The filenmae is set in WPtotal as testDataFileName.
    The field format for the datafile is explicit. The first row must contain the field names. These field names must be labeled as follows and in the following order.
    firstname lastname address city state zip country company phone cvv expirationDate email amount cardPAN
'''

import logging
from random import randint
from csv import DictReader

from wptotal import worldpay

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


class TestDatabase(object):
    ''' Read the test data file
        Objects:
            count - number of record read in from the file
            current - index to the current record in the data array (not needed externally)
        Methods:
            next() - get the next sequential record. If already at the end, start over at the beginning
            previous() - get the previous sequential record. If already at the beginning, return tto the last record.
            random() - Return a random record from the file. This does not advance the index therefore next() and previous() are unaffected
            getXXX() - get methods for each field of the dictionary

    '''
    def __init__(self):
        self.current = 0  # this is the index into the current dictionary record
        self.internalIndex = 0  # this is used esclusively for next() and previous() so that random doesn't reset their index - not for external consumption
        with open(worldpay.testDataFileName, 'rU') as csvfile:
            self.db = list(DictReader(csvfile))
        self.count = len(self.db)

    def next(self):
        if (self.internalIndex >= self.count - 1):  # if we hit the end of the list, start back at the beginning
            self.internalIndex = 0
        else:
            self.internalIndex += 1

        self.current = self.internalIndex  # align the current record to the same as the internal sequential pointer
        d = self.db[self.current]
        log.debug("Next test record (%d): %s", self.current, str(d))
        return d

    def previous(self):
        if (self.internalIndex <= 0):  # if we hit the beginning of the list, loop back to the end
            self.internalIndex = self.count - 1
        else:
            self.internalIndex -= 1

        self.current = self.internalIndex  # align the current record to the same as the internal sequential pointer
        d = self.db[self.current]  # if we were already at the beginning simply return the 1st element rather than fail
        log.debug("Previous test record (%d): %s", self.current, str(d))
        return d

    def reread(self):
        d = self.db[self.current]
        log.debug("Current test record (%d): %s", self.current, str(d))
        return d

    def random(self):
        self.current = randint(0, self.count - 1)
        d = self.db[self.current]
        log.debug("Random test record (%d): %s", self.current, str(d))
        return d

    def getFirstName(self):
        return self.db[self.current].setdefault('firstname', "")

    def getLastName(self):
        return self.db[self.current].setdefault('lastname', "")

    def getAddress(self):
        return self.db[self.current].setdefault('address', "")

    def getCity(self):
        return self.db[self.current].setdefault('city', "")

    def getState(self):
        return self.db[self.current].setdefault('state', "")

    def getZip(self):
        return self.db[self.current].setdefault('zip', "")

    def getCountry(self):
        return self.db[self.current].setdefault('country', "")

    def getCompany(self):
        return self.db[self.current].setdefault('company', "")

    def getPhone(self):
        return self.db[self.current].setdefault('phone', "")

    def getCVV(self):
        return self.db[self.current].setdefault('cvv', "")

    def getExpirationDate(self):
        return self.db[self.current].setdefault('expirationDate', "")

    def getEmail(self):
        return self.db[self.current].setdefault('email', "")

    def getAmount(self):
        return self.db[self.current].setdefault('amount', "")

    def getCardPAN(self):
        return self.db[self.current].setdefault('cardPAN', "")


test = TestDatabase()  # methods and storage for reading in test data
