#!/usr/bin/python
''' These are the transactions illustrated in Credit Card Present, Credit Card Not Present, & ACH
    Reference:
        https://www.worldpay.com/us/developers/apidocs/creditcardpresent.html
        https://www.worldpay.com/us/developers/apidocs/creditcardnotpresent.html
        https://www.worldpay.com/us/developers/apidocs/ach.html

    The main operations are:
        doAuth
        doCharge
        doVerify
        doPriorAuthCapture
'''
import logging
from pprint import pformat

from wpauthobjects import AuthorizationRequest, PriorAuthCaptureRequest, Card, Address, PaymentVaultToken, ExtendedInformation, ServiceData
from wpresponseobjects import AuthResponseParameters
from wpexceptions import WpBadResponseError, WpInvalidFunctionCallError
from wptotal import wpTransact
from wptestcard import test
# from beeprint import pp  # This is for an improved print debugger. You can pip install beeprint if you want or just remove the pp() statements

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


def doAuth():
    '''Authorize a card only
        Input:
            none
        Output:
            [transaction id, amount]
        Raises:
            Exceptions raised by wpTransact()
    '''

    return baseAuthTransaction(withCapture=False, verifyOnly=False)


def doCharge():
    '''Authorize and capture a card
        Input:
            none
        Output:
            [transaction id, amount]
        Raises:
            Exceptions raised by wpTransact()
    '''
    return baseAuthTransaction(withCapture=True, verifyOnly=False)


def doVerify():
    '''Verify a card - no auth or capture
        Input:
            none
        Output:
            responseCode
        Raises:
            Exceptions raised by wpTransact()
    '''
    return baseAuthTransaction(withCapture=False, verifyOnly=True)


def doPriorAuthCapture(previousTransaction):
    '''Perform a Prior Auth Capture
        Input:
            tid - Requires a transaction id from previous auth
            amt - amount to capture (not to exceed original auth)
        Returns:
            transactionId that was captured
            amount that was authorized
        Raises:
            WpBadResponse
            WpFunctionCallError
            other WP exeptions raised from wpTransact()
    '''
    tid = previousTransaction[0]
    amt = previousTransaction[1]

    if tid == 0:  # invalid transaction id
        raise WpInvalidFunctionCallError("doPriorAuthCapture (" + str(tid) + ")")

    par = PriorAuthCaptureRequest()

    test.random()  # use this just to get a different amount each time
    par.transactionId = tid
    par.amount = amt

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("PriorAuthCapture", par.serialize())
    except:  # pass the exception up
        raise

    # 3. Deserialize the result into a Response Object
    rp = AuthResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doPriorAuthCapture failed. TransactionId: " + str(par.transactionId) + " Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "PriorAuthCapture transaction successful. TransactionId: " + str(rp.transaction.transactionId) + " (" + "$" + amt + ")"
    print msg
    log.info(msg)

    return [rp.transaction.transactionId, rp.transaction.authorizedAmount]


def baseAuthTransaction(withCapture=False, verifyOnly=False):
    '''Perform the transactions that appear like an auth transaction
        Input:
            withCapture - True if doing a Charge, False if just an Auth
            verifyOnly - True if this is only a verify request, False if not
        Output:
            if verify - responseCode
            else [transaction id, amount]
        Raises:
            WpBadResponseError
            Exceptions passed from wpTransact()
    '''

    # 1. Fill in the Request Object
    # Fill in Address object
    address = Address()
    test.random()
    address.line1 = test.getAddress()
    address.city = test.getCity()
    address.state = test.getState()
    address.zip = test.getZip()
    address.country = test.getCountry()
    address.company = test.getCompany()
    address.phone = test.getPhone()

    # Fill in Card object
    card = Card()
    card.number = test.getCardPAN()
    card.cvv = test.getCVV()
    card.expirationDate = test.getExpirationDate()

    # Fill in AuthorizationRequest object
    ar = AuthorizationRequest()
    ar.amount = test.getAmount()

    # Build the full auth request object by attaching supporting objects
    card.attachAddress(address)
    ar.attachCard(card)

    if withCapture:  # we've overloaded this function as most of the code is the same for Charge, Auth, and verify
        operation = "Charge"
    else:
        if verifyOnly:
            operation = "Verify"
        else:
            operation = "Authorize"

    # 2. Send the transaction on a serialized Request Object
    log.debug("Sending transaction\n")
    try:
        response = wpTransact(operation, ar.serialize())
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = AuthResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):  # response from Worldpay indicates failure
        errMsg = operation + " failed. Result: , " + rp.result + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    if verifyOnly:
        msg = operation + " transaction successful. (" + test.getFirstName() + " " + test.getLastName() + " $" + str(test.getAmount()) + ")"
        print msg
        log.info(msg)
        return rp.responseCode
    else:
        # return the transaction id and amount
        transactionId = rp.transaction.transactionId
        msg = operation + " transaction successful. TransactionId:" + str(transactionId) + "(" + test.getFirstName() + " " + test.getLastName() + " $" + str(test.getAmount()) + ")"
        print msg
        log.info(msg)
        return [transactionId, ar.amount]


