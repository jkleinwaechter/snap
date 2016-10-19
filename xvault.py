#!/usr/bin/python
''' These are the transactions illustrated in SecureNet Vault
    Reference:
        https://www.worldpay.com/us/developers/apidocs/vault.html

    The main operations are:
        doCreateCustomer
        doUpdateCustomer
        doGetCustomer
        doCreatePaymentAccount
        doGetPaymentAccount
        doUpdatePaymentAccount
        doDeletePaymentAccount
        doCreateCustomerAndPayment
        doUpdateCustomerAndPayment

'''

import logging
from pprint import pformat
from datetime import datetime

from wpauthobjects import Card, Address, UserDefinedField
from wpvaultobjects import CustomerRequest, PaymentAccountRequest, CustomerAndPaymentRequest
from wpresponseobjects import CustomerResponseParameters, PaymentAccountResponseParameters, CustomerAndPaymentResponseParameters
from wpexceptions import WpBadResponseError
from wptotal import wpTransact
from wptestcard import test

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


def doCreateCustomer():
    '''Perform Create Customer in the vault
        Input:
            nothing
        Output:
            CustomerId
        Raises:
            Exceptions raised by wpTransact()
    '''
    test.random()  # get a random test data set

    # 1. Fill in the Request Object
    address = Address()
    address.line1 = test.getAddress()
    address.city = test.getCity()
    address.state = test.getState()
    address.zip = test.getZip()
    address.country = test.getCountry()
    address.company = test.getCompany()
    address.phone = test.getPhone()

    udf1 = UserDefinedField()
    udf2 = UserDefinedField()
    n = datetime.now()
    udf1.udfName = 'udf1'
    udf1.value = n.strftime('%d-%b-%y')
    udf2.udfName = 'udf2'
    udf2.value = n.strftime('%I:%M %p')

    cr = CustomerRequest()
    cr.firstName = test.getFirstName()
    cr.lastName = test.getLastName()
    cr.phoneNumber = test.getPhone()
    cr.emailAddress = test.getEmail()
    cr.company = test.getCompany()
    cr.notes = "Joe Kleinwaechter entered this from his python app. Need to delete it."
    cr.attachAddress(address)
    cr.attachUserDefinedField(udf1)
    cr.attachUserDefinedField(udf2)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("CreateCustomer", cr.serialize())
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = CustomerResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doCreateCustomer failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Create Customer transaction successful. CustomerId: " + str(rp.customerId)
    print msg
    log.info(msg)

    return rp.customerId


