#!/usr/bin/python

''' These are the common classes used to create Rest transactions.
    Main Functions
        wpTransact - this is call that makes the REST call.
    Global Variables
        worldpay - this is an instantiation of WPTotal
    Main Classes
        WPTotal - This class defines much of the static setup required to communicate.
                It is accessed through the singleton 'worldpay'. Most of the time you will
                only need access to devAppId to fill in a transaction request.
        WPTarget - local to module. This class defines the url endpoints and access method
'''

import requests
import logging
from base64 import b64encode
from pprint import pformat
from json import dumps, loads
from time import localtime, strftime

from wpexceptions import WpTimeoutError, WpConnectionError, WpTooManyRedirectsError, WpJSONError, WpHTTPError, WpInvalidEndpointError

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


class WPTotal:
    '''This class contains the constants and methods that affect the entire application'''

    # Constants
    host = "DEMO" # Determines the environment endpoint. Options are "DEMO" or "IPC"
    merchantId = '8006912'  # Change to your personal id as provided in your enrollemnt email
    merchantKey = 'cQxbjK2bCDfp'  # Change to your key procided by Virtual Terminal
    devId = 12345678  # Not sure where this comes from - totally fictional at this time
    appVersion = '0.1'  # internal
    httpProxy = 'http://10.1.1.91'  # Change to your HTTP proxy - Only used if -p option at cmdline
    httpsProxy = 'https://10.1.1.91'  # Change to your HTTPS proxy - Only used if -p option at cmdline
    timeout = 20  # Timeout for all http calls
    logFileName = 'log.txt'  # Where to send the log entries
    errorLogDirectory = "errorlogs"  # subdirectory to place error logs in
    publicKey = '5ad6c3eb-c93f-4d3e-8cb1-0aa847e079e5'
    testDataFileName = "testdata.csv"
    doubleSecretProbation = None  # This is a file that is opened for special debugging behaviors. set on the command line. Not for general consumption
    hostPrefix = { 
            "DEMO": "https://gwapi.demo.securenet.com/api/Payments/", 
            "IPC" : "localhost:8081/api/Payments/"
            }
    integrationType = {
        "DEMO": 0,
        "IPC": 1
        }


    # Class variables
    proxies = {}  # this will either be nil or the proxy depending on -p option
    httpHeader = {}  # this is the HTTP header that should be included in all REST posts
    devAppId = {}  # used in all of the REST post calls

    # Class methods
    def __init__(self):
        authId = "Basic " + b64encode(self.merchantId + ":" + self.merchantKey)
        self.httpHeader = {'Authorization': authId, 'Content-Type': 'application/json', 'Accept': 'application/json', 'Origin': 'worldpay.com'}
        self.devAppId = {'developerId': self.devId, 'version': self.appVersion, 'integrationType': self.integrationType.get(self.host)}

        log.debug("HTTP header: %s", pformat(self.httpHeader, indent=1))

        return

    def enableProxies(self):
        self.proxies = {
            'http': self.httpProxy,
            'https': self.httpsProxy
        }
        return

    def disableProxies(self):
        self.proxies = {}
        return


worldpay = WPTotal()  # base object for communicating with server