def doManualAuthTransaction(withCapture=False, verifyOnly=False):
    '''This allows an auth transaction not using the random test database
        Input:
            withCapture - True if doing a Charge, False if just an Auth
            verifyOnly - True if this is only a verify request, False if not
        Output:
            if verify - responseCode
            else [transaction id, amount]
        Raises:
            WpBadResponseError
            Exceptions passed from wpTransact()
    '''

    # 1. Fill in the Request Object
    # Create the objects being utilized
    ar = AuthorizationRequest()
    address = Address()
    card = Card()
    sd = ServiceData()
    ei = ExtendedInformation()

    address.line1 = "201 17th Street"
    address.city = "Atlanta"
    address.state = "GA"
    address.zip = "30000"
    address.country = "USA"
    address.company = "Wordplay"
    address.phone = "678.587.1836"

    card.trackData = "%B4444333322221111^SECURENET^20041015432112345678?;4444333322221111=20041015432112345678?"
    #######################################
    # % - sentinel code
    # B - B type Track 1 data
    # 4444333322221111 - pan
    # ^SECURENET^ - name (23 chars or less) (^ are field seperators)
    # 2004 - expiration date YYMM
    # 101 - service code 1=International capable, 0=Normal Rules 1=no restructions
    # 5432112345678? - Discretionary data
    # ; - Track 2 data
    # 4444333322221111 - PAN
    # = - seperator
    # 2004 - expiration date
    # 101 - service code
    # 5432112345678 - discretionary data
    # ? - sentinal code
    #######################################
    # card.number = "5500000000000004"  # MC
    # card.cvv = "111"
    # card.expirationDate = "03/20"

    sd.gratuityAmount = 1.96
    sd.server = "Joey"

    ar.amount = 10.39

    # Build the object relationships
    log.debug("SD: %s\n", pformat(sd.serialize(), indent=1))
    ei.attachServiceData(sd)
    log.debug("EI: %s\n", pformat(ei.serialize(), indent=1))
    ar.attachExtendedInformation(ei)

    log.debug("Address: %s\n", pformat(address.serialize(), indent=1))
    card.attachAddress(address)  # attach the address object
    log.debug("Card: %s\n", pformat(card.serialize(), indent=1))
    ar.attachCard(card)  # attach the card object

    if withCapture:  # we've overloaded this function as most of the code is the same for Charge, Auth, and verify
        operation = "Charge"
    else:
        if verifyOnly:
            operation = "Verify"
        else:
            operation = "Authorize"

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact(operation, ar.serialize())
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = AuthResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):  # response from Worldpay indicates failure
        errMsg = operation + " failed. Result: , " + rp.result + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    if verifyOnly:
        msg = operation + " transaction successful. (" + test.getFirstName() + " " + test.getLastName() + " $" + str(test.getAmount()) + ")"
        print msg
        log.info(msg)
        return rp.responseCode
    else:
        # return the transaction id and amount
        transactionId = rp.transaction.transactionId
        msg = operation + " transaction successful. TransactionId:" + str(transactionId) + "(" + test.getFirstName() + " " + test.getLastName() + " $" + str(test.getAmount()) + ")"
        print msg
        log.info(msg)
        return [transactionId, ar.amount]


def doChargeWithToken(cid, token=""):
    '''This is a test of the charge with token functionality which seems to be broken
    It is assumed the payment method is 1

        Input:
            cid = customer id
            token = optianl token to use instead of card
        Output:
        Raises:
            WpBadResponseError
            Exceptions passed from wpTransact()
    '''

    pvt = PaymentVaultToken()
    pvt.customerId = cid
    if token == "":
        pvt.paymentMethodId = 1
        pvt.paymentType = "CREDIT_CARD"
    else:
        pvt.paymentMethodId = token

    ar = AuthorizationRequest()
    ar.amount = 10.0
    ar.attachPaymentVaultToken(pvt)  # attach the vault object

    try:
        response = wpTransact("Charge", ar.serialize())
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    rp = AuthResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):  # response from Worldpay indicates failure
        errMsg = "Charge failed. Result: , " + rp.result + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    # return the transaction id and amount
    transactionId = rp.transaction.transactionId
    msg = "Charge transaction successful. TransactionId:" + str(transactionId) + "(" + test.getFirstName() + " " + test.getLastName() + " $" + str(test.getAmount()) + ")"
    print msg
    log.info(msg)
    return [transactionId, ar.amount]
