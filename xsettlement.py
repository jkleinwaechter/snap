#!/usr/bin/python
''' These are the transactions illustrated in Settlement
    Reference:
        https://www.worldpay.com/us/developers/apidocs/settlement.html

    The main operations are:
        doGetBatch
        doGetBatchById
        doCloseBatch
'''

import logging
from pprint import pformat

from wpsettlementobjects import BatchRequest
from wpresponseobjects import BatchResponseParameters
from wpexceptions import WpBadResponseError
from wptotal import wpTransact

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


def doGetBatch():
    '''Retrieve the transactions in the current batch
        Input:
            none
        Output:
            transaction code result
        Raises:
            Exceptions raised by wpTransact()
    '''
    return batchOperation(retrieve=True)


def doGetBatchById(batchId):
    '''Retrieve the transactions from a previously closed batch
        Input:
            batchId - id of the batch to retrieve
        Output:
            transaction code result
        Raises:
            Exceptions raised by wpTransact()
    '''
    return batchOperation(retrieve=True, bId=batchId)


def doCloseBatch():
    '''Close the current batch
        Input:
            tId - transaction to be voided
        Output:
            transaction code result
        Raises:
            Exceptions raised by wpTransact()
    '''
    return batchOperation()  # no parameters keys batchOperation to do a close current


def batchOperation(retrieve=False, bId=0):
    '''
    This function is the common logic for the three batch calls. No need to call this function directly
    Input: retrieve = True if this is a get operation
        bId = 0 if retrieveing current batch, otherwise it is the batch id
    Output:
        batchId = batchid returned
    Raises:
        WpBadResponse
        others raised from transact())
    '''
    # 1. Fill in the Request Object
    cb = BatchRequest()
    log.debug("batchOperation retrieve: %s, bid: %s Request: %s", retrieve, str(bId), pformat(cb.serialize(), indent=1))

    # Do the approporate transaction based on arguments
    if retrieve is False:  # close the currently open batch
        op = "CloseBatch"
    else:
        if bId:  # Retrieve a Closed Batch using its batch id
            op = "GetBatchById"
        else:  # get the currently open batch
            op = "GetBatch"

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact(op, cb.serialize(), bId)
    except:
        raise  # pass upward

    # 3. Deserialize the result into a Response Object
    rp = BatchResponseParameters(response)

    if (rp.responseCode != 1):
        errMsg = op + " failed. Batch id: " + str(rp.batchId) + "Result:  +  " + rp.result + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    # Print out transactions in the batch specified
    msg = op + " transactions: {"
    for i in rp.transactions:
        msg += str(i.transactionId) + "  "
    msg += "}"
    print msg
    log.info(msg)

    msg = op + " transaction successful. BatchId: " + rp.batchId
    print msg
    log.info(msg)

    return rp.batchId