class WPTarget:
    '''This module local class is used to associate the proper endpoint URI with the operation name
        The main call is getURL(). It is not intended to be called outside of this module.
    '''

    wpPost = 1  # Constants - do not change
    wpGet = 2
    wpDelete = 3
    wpPut = 4

    method = 0  # wpPost, wpGet, wpDelete, or wpPut

    # This is the translation dictionary. While all operationsare in lowercase, any case will work on invocation.
    url = {
        # SecureNet Credit Card Present
        "authorize": (worldpay.hostPrefix.get(worldpay.host) + "Authorize", wpPost),
        "priorauthcapture": ("https://gwapi.demo.securenet.com/api/Payments/Capture", wpPost),
        "charge": ("https://gwapi.demo.securenet.com/api/Payments/Charge", wpPost),
        "credit": ("https://gwapi.demo.securenet.com/api/Payments/Credit", wpPost),
        "verify": ("https://gwapi.demo.securenet.com/api/Payments/Verify", wpPost),

        # SecureNet Credit Card Not Present
        # All payments on this page use the same Credit Card Present transactions

        # SecureNet ACH page
        # All payments on this page use the "charge" transaction

        # SecureNet Settlement page
        "closebatch": ("https://gwapi.demo.securenet.com/api/Batches/Close", wpPost),
        "getbatchbyid": ("https://gwapi.demo.securenet.com/api/Batches/XXX", wpGet),
        "getbatch": ("https://gwapi.demo.securenet.com/api/Batches/Current", wpGet),

        # SecureNet Credits page
        # All payments on this page use the "credit" transaction

        # SecureNet Refunds page
        "refund": ("https://gwapi.demo.securenet.com/api/Payments/Refund", wpPost),

        # SecureNet Voids page
        "void": ("https://gwapi.demo.securenet.com/api/Payments/Void", wpPost),

        # SecureNet Tokenization page
        "createtoken": ("https://gwapi.demo.securenet.com/api/PreVault/Card", wpPost),

        # SecureNet Vault page
        "createcustomer": ("https://gwapi.demo.securenet.com/api/Customers", wpPost),
        "getcustomer": ("https://gwapi.demo.securenet.com/api/Customers/XXX", wpGet),
        "updatecustomer": ("https://gwapi.demo.securenet.com/api/Customers/XXX", wpPut),
        "createpaymentaccount": ("https://gwapi.demo.securenet.com/api/Customers/XXX/PaymentMethod", wpPost),
        "getpaymentaccount": ("https://gwapi.demo.securenet.com/api/Customers/XXX/PaymentMethod/YYY", wpGet),
        "updatepaymentaccount": ("https://gwapi.demo.securenet.com/api/Customers/XXX/PaymentMethod/YYY", wpPut),
        "deletepaymentaccount": ("https://gwapi.demo.securenet.com/api/Customers/XXX/PaymentMethod/YYY", wpDelete),
        "createcustomerandpayment": ("https://gwapi.demo.securenet.com/api/Customers/Payments", wpPost),
        "updatecustomerandpayment": ("https://gwapi.demo.securenet.com/api/Customers/XXX/Payments", wpPut),

        # SecureNet Recurring Billing page
        "createrecurringpaymentplan": ("https://gwapi.demo.securenet.com/api/Customers/XXX/PaymentSchedules/recurring", wpPost),
        "updaterecurringpaymentplan": ("https://gwapi.demo.securenet.com/api/customers/XXX/PaymentSchedules/recurring/YYY", wpPut),
        "createinstallmentpaymentplan": ("https://gwapi.demo.securenet.com/api/Customers/XXX/PaymentSchedules/Installment", wpPost),
        "updateinstallmentpaymentplan": ("https://gwapi.demo.securenet.com/api/customers/XXX/PaymentSchedules/installment/YYY", wpPut),
        "createvariablepaymentplan": ("https://gwapi.demo.securenet.com/api/Customers/XXX/PaymentSchedules/Variable", wpPost),
        "updatevariablepaymentplan": ("https://gwapi.demo.securenet.com/api/customers/XXX/PaymentSchedules/variable/YYY", wpPut),
        "getpaymentplan": ("https://gwapi.demo.securenet.com/api/Customers/XXX/PaymentSchedules/YYY", wpGet),

        # SecureNet Transaction Reporting and Management Page
        "searchtransactions": ("https://gwapi.demo.securenet.com/api/Transactions/Search", wpPost),
        "gettransaction": ("https://gwapi.demo.securenet.com/api/Transactions/XXX", wpGet),
        "updatetransaction": ("https://gwapi.demo.securenet.com/api/transactions/XXX", wpPut),
    }

    def __init__(self):
        pass

    def getURL(self, o, p1=None, p2=None):
        '''This will retrieve the API endpoint. It uses variable args,
            since some of the endpoints have one or two variable components.
            Input:
                o - name of operation (see table above)
                p1 - variable one of endpoint if required (if text above has an XXX in the field)
                p2 - variable two of endpoint if required (if text above has an YYY in the field)
            Output:
                endpoint string
            Raises:
                WPInvalidEndpointError
            This function is not intended for use outside of this moduel.
        '''

        op = o.lower()  # op is the operation requested, in a string, formed to lowercase just to avoid calling errors

        validRequest = op in self.url  # test to make sure it is in the supported operations list
        if validRequest is False:
            errMsg = "Operation: " + op
            if p1 is not None:
                errMsg += " p1: " + str(p1)
                if p2 is not None:
                    errMsg += " p2: " + str(p2)
            raise WpInvalidEndpointError(errMsg)
        else:
            a = self.url[op]
            t = a[0]  # This is the target url
            self.method = a[1]  # this specifies the type of transaction
            method = ""
            if self.method == self.wpGet:
                method = "Get"
            if self.method == self.wpPost:
                method = "Post"
            if self.method == self.wpPut:
                method = "Put"
            if self.method == self.wpDelete:
                method = "Delete"
            log.debug("Method: %s Url: %s", method, t)

        endpoint = ""

        if t.find("YYY") >= 0:
            if (p1 is not None) and (p2 is not None):
                s = t.replace('XXX', p1)
                endpoint = s.replace('YYY', p2)

        elif t.find("XXX") >= 0:
            if p1 is not None:  # We'll ignore any p2 if provided
                endpoint = t.replace('XXX', str(p1))
        else:
            endpoint = t

        log.debug("translated url lookup: %s", endpoint)

        if endpoint == "":
            errMsg = "Operation: " + op
            if p1 is not None:
                errMsg = errMsg + " p1: " + p1
                if p2 is not None:
                    errMsg = errMsg + " p2: " + p2
            log.error("Invalid endpoint. %s", errMsg)
            raise WpInvalidEndpointError(errMsg)
        else:
            return endpoint


