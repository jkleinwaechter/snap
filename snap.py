#!/usr/bin/python

import logging
import sys
import datetime
import os
import shutil
from pprint import pformat
from getopt import getopt
from wpexceptions import WpTimeoutError, WpConnectionError, WpTooManyRedirectsError, WpJSONError, WpBadResponseError, WpHTTPError, WpInvalidEndpointError
from wptotal import worldpay
from xauth import doAuth, doCharge, doPriorAuthCapture, doVerify, doManualAuthTransaction, doChargeWithToken
from xsettlement import doGetBatch, doCloseBatch, doGetBatchById
from xchargebacks import doVoid  # doRefund, doCredit
from xtoken import doCreateToken
from xvault import doCreateCustomer, doUpdateCustomer, doGetCustomer, doCreatePaymentAccount, doGetPaymentAccount, doUpdatePaymentAccount, doDeletePaymentAccount, doCreateCustomerAndPayment, doUpdateCustomerAndPayment
from xrecurring import doGetPaymentPlan, doCreateRecurringPaymentPlan, doCreateInstallmentPaymentPlan, doCreateVariablePaymentPlan, doUpdateRecurringPaymentPlan, doUpdateInstallmentPaymentPlan, doUpdateVariablePaymentPlan
from xtransactionreporting import doSearchTransactions, doGetTransaction, doUpdateTransaction

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry  # this allows the name of the current module to be placed in the log entry


def main(argv):
    ''' This is the main entry point into the Python demo script connecting to Worldpay Total REST Interface'''

    # parse the cmdLine to check if -p (use proxy) flag is set
    try:
        opts, args = getopt(argv, "spl:")
    except getopt.GetoptError as err:  # bad cmdline
        print err
        print 'Usage: sn.py [-p -lDEBUGSTATE -s]'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-p':  # -p will enable the fixed proxy settings
            worldpay.enableProxies()
        if opt == '-s':  # this is a special purpose flag used to isolate certain behaviors. Not for general consumption
            worldpay.doubleSecretProbation = open("doublesecretprobation.txt", 'w')
        if opt == '-l':  # -l will turn on log
            # Turn the string level into a numeric level required by
            level = getattr(logging, arg.upper())
            if not isinstance(level, int):  # Validate its an accepted log level
                print "Invalid log level: ", arg.upper()
            logging.raiseExceptions = True
            logging.basicConfig(filename=worldpay.logFileName, filemode='w', level=level, format='%(asctime)s %(message)s', datefmt='%H:%M:%S')
            log.info("----Log Started----")

    try:
        worldpay.validateConfiguration()  # Make sure our keys and ids are correct
        print '*' * 80
        enactFullScript()
        # enactTestScript()
        # enactInstallmentPaymentScript()
        # enactManualTransaction()
        status = 0  # return good to the shell

    except:  # if we had an exception - copy the log file into err directory and tag it with date and time
        status = 1  # return bad to the shell
        now = datetime.datetime.now()

        # Copy the log file to one with a time stamp
        t = now.strftime('%y%m%d%I%M')  # tag file with current time
        name, extension = worldpay.logFileName.split('.')  # we will use the current log file name as the root of the new file name
        errorFileName = name + "-" + t + "." + extension
        if os.path.isfile(errorFileName):
            errorFileName = errorFileName + " " + now.strftime('%S')  # add seconds

        destination = worldpay.errorLogDirectory + "/" + errorFileName
        if not os.path.isdir(worldpay.errorLogDirectory):  # if the directory doesn't exist, create it
            try:
                # BUG! use os.makedirs insted for windows
                os.mkdirs(worldpay.errorLogDirectory)
            except:
                log.error("Could not create error log directory: %s", worldpay.errorLogDirectory)
                destination = errorFileName  # just rename and leave it in this directory
            else:
                log.info("Created error log directory: %s", worldpay.errorLogDirectory)

        try:
            # BUG! use copy of shutil for windows
            os.rename(worldpay.logFileName, destination)
        except:
            msg = "Could not rename log file to " + destination
            log.error(msg)
        else:
            msg = "Copied log to " + destination
            log.info(msg)

        print(msg)

    if worldpay.doubleSecretProbation is not None:  # For now, if requested, dump return headers to a special file
        worldpay.doubleSecretProbation.close()

    return status


def enactManualTransaction():
    return doSearchTransactions()


