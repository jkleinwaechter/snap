#!/usr/bin/python

'''These are the request objects used to make calls to the Vault
    Reference
        https://www.worldpay.com/us/developers/apidocs/vault.html

    Main Classes
        CustomerRequest - used for create, get, and update customer
        PaymentAccountRequest - used for create, get, update and delete payment account
        CustomerAndPaymentRequest - used for create and update customer and payment account

'''
import logging

from wptotal import worldpay

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


class CustomerRequest(object):
    '''This is the class used for create, get and update customer '''

    def __init__(self):
        log.debug("CustomerRequest class:")
        # Required
        self.developerApplication = {}  # supplied by serialize. No need to fill this in
        self.firstName = ""  # optional in Update
        self.lastName = ""  # optional in Update
        # Optional
        self.customerId = ""  # mandatory in Update. Fill this in for Create if you want to manage your own customer ids.
        self.phoneNumber = ""
        self.emailAddress = ""
        self.sendEmailReceipts = ""
        self.company = ""
        self.notes = ""
        self.customerDuplicateCheckIndicator = 0
        self.address = {}  # serialized address class
        self.userDefinedFields = []  # this is an array of UserDefinedField objects

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            'developerApplication': self.developerApplication,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'customerId': self.customerId,
            'phoneNumber': self.phoneNumber,
            'emailAddress': self.emailAddress,
            'sendEmailReceipts': self.sendEmailReceipts,
            'company': self.company,
            'notes': self.notes,
            'customerDuplicateCheckIndicator': self.customerDuplicateCheckIndicator,
            'address': self.address,
            'userDefinedFields': self.userDefinedFields
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachUserDefinedField(self, udf):
        ''' add another UserDefinedField to the array. There is a limit of 50 UDFs'''
        self.userDefinedFields.append(udf.serialize())

    def attachAddress(self, addr):
        ''' add the serialized address to this object'''
        self.address = addr.serialize()


class PaymentAccountRequest(object):
    '''This is the class used for create, get, update and delete payment account '''

    def __init__(self):
        log.debug("PaymentAccountRequest class:")
        # Required
        self.developerApplication = {}  # supplied by serialize. No need to fill this in
        self.customerId = ""  # mandatory in Update. Fill this in for Create if you want to manage your own customer ids.
        # Optional
        self.paymentMethodId = ""
        self.notes = ""
        self.phone = ""
        self.primary = ""
        self.accountDuplicateCheckIndicator = 1
        # Conditional
        self.card = {}  # serialized Card class
        self.check = {}  # serialized Check Class
        self.userDefinedFields = []  # this is an array of UserDefinedField objects

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            'developerApplication': self.developerApplication,
            'customerId': self.customerId,
            'paymentMethodId': self.paymentMethodId,
            'notes': self.notes,
            'phone': self.phone,
            'primary': self.primary,
            'accountDuplicateCheckIndicator': self.accountDuplicateCheckIndicator,
            'card': self.card,
            'check': self.check,
            'userDefinedFields': self.userDefinedFields
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an emoty value
        return d

    def attachCard(self, c):
        ''' attach a Card object to the this object. C is the Card object'''
        self.card = c.serialize()

    def attachCheck(self, c):
        ''' attach a Check object to the this object. C is the Card object'''
        self.check = c.serialize()

    def attachUserDefinedField(self, udf):
        ''' add another UserDefinedField to the array. There is a limit of 50 UDFs'''
        self.userDefinedFields.append(udf.serialize())


class CustomerAndPaymentRequest(object):
    def __init__(self):
        log.debug("CreateCustomerAndPaymentRequest class:")
        # Required
        self.developerApplication = {}  # supplied by serialize. No need to fill this in
        self.firstName = ""  # optional in Update
        self.lastName = ""  # optional in Update
        # Optional
        self.customerId = ""  # mandatory in Update. Fill this in for Create if you want to manage your own customer ids.
        self.phoneNumber = ""
        self.paymentMethodId = ""
        self.emailAddress = ""
        self.primary = ""
        self.sendEmailReceipts = ""
        self.company = ""
        self.notes = ""
        self.customerDuplicateCheckIndicator = 1
        self.accountDuplicateCheckIndicator = 1
        self.card = {}
        self.check = {}
        self.address = {}  # serialized address class
        self.userDefinedFields = []  # this is an array of UserDefinedField objects

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            'developerApplication': self.developerApplication,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'customerId': self.customerId,
            'phoneNumber': self.phoneNumber,
            'paymentMethodId': self.paymentMethodId,
            'emailAddress': self.emailAddress,
            'primary': self.primary,
            'sendEmailReceipts': self.sendEmailReceipts,
            'company': self.company,
            'notes': self.notes,
            'customerDuplicateCheckIndicator': self.customerDuplicateCheckIndicator,
            'accountDuplicateCheckIndicator': self.accountDuplicateCheckIndicator,
            'card': self.card,
            'check': self.check,
            'address': self.address,
            'userDefinedFields': self.userDefinedFields
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachCard(self, c):
        ''' attach a Card object to this object. C is the Card object'''
        self.card = c.serialize()

    def attachCheck(self, c):
        ''' attach a Check object to this object. C is the Check object'''
        self.check = c.serialize()

    def attachUserDefinedField(self, udf):
        ''' add another UserDefinedField to the array. There is a limit of 50 UDFs'''
        self.userDefinedFields.append(udf.serialize())

    def attachAddress(self, addr):
        ''' attach an Address object to thius object. Addr is the address object'''
        self.address = addr.serialize()
