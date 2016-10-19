#!/usr/bin/python

'''These are all of the classes used to read the results from the REST callte
    All class names match the APIDOC names provided, including case.
    Main Classes
        ResponseParameters - base class of attributes common to all Response Objects
        AuthParameters - Data returned from auth charge, verify, prior auth capture, void, refund, and credit (also base class for all other top level Response Objects)
        BatchResponseParameters - Data returned from get batch, get batch by id, and close batch
        TokenResponseParameters - Data received from create token
        CustomerResponseParameters - Data received from create customer, update customer, get customer
        PaymentAccountResponseParameters - Data received from create vault account, get vault account, update payment account, delete payment account
        CustomerAndPaymentResponseParameters

    Notes:
        If a data element is not found,the member object will contain None.
        Some variable names end in RO. This stands for Response Object and is used avoid namespace clash with a similar name in the request object namespace
'''
import logging
from pprint import pformat


log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


class ResponseParameters(object):
    '''This is the base class for all of the other response objects'''

    def __init__(self, d={}):
        log.debug("ResponseParameters class: %s", pformat(d, indent=1))

        # self.result = d.setdefault("result", None)
        self.result = d.setdefault("result", None)
        self.responseCode = d.setdefault("responseCode", None)
        self.message = d.setdefault("message", None)
        self.jsonRequest = d.setdefault("jsonRequest", None)  # this wasn't in the original !!docx!!
        self.rawRequest = d.setdefault("rawRequest", None)  # this wasn't in the original !!docx!!
        self.rawResponse = d.setdefault("rawResponse", None)  # this wasn't in the original !!docx!!
        self.responseDateTime = d.setdefault("responseDateTime", None)  # this wasn't in the original !!docx!!
        self.success = d.setdefault("success", None)  # this wasn't in the original !!docx!!


class AuthResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after get batch, get batch by id, and close batch operations'''

    def __init__(self, d={}):
        log.debug("AuthResponseParameters class: %s", pformat(d, indent=1))

        if 'transaction' in d:
            self.transaction = Transaction(d['transaction'])  # tunnel down
        else:
            self.transaction = None
        if 'emvResponse' in d:  # This was mislabelled in the original !!doc!x!
            self.emvResponse = d.setdefault("emvResponse", None)
        else:
            self.emvResponse = None

        super(AuthResponseParameters, self).__init__(d)  # init the base class


class BatchResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after get batch, get batch by id, and close batch operations'''

    def __init__(self, d={}):
        log.debug("BatchResponseParameters class: %s", pformat(d, indent=1))

        self.batchCount = d.setdefault("batchCount", None)
        self.batchId = d.setdefault("batchId", None)
        # note that there are two closely named jsaon elements called transaction and transactions
        # transaction is a single Transaction entry and used in some REST calls
        # transactions is an array of Transactions and is included in other calls.

        if 'transaction' in d:
            self.transaction = Transaction(d["transaction"])  # tunnel down
        else:
            self.transaction = []

        self.transactions = []
        if d['transactions'] is not None:
            for i, k in enumerate(d["transactions"]):  # iterate through the one or more transaction records
                log.debug("Enumerate tranactions: i=%d, k=%s", i, pformat(k, indent=1))
                self.transactions.append(Transaction(k))

        if 'emvResponse' in d:  # This was mislabelled in the original !!docx!!
            self.emvResponse = d.setdefault("emvResponse", None)
        else:
            self.emvResponse = None
        super(BatchResponseParameters, self).__init__(d)  # init the base class


class TokenResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after performing a create token operation'''

    def __init__(self, d={}):
        log.debug("TokenResponseParameters class: %s", pformat(d, indent=1))

        self.customerId = d.setdefault("customerId", None)
        self.token = d.setdefault("token", None)

        if 'emvResponse' in d:  # This was mislabelled in the original !!docx!!
            self.emvResponse = d.setdefault("emvResponse", None)
        else:
            self.emvResponse = None

        super(TokenResponseParameters, self).__init__(d)  # init the base class


class CustomerResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after performing a create, update or get customer operations'''

    def __init__(self, d={}):
        log.debug("CustomerResponseParameters class: %s", pformat(d, indent=1))
        self.customerId = d.setdefault("customerId", None)

        if 'vaultCustomer' in d:
            self.vaultCustomer = VaultCustomer(d["vaultCustomer"])  # tunnel down
        else:
            self.vaultCustomer = None

        super(CustomerResponseParameters, self).__init__(d)  # init the base class


class PaymentAccountResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after performing a create, update, get, or delete payment account operations'''

    def __init__(self, d={}):
        log.debug("PaymentAccountResponseParameters class: %s", pformat(d, indent=1))
        # in the original !!docx!! but not seen in JSON self.customerId = d.setdefault("customerId", None)

        if 'vaultPaymentMethod' in d:
            self.vaultPaymentMethod = VaultPaymentMethod(d["vaultPaymentMethod"])  # tunnel down
        else:
            self.vaultPaymentMethod = None

        if 'emvResponse' in d:  # This was mislabelled in the original !!docx!!
            self.emvResponse = d.setdefault("emvResponse", None)
        else:
            self.emvResponse = None

        super(PaymentAccountResponseParameters, self).__init__(d)  # init the base class


class CustomerAndPaymentResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after performing a Customer and Payment operation'''

    def __init__(self, d={}):
        log.debug("CustomerAndPaymentResponseParameters class: %s", pformat(d, indent=1))
        # This is in the original !!docx!! but doesn't show on the JSON stream self.customerId = d.setdefault("customerId", None)

        self.accountMessage = d.setdefault("accountMessage", None)  # These weren't in the original !!docx!!
        self.accountResponseCode = d.setdefault("accountResponseCode", None)  # These weren't in the original !!docx!!
        self.accountResponseMessage = d.setdefault("accountResponseMessage", None)  # These weren't in the original !!docx!!
        self.accountResult = d.setdefault("accountResult", None)  # These weren't in the original !!docx!!
        self.accountSuccess = d.setdefault("accountSuccess", None)  # These weren't in the original !!docx!!
        self.assignedPaymentId = d.setdefault("assignedPaymentId", None)  # These weren't in the original !!docx!!
        self.customerMessage = d.setdefault("customerMessage", None)  # These weren't in the original !!docx!!
        self.customerREsponseCode = d.setdefault("customerResponseCode", None)  # These weren't in the original !!docx!!
        self.customerResponseMessage = d.setdefault("CustomerResponseMessage", None)  # These weren't in the original !!docx!!
        self.customerResult = d.setdefault("customerResult", None)  # These weren't in the original !!docx!!
        self.customerSuccess = d.setdefault("customerSuccess", None)  # These weren't in the original !!docx!!

        if 'vaultCustomer' in d:
            self.vaultCustomer = VaultCustomer(d["vaultCustomer"])  # tunnel down
        else:
            self.vaultCustomer = None

        if 'emvResponse' in d:  # This was mislabelled in the original !!docx!!
            self.emvResponse = d.setdefault("emvResponse", None)
        else:
            self.emvResponse = None

        super(CustomerAndPaymentResponseParameters, self).__init__(d)  # init the base class


class RecurringPaymentPlanResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after performing a Recurring Payment operation'''

    def __init__(self, d={}):
        log.debug("RecurringPaymentPlanResponseParameters class: %s", pformat(d, indent=1))
        self.customerId = d.setdefault("customerId", None)
        self.planId = d.setdefault("planId", None)

        if 'storedRecurringPaymentPlan' in d:
            self.storedRecurringPaymentPlan = RecurringPaymentPlanRO(d["storedRecurringPaymentPlan"])  # tunnel down
        else:
            self.storedRecurringPaymentPlan = None

        super(RecurringPaymentPlanResponseParameters, self).__init__(d)  # init the base class


class InstallmentPaymentPlanResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after performing a Recurring Payment operation'''

    def __init__(self, d={}):
        log.debug("InstallmentPaymentPlanResponseParameters class: %s", pformat(d, indent=1))
        self.customerId = d.setdefault("customerId", None)
        self.planId = d.setdefault("planId", None)

        if 'storedInstallmentPaymentPlan' in d:
            self.storedInstallmentPaymentPlan = InstallmentPaymentPlanRO(d["storedInstallmentPaymentPlan"])  # tunnel down
        else:
            self.storedInstallmentPaymentPlan = None

        super(InstallmentPaymentPlanResponseParameters, self).__init__(d)  # init the base class


class VariablePaymentPlanResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after performing a Recurring Payment operation'''

    def __init__(self, d={}):
        log.debug("VariablePaymentPlanResponseParameters class: %s", pformat(d, indent=1))
        self.customerId = d.setdefault("customerId", None)
        self.planId = d.setdefault("planId", None)

        if 'storedVariablePaymentPlan' in d:
            self.storedVariablePaymentPlan = VariablePaymentPlanRO(d["storedVariablePaymentPlan"])  # tunnel down
        else:
            self.storedVariablePaymentPlan = None

        super(VariablePaymentPlanResponseParameters, self).__init__(d)  # init the base class


class GetPaymentPlanResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after performing a Recurring Payment operation'''

    def __init__(self, d={}):
        log.debug("GetPaymentPlanResponseParameters class: %s", pformat(d, indent=1))
        self.customerId = d.setdefault("customerId", None)
        self.planId = d.setdefault("planId", None)
        self.planType = "Unknown"

        if d['storedInstallmentPaymentPlan'] is not None:
            self.planType = "Installment"
            self.storedInstallmentPaymentPlan = InstallmentPaymentPlanRO(d["storedInstallmentPaymentPlan"])  # tunnel down
        else:
            self.storedInstallmentPaymentPlan = None

        if d['storedVariablePaymentPlan'] is not None:
            self.planType = "Variable"
            self.storedVariablePaymentPlan = VariablePaymentPlanRO(d["storedVariablePaymentPlan"])  # tunnel down
        else:
            self.storedVariablePaymentPlan = None

        if d['storedRecurringPaymentPlan'] is not None:
            self.planType = "Recurring"
            self.storedRecurringPaymentPlan = RecurringPaymentPlanRO(d["storedRecurringPaymentPlan"])  # tunnel down
        else:
            self.storedRecurringPaymentPlan = None

        super(GetPaymentPlanResponseParameters, self).__init__(d)  # init the base class


class TransactionReportingResponseParameters(ResponseParameters):
    '''This is the class that will be filled in after performing a Search/Retrieve/Update Transaction'''

    def __init__(self, d={}):
        log.debug("TransactionReportingResponseParameters class: %s", pformat(d, indent=1))
        self.ipAddress = d.setdefault("ipAddress", None)  # only provided in Update Transaction
        if 'transaction' in d:
            self.transaction = Transaction(d['transaction'])  # tunnel down
        else:
            self.transaction = None

        self.transactions = []
        if 'transactions' in d:
            for i, k in enumerate(d["transactions"]):  # iterate through the one or more transaction records
                log.debug("Enumerate tranactions: i=%d, k=%s", i, pformat(k, indent=1))
                self.transactions.append(Transaction(k))

        super(TransactionReportingResponseParameters, self).__init__(d)  # init the base class


'''
    All of the objects below are contained within the various classes above.
    You do not need to instantiate these as they are created in the constructors
    of the classes above. They are named in accordance with the name used in
    https://www.worldpay.com/us/developers/apidocs/getstarted.html.
'''