def enactFullScript():
    #
    # This is the battery of all transactions
    # Available operations:

    ############################################################################################################
    # STANDALONE:
    #   Verify, Update, SearchTransactions, GetBatch, CloseBatch, CreateToken
    ############################################################################################################
    # UNSETTLED TRANSACTION (tid)
    #   Generates:
    #       Auth
    #   Removes:
    #       PriorAuthCapture, doVoid
    #   Requires:
    #       Void, PriorAuthCapture, GetTransaction, UpdateTransaction
    ############################################################################################################
    # SETTLED TRANSACION (tid)
    #   Generates:
    #       PriorAuthCapture, Charge
    #   Removes:
    #       Refund, Credit
    #   Requires:
    #       Charge, PriorAuthCapture
    ############################################################################################################
    # CUSTOMER: (cid)
    #   Generates:
    #       CreateCustomer, CreateCustomerAndPayment
    #   Requires:
    #       GetCustomer, UpdateCustomer, CreatePaymentAccount, UpdatePaymentAccount, DeletePayementAccount,
    #       UpdateCustomerAndPayment, CreateRecurringPaymentPlan, CreateInstallmentPaymentPlan, CreateVariablePaymentPlan
    ############################################################################################################
    # PAYMENT ACCOUNT (therefore customer account as well) (pid)
    #   Generates:
    #       CreatePayment, CreateCustomerAndPayment
    #   Removes:
    #       DeletePaymentAccount
    #   Requires:
    #       UpdatePaymentAccount, GetPaymentAccount, DeletePaymentAccount,
    ############################################################################################################
    # PAYMENT PLAN (nid)
    #   Generates:
    #       CreateRecurringPaymentPlan, CreateVariablePaymentPlan, CreateInstallmentPaymentPlan
    #   Requires:
    #       GetPaymentPlan, UpdateRecurringPaymentPlan, UpdateVariablePaymentPlan, UpdateInstallmentPaymentPlan
    ############################################################################################################
    authTransactions = []  # These two arrays are used to allow the tests to share transaction ids between themselves
    capturedTransactions = []
    customers = []  # used to stack customer transactions

    try:
        # 2 Auths
        for i in range(2):
            authTransactions.append(doAuth())  # Auth without capture

        # Verify
        doVerify()  # Verify cardholder information

        # Charge
        capturedTransactions.append(doCharge())  # do a charge (auth + capture) and add it to the stack of settlend transactions

        # Capture
        if len(capturedTransactions):
            capturedTransactions.append(doPriorAuthCapture(authTransactions.pop()))  # capture a previous auth only
        else:
            msg = "PriorAuthCapture not performed. No unsettled transactions in the queue"
            log.info(msg)
            print msg

        # Update Transaction
        if len(capturedTransactions):  # This transaction must have had at least one settled transaction available
            t = capturedTransactions[-1]  # pull of the tid/amt tuple
            doUpdateTransaction(t[0])  # Update the most recent settled item
        else:
            msg = "UpdateTransaction not performed. No settled transactions to utilize."
            log.info(msg)
            print msg

        # Get Transaction
        if len(capturedTransactions):  # This transaction must have had at least one settled transaction available
            t = capturedTransactions[-1]  # pull out the tid/amt tuple
            doGetTransaction(capturedTransactions[-1][0])  # Retreive the most recent settled transaction
        else:
            msg = "GetTransaction not performed. No settled transactions to utilize."
            log.info(msg)
            print msg

        # Get Batch
        doGetBatch()  # get the current batch contents fix - not returning anything

        log.info("Authorized Transactions: %s", pformat(capturedTransactions, indent=1))
        log.info("Captured Transactions: %s", pformat(authTransactions, indent=1))

        # Void
        if len(capturedTransactions):
            doVoid(capturedTransactions.pop()[0])  # void one of the captured transactions
        else:
            msg = "Void not performed. No unsettled transactions in the queue."
            log.info(msg)
            print msg

        # Close Batch
        batchId = doCloseBatch()  # close the current batch

        # Get Batch by Id
        try:
            batchId = doGetBatchById(batchId)
        except (WpTimeoutError, WpConnectionError, WpTooManyRedirectsError, WpJSONError, WpBadResponseError, WpJSONError, WpHTTPError) as e:
            print(e.message)
            sys.exit(1)

        # Find all transactions in last 24 hours
        doSearchTransactions()  # Search for some transactions based on criteria set in the called function

        # Create a Token
        doCreateToken("", False)  # create a local token

        # Create a Customer
        customers.append(doCreateCustomer())  # Create a new customer and push the cid on the queue

        # Get a Customer
        if len(customers):
            cid = customers[-1]
            doGetCustomer(cid)  # Get an existing customer record
        else:
            msg = "GetCustomer not performed. No customers in the queue."
            log.info(msg)
            print msg

        # Update customer
        if len(customers):
            doUpdateCustomer(customers[-1])   # update the customer with the current cid.
        else:
            msg = "UpdateCustomer not performed. No customers in the queue."
            log.info(msg)
            print msg

        # Create Payment Account
        if len(customers):
            pid = doCreatePaymentAccount(customers[-1])  # Create a new account and attach it to the current customer
        else:
            msg = "CreatePaymentAccount not performed. No customers in the queue."
            log.info(msg)
            print msg

        # Update Payment Account
        doUpdatePaymentAccount(cid, pid)   # Try updating one of the accounts for this customer id  FIX - need to make this queue based

        # Get Payment Account
        doGetPaymentAccount(cid, pid)  # see if we can pull back the account we created and attached earlier

        # Delete Payment Account
        doDeletePaymentAccount(cid, pid)  # Now delete the associated account

        # Update a Customer and Payment
        cid = doCreateCustomerAndPayment()    # First, create a new customer and remember the cid for other transactions
        doUpdateCustomerAndPayment(cid)    # Update a new customer and remember the cid for other transactions

        # Create a Recurring Paymnet
        cid = doCreateCustomerAndPayment()  # First, create a new customer and remember the cid for recurring transactions
        pid = doCreateRecurringPaymentPlan(cid)  # Establish a recurring payment plan

        # Update Recurring Payment Plan
        doUpdateRecurringPaymentPlan(cid, pid)  # Update a recurring payment plan

        # Create Installment Plan
        cid = doCreateCustomerAndPayment()  # First, create a new customer and remember the cid for installment transactions
        pid = doCreateInstallmentPaymentPlan(cid)  # Establish an installment payment Plan

        # Confirmed bug on server
        # try:
        #    doUpdateInstallmentPaymentPlan(cid, pid)  # Update an installment payment plan
        # except (WpTimeoutError, WpConnectionError, WpTooManyRedirectsError, WpJSONError, WpBadResponseError, WpJSONError, WpHTTPError, WpInvalidEndpointError) as e:
        #    print(e.message)
        #    sys.exit(1)

        # Create Variable Payment Plan
        cid = doCreateCustomerAndPayment()  # Create a new customer and remember the cid for other transactions
        pid = doCreateVariablePaymentPlan(cid)  # Establish a variable payment Plan

        # Update Variable Payment Plan
        try:
            doUpdateVariablePaymentPlan(cid, pid)  # Update a variable payment plan
        except (WpTimeoutError, WpConnectionError, WpTooManyRedirectsError, WpJSONError, WpBadResponseError, WpJSONError, WpHTTPError, WpInvalidEndpointError) as e:
            print(e.message)
            sys.exit(1)

        # Get Payment Plan
        doGetPaymentPlan(cid, pid)  # Update a variable payment plan

        # Do a non-linked credit transaction - disabled until I can get this enabled by SecureNet
        # try:
        #   doCredit()
        # except (WpTimeoutError, WpConnectionError, WpTooManyRedirectsError, WpJSONError, WpBadResponseError, WpJSONError, WpHTTPError,WpInvalidEndpointError) as e:
        #   print(e.message)
        #   sys.exit(1)

    except (WpTimeoutError, WpConnectionError, WpTooManyRedirectsError, WpJSONError, WpBadResponseError, WpHTTPError, WpInvalidEndpointError) as e:
        print(e.message)
        if worldpay.doubleSecretProbation is not None:  # For now, if requested, dump return headers to a special file
            worldpay.doubleSecretProbation.close()
        sys.exit(1)  # return error to the shell in case this program is scripted

    return


def enactTestScript():
    try:
        cid = doCreateCustomerAndPayment()
        tk = doCreateToken(cid=cid, saveToVault=True)
        doChargeWithToken(cid=cid, token=tk)

    except (WpTimeoutError, WpConnectionError, WpTooManyRedirectsError, WpJSONError, WpBadResponseError, WpHTTPError, WpInvalidEndpointError) as e:
        print(e.message)
        raise  # push the error up

    return


if __name__ == "__main__":  # Start the program
    main(sys.argv[1:])
