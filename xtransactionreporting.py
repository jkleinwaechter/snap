#!/usr/bin/python
''' These are the transactions illustrated in Transaction Reporting
    Reference:
    https://apidocs.securenet.com/docs/transactions.html?lang=JSON#content

    The main operations are:
        doSearchTransactions
        doGetTransaction
        doUpdateTransaction
'''

import datetime
import logging
from pprint import pformat

from wptotal import wpTransact
from wpauthobjects import LevelTwoData
from wptransactionreportingobjects import SearchTransactionsRequest, UpdateTransactionRequest
from wpresponseobjects import TransactionReportingResponseParameters
from wpexceptions import WpBadResponseError


log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


def doSearchTransactions():
    '''Search a transaction based on supplied criteria
        Input:
            none
        Output:
            none
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    st = SearchTransactionsRequest()
    st.startDate = "9/8/2016"
    st.endDate = "9/9/2016"

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("SearchTransactions", st.serialize())
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    rp = TransactionReportingResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):  # response from Worldpay indicates failure
        errMsg = "SearchTransactions failed. Result: , " + rp.result + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    # return the transaction id and amount
    msg = "Search tansactions successful."
    print msg
    log.info(msg)

    for record in rp.transactions:
        msg = "  (" + record.creditCardType + " " + record.cardNumber + "  $" + str(record.transactionData.amount)
        print msg
    return


def doGetTransaction(tid):
    '''Get a transaction based on transaction id
        Input:
            tid - transaction id
        Output:
            none
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object - none required for this operation
    # 2. Send the transaction
    try:
        response = wpTransact("GetTransaction", "", tid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = TransactionReportingResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):  # response from Worldpay indicates failure
        errMsg = "GetTransaction failed. Result: , " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    cardNumber = rp.transactions[0].cardNumber
    cardType = rp.transactions[0].creditCardType
    amount = str(rp.transactions[0].transactionData.amount)
    msg = "Get Transaction successful. (" + cardType + " " + cardNumber + "  $" + amount + ")"
    print msg
    log.info(msg)

    return


def doUpdateTransaction(tid):
    '''Update details on a previous transaction
        Input:
            tid - transaction id
        Output:
            none
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    # For this exercise we'll attach some level 2 data to the transaction
    '''
    l2 = LevelTwoData()
    now = datetime.datetime.now()
    l2.orderDate = now.strftime('%d/%b/%y')
    l2.purchaseOrder = "PO325425"
    l2.dutyAmount = 1.15
    l2.freightAmount = 2.30
    l2.retailLaneNumber = 69
    l2.taxAmount = 0.05
    l2.status = "EXEMPT"
    '''

    ut = UpdateTransactionRequest()
    ut.referenceTransactionId = tid
    ut.email = "iamnothim@comcast.net"
    ut.emailReceipt = True
    '''ut.attachLevelTwoData(l2)'''

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("UpdateTransaction", ut.serialize(), tid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = TransactionReportingResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):  # response from Worldpay indicates failure
        errMsg = "UpdateTransaction failed. Result: , " + rp.result + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    # return the transaction id and amount
    msg = "Update transaction successful. TransactionId = " + str(rp.transaction.transactionId) + " IP Address: " + str(rp.ipAddress)
    print msg
    log.info(msg)

    return