class Transaction(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("Transaction class: %s", pformat(d, indent=1))

        self.customerId = d.setdefault("customerId", None)  # not in original !!docx!!
        self.emailReceipt = d.setdefault("emailReceipt", None)  # not in original !!docx!!
        self.fleetCardInfo = d.setdefault("fleetCardInfo", None)  # not in original !!docx!!
        self.fnsNumber = d.setdefault("fnsNumber", None)  # not in original !!docx!!
        self.imageResult = d.setdefault("imageResult", None)  # not in original !!docx!!
        self.marketSpecificData = d.setdefault("marketSpecificData", None)  # not in original !!docx!!
        self.voucherNumber = d.setdefault("voucherNumber", None)  # not in original !!docx!!
        self.additionalData1 = d.setdefault("additionalData1", None)  # not in original !!docx!!
        self.additionalData2 = d.setdefault("additionalData2", None)  # not in original !!docx!!
        self.additionalData3 = d.setdefault("additionalData3", None)  # not in original !!docx!!
        self.additionalData4 = d.setdefault("additionalData4", None)  # not in original !!docx!!
        self.additionalData5 = d.setdefault("additionalData5", None)  # not in original !!docx!!
        self.secureNetId = d.setdefault("secureNetId", None)
        self.transactionType = d.setdefault("transactionType", None)
        self.responseText = d.setdefault("responseText", None)
        self.orderId = d.setdefault("orderId", None)
        self.transactionId = d.setdefault("transactionId", None)
        self.authorizationCode = d.setdefault("authorizationCode", None)
        self.authorizedAmount = d.setdefault("authorizedAmount", None)
        self.allowedPartialCharges = d.setdefault("authorizedAmount", None)
        self.paymentTypeCode = d.setdefault("paymentTypeCode", None)
        self.paymentTypeResult = d.setdefault("paymentTypeResult", None)
        self.level2Valid = d.setdefault("level2Valid", None)
        self.level3Valid = d.setdefault("level3Valid", None)
        self.creditCardType = d.setdefault('creditCardType', None)
        self.cardNumber = d.setdefault('cardNumber', None)
        self.avsCode = d.setdefault('avsCode', None)
        self.avsResult = d.setdefault('avsResult', None)
        self.cardholder_firstName = d.setdefault('cardHolder_FirstName', None)
        self.cardholder_lastName = d.setdefault('cardHolder_LastName', None)
        self.expirationDate = d.setdefault('expirationDate', None)
        self.email = d.setdefault('email', None)
        # This is in the !!docx!! but I see no evidence it is in the JSON self.phone = d.setdefault("phone", None)
        # This is in the !!docx!! but I see no evidence it is in the JSON self.company = d.setdefault('company', None)
        self.cardCodeCode = d.setdefault('cardCodeCode', None)
        self.cardCodeResult = d.setdefault('cardCodeResult', None)
        self.accountName = d.setdefault('accountName', None)
        self.accountType = d.setdefault('accountType', None)
        self.accountNumber = d.setdefault('accountNumber', None)
        self.checkNumber = d.setdefault('checkNumber', None)
        self.traceNumber = d.setdefault('traceNumber', None)
        self.surchargeAmount = d.setdefault('surchargeAmount', None)
        self.cashBackAmount = d.setdefault('cashBackAmount', None)
        self.gratuity = d.setdefault('gratuity', None)
        self.industrySpecificData = d.setdefault('industrySpecificData', None)
        self.networkCode = d.setdefault('networkCode', None)
        self.additionalAmount = d.setdefault('additionalAmount', None)
        self.method = d.setdefault('method', None)

        if 'billAddress' in d:
            self.billAddress = AddressRO(d['billAddress'])  # tunnel down
        else:
            self.billAddress = None

        if 'transactionData' in d:
            self.transactionData = TransactionData(d["transactionData"])  # tunnel down
        else:
            self.transactionData = None

        if 'settlementData' in d:
            self.settlementData = SettlementData(d['settlementData'])  # tunnel down
        else:
            self.settlementData = None

        if 'vaultData' in d:
            self.vaultData = VaultData(d["vaultData"])  # tunnel down
        else:
            self.vaultData = None

        ''' The following fields show up in the json but are not in the !!docsx!! for Transaction
        additionalData1
        additionalData2
        additionalData3
        additionalData4
        additionalData5
        customerId
        emailReceipt
        fleetCardInfo
        fnsNumber
        voucherNumber
        '''


class TransactionData(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("TransactionData class: %s", pformat(d, indent=1))
        self.date = d.setdefault("date", None)
        self.amount = d.setdefault("amount", None)


class SettlementData(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("SettlementData class: %s", pformat(d, indent=1))
        self.date = d.setdefault("date", None)
        self.amount = d.setdefault("amount", None)
        self.batchId = d.setdefault("batchId", None)


class VaultData(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("VaultData class: %s", pformat(d, indent=1))
        self.company = d.setdefault("company", None)
        self.firstName = d.setdefault("firstName", None)
        self.lastName = d.setdefault("lastName", None)
        self.email = d.setdefault("email", None)
        self.phone = d.setdefault("phone", None)

        if 'token' in d:
            self.token = Token(d["token"])  # tunnel down
        else:
            self.token = None


class VaultCustomer(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("VaultCustomer class: %s", pformat(d, indent=1))
        self.customerId = d.setdefault("customerId", None)
        self.firstName = d.setdefault("firstName", None)
        self.lastName = d.setdefault("lastName", None)
        self.emailAddress = d.setdefault("emailAddress", None)  # This was mislabelled in the original !!docx!!
        self.sendEmailReceipts = d.setdefault("sendEmailReceipts", None)
        self.company = d.setdefault("company", None)
        self.notes = d.setdefault("notes", None)
        self.phoneNumber = d.setdefault("phoneNumber", None)
        self.primaryPaymentMethodId = d.setdefault("primaryPaymentMethodId", None)

        if 'address' in d:
            self.address = AddressRO(d['address'])  # tunnel down
        else:
            self.address = None

        self.variablePaymentPlans = []
        if d['variablePaymentPlans'] is not None:
            for i, k in enumerate(d["variablePaymentPlans"]):  # iterate through the one or more payment plan records
                log.debug("Enumerate variable payment plans: i=%d, k=%s", i, pformat(k, indent=1))
                self.variablePaymentPlans.append(VariablePaymentPlanRO(k))

        self.recurringPaymentPlans = []
        if d['recurringPaymentPlans'] is not None:
            for i, k in enumerate(d["recurringPaymentPlans"]):  # iterate through the one or more payment plan records
                log.debug("Enumerate recurring payment plans: i=%d, k=%s", i, pformat(k, indent=1))
                self.recurringPaymentPlans.append(RecurringPaymentPlanRO(k))

        self.installmentPaymentPlans = []
        if d['installmentPaymentPlans'] is not None:
            for i, k in enumerate(d["installmentPaymentPlans"]):  # iterate through the one or more payment plan records
                log.debug("Enumerate installment payment plans: i=%d, k=%s", i, pformat(k, indent=1))
                self.installmentPaymentPlans.append(InstallmentPaymentPlanRO(k))

        self.userDefinedFields = []
        if d['userDefinedFields'] is not None:
            for i, k in enumerate(d["userDefinedFields"]):  # iterate through the one or more user defined record
                log.debug("Enumerate user defined fields: i=%d, k=%s", i, pformat(k, indent=1))
                self.userDefinedFields.append(UserDefinedFieldRO(k))

        self.paymentMethods = []
        if d['paymentMethods'] is not None:
            for i, k in enumerate(d["paymentMethods"]):  # iterate through the one or more user defined record
                log.debug("Enumerate paymentMethod fields: i=%d, k=%s", i, pformat(k, indent=1))
                self.paymentMethods.append(PaymentMethod(k))


'''
This is a !!doc!! error


class VaultCustomerAndPayment(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("VaultCustomerAndPayment class: %s", pformat(d, indent=1))
        if 'vaultCustomer' in d:
            self.vaultCustomer = VaultCustomer(d["vaultCustomer"])  # tunnel down
        if 'vaultPaymentMethod' in d:
            self.vaultPaymentMethod = VaultPaymentMethod(d["vaultPaymentMethod"])  # tunnel down
        self.accountResult = 0
        self.accountResponseCode = 0
        self.accountMessage = ""
        self.customerResult = 0
        self.customerResponseCode = 0
        self.customerMessage = ""
'''


class VaultPaymentMethod(object):
    def __init__(self, d={}):
        if d is None:
            return
        self.customerId = d.setdefault("customerId", None)
        self.paymentId = d.setdefault("paymentId", None)
        self.notes = d.setdefault("notes", None)
        self.method = d.setdefault("method", None)
        self.primary = d.setdefault("primary", None)
        self.lastAccessDate = d.setdefault("lastAccessDate", None)

        if 'card' in d:
            self.card = MaskedCard(d["card"])  # tunnel down
        else:
            self.card = None

        if 'check' in d:
            self.check = CheckRO(d["check"])
        else:
            self.check = None

        self.userDefinedFields = []
        if d['userDefinedFields'] is not None:
            for i, k in enumerate(d["userDefinedFields"]):  # iterate through the one or more user defined record
                log.debug("Enumerate user defined fields: i=%d, k=%s", i, pformat(k, indent=1))
                self.userDefinedFields.append(UserDefinedFieldRO(k))


class PaymentMethod(object):
    def __init__(self, d={}):
        if d is None:
            return
        self.customerId = d.setdefault("customerId", None)
        self.paymentId = d.setdefault("paymentId", None)
        self.notes = d.setdefault("notes", None)
        self.method = d.setdefault("method", None)
        self.primary = d.setdefault("primary", None)
        # in the original !!docx!! but not seen in JSON string self.creditCardType = d.setdefault("creditCardType", None)
        self.lastAccessDate = d.setdefault("lastAccessDate", None)

        if 'card' in d:
            self.card = MaskedCard(d["card"])  # tunnel down
        else:
            self.card = None

        if 'check' in d:
            self.check = CheckRO(d["check"])
        else:
            self.check = None

        self.userDefinedFields = []
        if d['userDefinedFields'] is not None:
            for i, k in enumerate(d["userDefinedFields"]):  # iterate through the one or more user defined record
                log.debug("Enumerate user defined fields: i=%d, k=%s", i, pformat(k, indent=1))
                self.userDefinedFields.append(UserDefinedFieldRO(k))


class VariablePaymentPlanRO(object):
    def __init__(self, d={}):
        if d is None:
            return
        self.planStartDate = d.setdefault("planStartDate", None)
        self.planEndDate = d.setdefault("planEndDate", None)
        self.primaryPaymentMethod = d.setdefault("primaryPaymentMethod", None)
        self.secondaryPaymentMethod = d.setdefault("secondaryPaymentMethod", None)
        self.nextPaymentDate = d.setdefault("nextPaymentDate", None)

        self.active = d.setdefault("active", None)
        self.notes = d.setdefault("notes", None)
        self.planId = d.setdefault("planId", None)
        self.startDate = d.setdefault("startDate", None)
        self.nextPaymentDate = d.setdefault("nextPaymentDate", None)
        self.maxRetries = d.setdefault("maxRetries", None)
        self.primaryPaymentMethodId = d.setdefault("primaryPaymentMethodId", None)
        self.secondaryPaymentMethodId = d.setdefault("secondaryPaymentMethodId", None)

        self.scheduledPayments = []
        if d['scheduledPayments'] is not None:
            for i, k in enumerate(d["scheduledPayments"]):  # iterate through the one or more payment plan records
                log.debug("Enumerate scheduled payments: i=%d, k=%s", i, pformat(k, indent=1))
                self.scheduledPayments.append(ScheduledPaymentRO(k))

        self.userDefinedFields = []
        if d['userDefinedFields'] is not None:
            for i, k in enumerate(d["userDefinedFields"]):  # iterate through the one or more user defined record
                log.debug("Enumerate user defined fields: i=%d, k=%s", i, pformat(k, indent=1))
                self.userDefinedFields.append(UserDefinedFieldRO(k))


class ScheduledPaymentRO(object):
    def __init__(self, d={}):
        if d is None:
            return
        self.amount = d.setdefault("amount", None)
        self.scheduledDate = d.setdefault("scheduledDate", None)
        self.numberOfRetries = d.setdefault("numberOfRetries", None)
        self.paid = d.setdefault("paid", None)
        self.paymentDate = d.setdefault("paymentDate", None)
        self.paymentMethodId = d.setdefault("paymentMethodId", None)
        self.planId = d.setdefault("planId", None)
        self.processed = d.setdefault("processed", None)
        self.scheduleId = d.setdefault("scheduleId", None)
        self.transactionId = d.setdefault("transactionId", None)


class RecurringPaymentPlanRO(object):
    def __init__(self, d={}):
        if d is None:
            return
        self.cycleType = d.setdefault("cycleType", None)
        self.dayOfTheMonth = d.setdefault("dayOfTheMonth", None)
        self.dayOfTheWeek = d.setdefault("dayOfTheWeek", None)
        self.month = d.setdefault("month", None)
        self.frequency = d.setdefault("frequency", None)
        self.endDate = d.setdefault("endDate", None)
        self.active = d.setdefault("active", None)
        self.notes = d.setdefault("notes", None)
        self.planId = d.setdefault("planId", None)
        self.startDate = d.setdefault("startDate", None)
        self.nextPaymentDate = d.setdefault("nextPaymentDate", None)
        self.maxRetries = d.setdefault("maxRetries", None)
        self.primaryPaymentMethodId = d.setdefault("primaryPaymentMethodId", None)
        self.secondaryPaymentMethodId = d.setdefault("secondaryPaymentMethodId", None)

        self.userDefinedFields = []
        if 'userDefinedFields' in d:
            for i, k in enumerate(d["userDefinedFields"]):  # iterate through the one or more user defined record
                log.debug("Enumerate user defined fields: i=%d, k=%s", i, pformat(k, indent=1))
                self.userDefinedFields.append(UserDefinedFieldRO(k))


class InstallmentPaymentPlanRO(object):
    def __init__(self, d={}):
        if d is None:
            return
        self.cycleType = d.setdefault("cycleType", None)
        self.dayOfTheMonth = d.setdefault("dayOfTheMonth", None)
        self.dayOfTheWeek = d.setdefault("dayOfTheWeek", None)
        self.month = d.setdefault("month", None)
        self.frequency = d.setdefault("frequency", None)
        self.totalAmount = d.setdefault("totalAmount", None)
        self.numberOfPayments = d.setdefault("numberOfPayments", None)
        self.installmentAmount = d.setdefault("installmentAmount", None)
        self.balloonAmount = d.setdefault("balloonAmount", None)
        self.balloonPaymentAddedTo = d.setdefault("balloonPaymentAddedTo", None)
        self.remainderAmount = d.setdefault("remainderAmount, None)")
        self.remainderAmountAddedTo = d.setdefault("remainderAmountAddedTo", None)
        self.active = d.setdefault("active", None)
        self.notes = d.setdefault("notes", None)


class Token(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("Token class: %s", pformat(d, indent=1))
        self.customerId = d.setdefault("customerId", None)
        self.paymentMethodId = d.setdefault("paymentMethodId", None)
        self.paymentType = d.setdefault("paymentType", None)


class AddressRO(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("AddressRO class: %s", pformat(d, indent=1))
        self.line1 = d.setdefault('line1', None)
        self.city = d.setdefault('city', None)
        self.state = d.setdefault('state', None)
        self.zip = d.setdefault('zip', None)
        self.country = d.setdefault('country', None)
        self.company = d.setdefault('company', None)
        self.phone = d.setdefault('phone', None)


class MaskedCard(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("MaskedCard class %s", pformat(d, indent=1))
        self.company = d.setdefault('company', None)
        self.creditCardType = d.setdefault('creditCardType', None)
        self.email = d.setdefault('email', None)
        self.expirationDate = d.setdefault('expirationDate', None)
        self.firstName = d.setdefault('firstName', None)
        self.lastName = d.setdefault('lastName', None)
        self.lastFourDigits = d.setdefault('lastFourDigits', None)
        self.maskedNumber = d.setdefault('maskedNumber', None)

        if 'address' in d:
            self.address = AddressRO(d['address'])  # tunnel down
        else:
            self.address = None


class UserDefinedFieldRO(object):
    # FIX This object needs some research - leave blank for now.
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("UDF Response class %s", pformat(d, indent=1))


class CheckRO(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("CheckRO class %s", pformat(d, indent=1))
        self.accountType = d.setdefault('accountType', None)
        self.checkType = d.setdefault('checkType', None)
        self.routingNumber = d.setdefault('routingNumber', None)
        self.accountNumber = d.setdefault('accountNumber', None)
        self.checkNumber = d.setdefault('checkNumber', None)
        self.firstName = d.setdefault('firstName', None)
        self.lastName = d.setdefault('lastName', None)
        self.email = d.setdefault('email', None)
        self.front = d.setdefault('front', None)
        self.back = d.setdefault('back', None)
        self.verification = d.setdefault('verification', None)

        if 'address' in d:
            self.address = AddressRO(d['address'])  # tunnel down
        else:
            self.address = None


class EmvResponse(object):
    def __init__(self, d={}):
        if d is None:
            return
        log.debug("EmvResponse class %s", pformat(d, indent=1))
        self.issuerauthenticationdata = d.setdefault('issuerauthenticationdata', None)
        self.issuerscripttemplateE1 = d.setdefault('issuerscripttemplateE1', None)
        self.issuerscripttemplateE2 = d.setdefault('issuerscripttemplateE2', None)