def doUpdateCustomer(cid):
    '''Perform Create Customer in the vault
        Input:
            cid - customer id
        Output:
            nothing
        Raises:
            Exceptions raised by wpTransact()
    '''
    # Note that for test purposes, this is just going to read back in the current test record and fill it in under the assumption that the cid passed was the last one created

    test.reread()  # get the current test data set

    # 1. Fill in the Request Object
    address = Address()
    address.line1 = test.getAddress()
    address.city = test.getCity()
    address.state = test.getState()
    address.zip = test.getZip()
    address.country = test.getCountry()
    address.company = test.getCompany()
    address.phone = test.getPhone()

    udf1 = UserDefinedField()
    udf2 = UserDefinedField()
    n = datetime.now()
    udf1.udfName = 'udf1'
    udf1.value = n.strftime('%d-%b-%y')
    udf2.udfName = 'udf2'
    udf2.value = n.strftime('%I:%M %p')

    cr = CustomerRequest()
    cr.firstName = test.getFirstName()
    cr.lastName = test.getLastName()
    cr.phoneNumber = test.getPhone()
    cr.emailAddress = test.getEmail()
    cr.company = test.getCompany()
    cr.attachAddress(address)
    cr.attachUserDefinedField(udf1)
    cr.attachUserDefinedField(udf2)

    n = datetime.now()
    cr.notes = "This record updated on " + n.strftime('%d-%b-%y  @%I:%M %p')

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("UpdateCustomer", cr.serialize(), cid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = CustomerResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doUpdateCustomer failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Update Customer transaction successful. CustomerId: " + str(rp.customerId)
    print msg
    log.info(msg)

    return


def doGetCustomer(cid):
    '''Perform Retrieve Customer in the vault
        Input:
            cid - customer id
        Output:
            nothing
        Raises:
            Exceptions raised by wpTransact()
    '''
    # 1. Fill in the Request Object - there transaction doesn't require a Request Object
    # 2. Send the transaction
    try:
        response = wpTransact("GetCustomer", "", cid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = CustomerResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doGetCustomer failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Get Customer transaction successful. CustomerId: " + str(rp.customerId) + " Name: " + rp.vaultCustomer.firstName + " " + rp.vaultCustomer.lastName
    print msg
    log.info(msg)

    return


def doCreatePaymentAccount(cid):
    '''Create a payment instrument and attach to a vault customer
        Input:
            cid - customer id
        Output:
            pid - payment id
        Raises:
            Exceptions raised by wpTransact()
    '''
    test.random()  # get a random test data set

    # 1. Fill in the Request Object
    card = Card()
    card.number = test.getCardPAN()
    card.cvv = test.getCVV()
    card.expirationDate = test.getExpirationDate()

    va = PaymentAccountRequest()
    va.customerId = cid
    va.primary = True
    va.attachCard(card)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("CreatePaymentAccount", va.serialize(), cid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = PaymentAccountResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doCreatePaymentAccount failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Create Payment Account transaction successful. CustomerId: " + str(rp.vaultPaymentMethod.customerId) + " PaymentId: " + str(rp.vaultPaymentMethod.paymentId)
    print msg
    log.info(msg)

    return rp.vaultPaymentMethod.paymentId


def doGetPaymentAccount(cid, pid):
    '''Perform Retrieve Payment Account from the vault
        Input:
            cid - customer id
            pid - payment id
        Output:
            nothing
        Raises:
            Exceptions raised by wpTransact()
    '''
    # 1. Fill in the Request Object - this transaction doesn't require a Request Object
    # 2. Send the transaction
    try:
        response = wpTransact("GetPaymentAccount", "", cid, pid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = PaymentAccountResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doGetPaymentAccount failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Get Payment Account transaction successful. CustomerId: " + str(rp.vaultPaymentMethod.customerId) + " Card: " + rp.vaultPaymentMethod.card.maskedNumber
    print msg
    log.info(msg)

    return


def doUpdatePaymentAccount(cid, pid):
    '''Create a payment instrument and attach to a vault customer
        Input:
            cid - customer id
            pid - payment method id
        Output:
            nothing
        Raises:
            Exceptions raised by wpTransact()
    '''
    test.reread()  # reread the last record as I am assuming we are simply modifying the last account created

    # 1. Fill in the Request Object
    card = Card()
    card.number = test.getCardPAN()
    card.cvv = '999'  # this is the field we will modify for this test case
    card.expirationDate = test.getExpirationDate()

    va = PaymentAccountRequest()
    va.customerId = cid
    va.primary = True
    va.paymnetMethodId = pid
    va.attachCard(card)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("UpdatePaymentAccount", va.serialize(), cid, pid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = PaymentAccountResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doUpdatePaymentAccount failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Update Payment Account transaction successful. CustomerId: " + str(rp.vaultPaymentMethod.customerId) + " PaymentId: " + str(rp.vaultPaymentMethod.paymentId)
    print msg
    log.info(msg)

    return


def doDeletePaymentAccount(cid, pid):
    '''Perform Delete Account from the vault
        Input:
            cid - customer id
            pid - payment id
        Output:
            nothing
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    # Doc error??
    # va = PaymentAccountRequest()  # we will resuse this object as we only need a subset
    # va.customerId = cid
    # va.paymentMethodId = pid

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("DeletePaymentAccount", "", cid, pid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = PaymentAccountResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doDeletePaymentAccount failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Delete Payment Account transaction successful. CustomerId: " + cid
    print msg
    log.info(msg)

    return


def doCreateCustomerAndPayment():
    '''Perform Create Customer in the vault
        Input:
            nothing
        Output:
            CustomerId
        Raises:
            Exceptions raised by wpTransact()
    '''
    test.random()  # get a random test data set

    # 1. Fill in the Request Object
    address = Address()
    address.line1 = test.getAddress()
    address.city = test.getCity()
    address.state = test.getState()
    address.zip = test.getZip()
    address.country = test.getCountry()
    address.company = test.getCompany()
    address.phone = test.getPhone()

    card = Card()
    card.number = test.getCardPAN()
    card.cvv = test.getCVV()
    card.expirationDate = test.getExpirationDate()

    cr = CustomerAndPaymentRequest()
    cr.firstName = test.getFirstName()
    cr.lastName = test.getLastName()
    cr.phoneNumber = test.getPhone()
    cr.emailAddress = test.getEmail()
    cr.company = test.getCompany()
    cr.notes = "Joe Kleinwaechter entered this from his python app. Need to delete it."
    cr.primary = True
    cr.attachAddress(address)
    cr.attachCard(card)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("CreateCustomerAndPayment", cr.serialize())
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = CustomerAndPaymentResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doCreateCustomerAndPayment failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Create Customer and Payment transaction successful. CustomerId: " + str(rp.vaultCustomer.customerId) + " PaymentId: " + str(rp.vaultCustomer.primaryPaymentMethodId)
    print msg
    log.info(msg)

    return rp.vaultCustomer.customerId


def doUpdateCustomerAndPayment(cid):
    '''Perform Update Customer in the vault
        Input:
            cid - customer id
        Output:
            CustomerId
        Raises:
            Exceptions raised by wpTransact()
    '''
    test.reread()  # get a random test data set

    # 1. Fill in the Request Object
    address = Address()
    address.line1 = test.getAddress()
    address.city = test.getCity()
    address.state = test.getState()
    address.zip = test.getZip()
    address.country = test.getCountry()
    address.company = test.getCompany()
    address.phone = test.getPhone()

    udf1 = UserDefinedField()
    udf2 = UserDefinedField()
    n = datetime.now()
    udf1.udfName = 'udf1'   # this is the field we will modify for this test case
    udf1.value = n.strftime('%d-%b-%y')
    udf2.udfName = 'udf2'   # this is the field we will modify for this test case
    udf2.value = n.strftime('%I:%M %p')

    card = Card()
    card.number = test.getCardPAN()
    card.cvv = '999'  # this is the field we will modify for this test case
    card.expirationDate = test.getExpirationDate()

    cr = CustomerAndPaymentRequest()
    cr.customerId = cid
    cr.paymentMethodId = 1
    cr.firstName = test.getFirstName()
    cr.lastName = test.getLastName()
    cr.phoneNumber = test.getPhone()
    cr.emailAddress = test.getEmail()
    cr.company = test.getCompany()
    cr.notes = "This record had been modified using unicorn dust."
    cr.primary = True
    cr.attachAddress(address)
    cr.attachCard(card)
    cr.attachUserDefinedField(udf1)
    cr.attachUserDefinedField(udf2)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("UpdateCustomerAndPayment", cr.serialize(), cid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = CustomerAndPaymentResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doUpdateCustomerAndPayment failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Update Customer and Payment transaction successful. CustomerId: " + str(rp.vaultCustomer.customerId) + " PaymentId: " + str(rp.vaultCustomer.primaryPaymentMethodId)
    print msg
    log.info(msg)

    return rp.vaultCustomer.customerId
