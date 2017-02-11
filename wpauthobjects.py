#!/usr/bin/python
'''These are the request objects used to make card present/not present calls.
    Reference
        https://www.worldpay.com/us/developers/apidocs/creditcardpresent.htm
        https://www.worldpay.com/us/developers/apidocs/creditcardnotpresent.html
        https://www.worldpay.com/us/developers/apidocs/ach.html

    Main Classes
        AuthorizationRequest - used for both auth and capture calls
        PriorAuthCaptureRequest - used for prior auth capture only call
'''

import logging

from wptotal import worldpay

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry

''' The following classes are all objects that can be attached to the main request objects
    (located at the end of this file). For these classes you need to create an instance of
    the object, fill it in and then perform an attachXXx method in the main request object.
'''


class Encryption(object):
    '''This is the encryption referenced in the main Authorizatoin Request Object'''
    def __init(self):
        log.debug("Encryption class:")
        self.encryptionMode = 0

    def serialize(self):
        s = {
            "encryptionMode": self.encryptionMode
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d


class AdditionalTerminalInfo(object):
    '''This is the Additional Terminal Info referenced in the main Authorizatoin Request Object'''
    def __init__(self):
        log.debug("AdditionalTerminalInfo class:")
        self.terminalId = ""
        self.terminalCity = ""
        self.terminalState = ""
        self.terminalLocation = ""
        self.storeNumber = ""

    def serialize(self):
        s = {
            "terminalId": self.terminalId,
            "terminalCity": self.terminalCity,
            "terminalState": self.terminalState,
            "terminalLocation": self.terminalLocation,
            "storeNumber": self.storeNumber
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d


class Address(object):
    '''This is the Address object referenced in many other Request Objects'''
    def __init__(self):
        log.debug("Address class:")
        self.line1 = ""
        self.city = ""
        self.state = ""
        self.zip = ""
        self.country = ""
        self.company = ""
        self.phone = ""

    def serialize(self):
        s = {
            "line1": self.line1,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "country": self.country,
            "company": self.company,
            "phone": self.phone
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value

        return d


class Card(object):
    '''This is the Card object referenced in many other Request Objects'''
    def __init__(self):
        log.debug("Card class:")
        self.trackData = ""
        self.number = ""
        self.cvv = ""
        self.expirationDate = ""
        self.ksn = ""
        self.pinblock = ""
        self.firstName = ""
        self.lastName = ""
        self.signature = ""
        self.email = ""
        self.emailReceipt = False  # Boolean
        self.address = {}  # serialized Address class

    def serialize(self):
        s = {
            "trackData": self.trackData,
            "number": self.number,
            "cvv": self.cvv,
            "expirationDate": self.expirationDate,
            "ksn": self.ksn,
            "pinblock": self.pinblock,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "signature": self.signature,
            "email": self.email,
            "emailReceipt": self.emailReceipt,
            "address": self.address
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachAddress(self, addr):
        self.address = addr.serialize()


class Check(object):
    '''This is the Check referenced in many other Request Objects'''
    def __init__(self):
        log.debug("Check class:")
        self.accountType = ""
        self.checkType = ""
        self.routingNumber = ""
        self.accountNumber = ""
        self.checkNumber = ""
        self.firstName = ""
        self.lastName = ""
        self.email = ""
        self.front = ""
        self.back = ""
        self.verification = ""
        self.address = {}

    def serialize(self):
        s = {
            "accountType": self.acountType,
            "checkType": self.checkType,
            "routingNumber": self.routingNumber,
            "accountNumber": self.accountNumber,
            "checkNumber": self.checkNumber,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "front": self.front,
            "back": self.back,
            "verification": self.verification,
            "address": self.address
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value

        return d

    def attachAddress(self, addr):
        self.address = addr.serialize()


class PaymentVaultToken(object):
    '''This is the Payment Vault Token object referenced in the main Authorization Request Object'''
    def __init__(self):
        log.debug("PaymentVaultToken class:")
        self.customerID = ""
        self.paymentMethodId = ""
        self.publicKey = ""
        self.paymentType = ""

    def serialize(self):
        self.publicKey = worldpay.publicKey
        s = {
            "customerID": self.customerID,
            "paymentMethodId": self.paymentMethodId,
            "publicKey": self.publicKey,
            "paymentType": self.paymentType
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value

        return d


class LevelTwoData(object):
    '''This is the Level Two object referenced in the main Authorization Request Object'''
    def __init__(self):
        log.debug("LevelTwoData class:")
        self.orderDate = 0  # DateTime fromat
        self.purchaseOrder = ""
        self.dutyAmount = 0.0
        self.freightAmount = 0.0
        self.retailLaneNumber = 0
        self.taxAmount = 0.0
        self.status = ""  # enum NOT_INCLUDED, INCLUDED, EXEMPT

    def serialize(self):
        s = {
            "orderDate": self.orderDate,
            "purchaseOrder": self.purchaseOrder,
            "dutyAmount": self.dutyAmount,
            "freightAmount": self.freightAmount,
            "retailLaneNumber": self.retailLaneNumber,
            "taxAmount": self.taxAmount,
            "status": self.status
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value

        return d


class LevelThreeData(object):
    '''This is the Level Three object referenced in the main Authorization Request Object'''
    def __init__(self):
        log.debug("LevelThreeData class:")
        self.orderDate = 0  # DateTime format
        self.discountAmount = 0.0
        self.planId = 0
        self.startDate = 0  # DateTime format
        self.nextPaymentDate = 0  # DateTime format
        self.maxRetries = 0
        self.primaryPaymentMethodId = ""
        self.secondaryPaymentMethodId = ""
        self.vatData = {}  # serialized VatData Class
        self.destinationAddress = {}  # serialized Address class
        self.originaAddress = {}  # serialized Address class
        self.products = []  # serialized Products class
        self.userDefinedFields = []

    def serialize(self):
        s = {
            "orderDate": self.orderDate,
            "discountAmount": self.discountAmount,
            "planId": self.planId,
            "startDate": self.planId,
            "nextPaymentDate": self.nextPaymentDate,
            "maxRetries": self.maxRetries,
            "primaryPaymentMethodId": self.primaryPaymentMethodId,
            "asecondaryPaymentMethodId": self.secondaryPaymentMethodId,
            "vatData": self.vatData,
            "destinationAddress": self.destinationAddress,
            "originalAddress": self.originalAddress,
            "products": self.products,
            "userDefinedFields": self.userDefinedFields
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value

        return d

    def attachVatData(self, vd):
        ''' attach a VatData object to the current object. vd is the VatData object'''
        self.vatData = vd.serialize()

    def attachDestinationAddress(self, a):
        ''' attach an Address object to the destinationAddress. a is the Address object'''
        self.destinationAddress = a.serialize()

    def attachOriginalAddress(self, a):
        ''' attach an Address object to the originalAddress. a is the Address object'''
        self.originalAddress = a.serialize()

    def attachProduct(self, pr):
        ''' attach a Product object to the current object. pr is the Proudct object'''
        self.products.append(pr.serialize())

    def attachUserDefinedField(self, udf):
        ''' add another UserDefinedField to the array. There is a limit of 50 UDFs'''
        self.userDefinedFields.append(udf.serialize())


class VatData(object):
    '''This is the Value Add Tax object referenced in the main Authorization Request Object'''
    def __init__(self):
        log.debug("ValData class:")
        self.purchaserVatNumber = ""
        self.merchantVatNumber = ""
        self.taxRate = 0.0

    def serialize(self):
        s = {
            "purchaserVatNumber": self.purchaserVatNumber,
            "merchantVatNumber": self.merchantVatNumber,
            "taxRate": self.taxRate
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d


class Product(object):
    '''This is the Product object referenced in the main Authorization Request Object'''
    def __init__(self):
        log.debug("Product class:")
        self.alternateTaxId = ""
        self.commodityCode = ""
        self.discountAmount = ""
        self.discountRate = 0.0
        self.discountIndicator = ""
        self.grossNetIndicator = ""
        self.itemCode = ""
        self.itemName = ""
        self.itemDescription = ""
        self.unit = ""
        self.unitPrice = 0.0
        self.quantity = 0.0
        self.totalAmount = 0.0
        self.taxAmount = 0.0
        self.taxRate = 0.0
        self.taxTypeIdentifier = ""
        self.taxTypeApplied = ""
        self.taxable = False

    def serialize(self):
        s = {
            "alternateTaxId": self.alternateTaxId,
            "commodityCode": self.commodityCode,
            "discountAmount": self.discountAmount,
            "discountRate": self.discountRate,
            "discountIndicator": self.discountIndicator,
            "grossNetIndicator": self.grossNetIndicator,
            "itemCode": self.itemCode,
            "itemName": self.itemName,
            "itemDescription": self.itemDescription,
            "unit": self.unit,
            "unitPrice": self.unitPrice,
            "quantity": self.quantity,
            "totalAmount": self.totalAmount,
            "taxAmount": self.taxAmount,
            "taxRate": self.taxRate,
            "taxTypeIdentifier": self.taxTypeIdentifier,
            "taxTypeApplied": self.taxTypeApplied,
            "taxable": self.taxable
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d


class MailOrTelephoneData(object):
    '''This is the MOTO object referenced in the main Authorization Request Object'''
    def __init__(self):
        log.debug("MailOrTelephoneData class:")
        self.type = ""  # enum SINGLE_PURCHASE, RECURRING, INSTALLMENT
        self.totalNumberofInstallments = ""  # required if type is INSTALLMENT
        self.currentInstallment = ""  # Required if type is INSTALLMENT

    def serialize(self):
        s = {
            "type": self.type,
            "totalNumberofInstallments": self.totalNumberofInstallments,
            "currentInstallment": self.currentInstallment
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d


class ServiceData(object):
    '''This is the Tip object referenced in the main Authorization Request Object'''
    def __init__(self):
        log.debug("ServiceData class:")
        self.gratuityAmount = 0.0
        self.server = ""

    def serialize(self):
        s = {
            "gratuityAmount": self.gratuityAmount,
            "server": self.server
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d


class ExtendedInformation(object):
    '''This is the Extended Information object referenced in the main Authorization Request Object'''
    def __init__(self):
        log.debug("ExtendedInformation class:")
        self.typeOfGoods = ""
        self.deviceCode = ""
        self.entrySource = ""
        self.notes = ""
        self.invoiceNumber = ""
        self.invoiceDescriptor = ""
        self.additionalTerminalInfo = {}  # serialized AdditionalTerminalInformation class
        self.levelTwoData = {}  # serialized LevelTwoData class
        self.levelThreeData = {}  # serialized LevelThreeData class
        self.mailOrTelephoneData = {}  # serialized mailOrTelephoneData class
        self.serviceData = {}  # serialized serviceData class
        self.userDefinedFields = []  # Not sure if this should use a class or be hand crafted. Research

    def serialize(self):
        s = {
            "typeOfGoods": self.typeOfGoods,
            "deviceCode": self.deviceCode,
            "entrySource": self.entrySource,
            "notes": self.notes,
            "invoiceNumber": self.invoiceNumber,
            "invoiceDescriptor": self.invoiceDescriptor,
            "additionalTerminalInfo": self.additionalTerminalInfo,
            "levelTwoData": self.levelTwoData,
            "levelThreeData": self.levelThreeData,
            "mailOrTelephoneData": self.mailOrTelephoneData,
            "serviceData": self.serviceData,
            "userDefinedFields": self.userDefinedFields
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachAdditionalTerminalInfo(self, ati):
        ''' attach an AdditionalTerminalInfo to the current object. ati is the AdditionalTerminalInfo object'''
        log.debug("before")
        self.additionalTerminalInfo = ati.serialize()

    def attachLevelTwoData(self, ltd):
        ''' attach a LevelTwoData object to the current object. ltd is the LevelThreeData object'''
        self.levelTwoData = ltd.serialize()

    def attachLevelThreeData(self, ltd):
        ''' attach a LevelThreeData object to the current object. ltd is the LevelThreeData object'''
        self.levelThreeData = ltd.serialize()

    def attachMailOrTelephoneData(self, moto):
        ''' attach a MailOrTelephoneData object to the current object. moto is the MailOrTelephoneData object'''
        self.mailOrTelephoneDataData = moto.serialize()

    def attachServiceData(self, sd):
        ''' attach a ServiceData object to the current object. sd the ServiceData object'''
        self.serviceData = sd.serialize()

    def attachUserDefinedField(self, udf):
        ''' add another UserDefinedField to the array. There is a limit of 50 UDFs'''
        self.userDefinedFields.append(udf.serialize())


class UserDefinedField(object):
    ''' This class is used to define a user defined field pair'''

    def __init__(self):
        log.debug("UserDefinedFields class:")
        # Required
        self.udfName = ""  # Can be 'udf1' - 'udf50'
        self.value = ""

    def serialize(self):
        s = {
            "udfName": self.udfName,
            "value": self.value
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d


'''
    The following classes are the main Request Objects.
'''


class AuthorizationRequest(object):
    '''This is the main class to be used when performing either an Auth or Charge request'''

    def __init__(self):
        log.debug("AuthorizationRequest class:")
        # Required
        self.amount = 0.0
        self.card = {}  # serialized Card class
        self.check = {}  # serialized Check class
        self.extendedInformation = {}  # serialized ExtendedInformation class
        self.developerApplication = {}  # supplied by serialize. No need to fill this in
        self.encryption = {}  # required if doing a manual E2EE encryption
        # Conditional
        self.paymentVaultToken = {}  # serialized PaymentVaultToken class
        # Optional
        self.addToVault = False
        self.addToVaultOnFailure = False
        self.cashBackAmount = 0.0
        self.allowPartialChanges = False
        self.transactionDuplicateCheckIndicator = 0
        self.orderId = ""
        self.transactionId = 0

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "amount": self.amount,
            "addToVault": self.addToVault,
            "addToVaultOnFailure": self.addToVaultOnFailure,
            "cashBackAmount": self.cashBackAmount,
            "allowPartialChanges": self.allowPartialChanges,
            "transactionDuplicateCheckIndicator": self.transactionDuplicateCheckIndicator,
            "orderId": self.orderId,
            "transactionId": self.transactionId,
            "card": self.card,
            "check": self.check,
            'extendedInformation': self.extendedInformation,
            "developerApplication": self.developerApplication,
            "encryption": self.encryption,
            "paymentVaultToken": self.paymentVaultToken
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachCard(self, c):
        ''' attach a Card object to the this object. C is the Card object'''
        self.card = c.serialize()

    def attachCheck(self, c):
        ''' attach a Check object to the this object. C is the Card object'''
        self.check = c.serialize()

    def attachExtendedInformation(self, ei):
        ''' attach an ExtendedInformation object to the this object. ei is the ExtendedInformation object'''
        log.debug("ei.serialize")
        self.extendedInformation = ei.serialize()

    def attachEncryption(self, enc):
        ''' attach an Encryption object to this object. enc is the Encryption object'''
        self.encryption = enc.serialize()

    def attachPaymentVaultToken(self, pvt):
        ''' attach a PaymentVaultToken to the current object. pvt is the PaymentVaultToken object.'''
        self.paymentVaultToken = pvt.serialize()


class PriorAuthCaptureRequest(object):
    '''This is the main class to be used when performing a Capture request.
        Note that a prior Auth must have been performed to get the transactionId'''

    def __init__(self):
        log.debug("PriorAuthCaptureRequest class:")
        # Required
        self.developerApplication = {}
        self.transactionId = 0
        self.amount = 0.0
        self.extendedInformation = {}

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added

        s = {
            "transactionId": self.transactionId,
            "developerApplication": self.developerApplication,
            "amount": self.amount,
            "extendedInformation": self.extendedInformation
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachExtendedInformation(self, ei):
        ''' attach an Extended Information object to the current object. ei is the Extended Information object'''
        self.extendedInformation = ei.serialize()
