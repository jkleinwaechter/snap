#!/usr/bin/python
''' These are the transactions illustrated in Credits, Refunds, Voids
    Reference:
        https://www.worldpay.com/us/developers/apidocs/credits.html
        https://www.worldpay.com/us/developers/apidocs/refunds.html
        https://www.worldpay.com/us/developers/apidocs/voids.html

    The main operations are:
        doVoid
        doRefund
        doCredit
'''
import logging
from pprint import pformat

from wpauthobjects import AuthorizationRequest, Card
from wpresponseobjects import AuthResponseParameters
from wptotal import wpTransact
from wptestcard import test

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


def doVoid(tId):
    '''Perform a void on a non-settled transaction.
        Input:
            tId - transaction to be voided
        Output:
            transaction code result
        Raises:
            Exceptions raised by wpTransact()
    '''
    return chargeback(tId, refund=False)


def doRefund(tId):
    '''Perform a void on a non-settled transaction.
        Input:
            tId - transaction to be voided
        Output:
            transaction code result
        Raises:
            Exceptions raised by wpTransact()
    '''
    return chargeback(tId, refund=True)


def doCredit():
    '''Perform a Credit transaction. This is a dangerous transaction
        in that it doesn't require a linked transaction
        Input:
            nothing
        Output:
            transaction code result
        Raises:
            Exceptions raised by wpTransact()
    '''
    test.random()  # get a random test record

    # 1. Fill in the Request Object
    card = Card()
    card.number = test.getCardPAN()
    card.cvv = test.getCVV()
    card.expirationDate = test.getExpirationDate()

    ar = AuthorizationRequest()
    ar.amount = test.getAmount()
    ar.attachCard(card)  # attach the card object

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("Credit", ar.serialize())
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = AuthResponseParameters(response)

    if (rp.responseCode != 1):  # response from Worldpay indicates failure
        errMsg = "Credit transaction failed. Result: " + rp.result + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        print errMsg
        log.info(errMsg)
        return rp.responseCode

    # return the response code

    msg = "Credit transaction successful. TransactionId: ", str(rp.transactionId)
    print msg
    log.info(msg)
    return rp.responseCode


def chargeback(tId, refund=False):
    '''base function used by doRefund and doVoid.
        No need to call directly.
        Input:
            tId - transaction to be voided
            refund - True if refund, False if void
        Output:
            transaction code result
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    ar = AuthorizationRequest()
    ar.transactionId = tId

    if refund:
        op = "Refund"
    else:
        op = "Void"

    log.info("%s: %s", op, pformat(ar.serialize(), indent=1))

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact(op, ar.serialize())
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    log.info("%s Response: %s", op, pformat(response, indent=1))

    # 3. Deserialize the result into a Response Object
    rp = AuthResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):  # response from Worldpay indicates failure
        errMsg = op + " Transaction failed. Result: " + rp.result + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        print errMsg
        log.info(errMsg)
        return rp.responseCode

    msg = op + " Transaction successful. TransactionId:" + str(rp.transaction.transactionId)
    print msg
    log.info(msg)
    return rp.responseCode