def wpTransact(operation, payload, *args):
    ''' This function makes the REST call. Input and output are dictionary objects.
        input:
            operation = String that identifies the operation (see 'url' above)
            payload = Dictionary that represents the data to be sent to the operation endpoint
        returns:
            Dictionary of the response
        raise:
            WpInvalidEndpoint
            WpTimeoutError
            WpConnectionError
            WpTooManyRedirectsError
            WpHTTPError
            WpJSONError
    '''
    target = WPTarget()  # API endpoint class

    if len(payload):
        transactionJSON = dumps(payload)  # Convert payload dictionary to JSON
    else:  # some transactions don't have a payload
        transactionJSON = ""

    if (len(args) == 2):
        p1 = args[0]
        p2 = args[1]
    elif (len(args) == 1):
        p1 = args[0]
        p2 = None
    else:
        p1 = None
        p2 = None

    # Get the registered endpoint
    try:
        url = target.getURL(operation, p1, p2)
    except:
        raise

    log.info(">>>>>>>>>>>>>>>>>>> %s %s >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", operation, strftime("%T", localtime()))
    log.info(">>>Payload>>> \n%s\n", pformat(payload, indent=1))
    log.info(">>>Target>>> \n%s", url)

    log.info(">>>HTTP header>>> \n%s", pformat(worldpay.httpHeader, indent=1))

    # Make the API call
    log.debug("JSON Request: \n%s\n", transactionJSON)
    try:
        if target.method == target.wpPost:  # is a post operation
            log.info(">>>Post>>>")
            responseJSON = requests.post(url, headers=worldpay.httpHeader, data=transactionJSON, proxies=worldpay.proxies, timeout=worldpay.timeout)
        elif target.method == target.wpGet:  # it is a get operation
            log.info(">>>Get>>>")
            responseJSON = requests.get(url, headers=worldpay.httpHeader, data=transactionJSON, proxies=worldpay.proxies, timeout=worldpay.timeout)
        elif target.method == target.wpPut:  # it is an update operation
            log.info(">>>Put>>>")
            responseJSON = requests.put(url, headers=worldpay.httpHeader, data=transactionJSON, proxies=worldpay.proxies, timeout=worldpay.timeout)
        elif target.method == target.wpDelete:  # it is a get operation
            log.info(">>>Delete>>>")
            responseJSON = requests.delete(url, headers=worldpay.httpHeader, data=transactionJSON, proxies=worldpay.proxies, timeout=worldpay.timeout)
        else:
            errMsg = "Operation: " + operation
            if p1 is not None:
                errMsg = errMsg + " p1: " + p1
            if p2 is not None:
                errMsg = errMsg + " p2: " + p2
            raise WpInvalidEndpointError(errMsg)

        responseJSON.raise_for_status  # make anything other than a 200 cause an exception

    except requests.exceptions.Timeout:
        raise WpTimeoutError(operation)

    except requests.exceptions.ConnectionError:
        raise WpConnectionError(operation)

    except requests.exceptions.TooManyRedirects:
        raise WpTooManyRedirectsError(operation)

    except requests.exceptions.HTTPError as e:
        raise WpHTTPError(e)

    log.debug("JSON Response: \n%s\n", responseJSON.text)
    if (responseJSON.status_code == requests.codes.ok):  # If result is good, convert to Dict and return
        ret = loads(responseJSON.text)
        log.info(">>>Response>>> \n%s\n", pformat(ret, indent=1))

        if worldpay.doubleSecretProbation is not None:  # For now, if requested, dump return headers to a special file
            h = '*' * 20 + operation + '*' * 20 + '\n'
            worldpay.doubleSecretProbation.write(h)
            worldpay.doubleSecretProbation.write(pformat(ret, indent=1))
            worldpay.doubleSecretProbation.write('\n')
        return ret

    else:
        raise WpJSONError(str(responseJSON.status_code))
