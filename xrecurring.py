#!/usr/bin/python
''' These are the transactions illustrated in SecureNet Vault
    Reference:
        http://apidocs.demo.securenet.com/docs/recurringbilling.html

    The main operations are:
        doRecurringPaymentPlan
        doInstallmentPaymentPlan
        doVariablePaymentPlan
        doGetPaymentPlan
'''

import datetime
import logging
from pprint import pformat

from wpauthobjects import UserDefinedField
from wprecurringobjects import RecurringPaymentPlanRequest, InstallmentPaymentPlanRequest, VariablePaymentPlanRequest, GetPaymentPlanRequest
from wprecurringobjects import RecurringPaymentPlan, ScheduledPayment, VariablePaymentPlan, InstallmentPaymentPlan
from wpresponseobjects import RecurringPaymentPlanResponseParameters, InstallmentPaymentPlanResponseParameters, VariablePaymentPlanResponseParameters, GetPaymentPlanResponseParameters
from wpexceptions import WpBadResponseError
from wptotal import wpTransact

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


def doCreateRecurringPaymentPlan(cid):
    '''Perform Create Recurring Payment
        Input:
            cid - customer id
        Output:
            planId - the id of the payment plan
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    plan = RecurringPaymentPlan()
    plan.cycleType = "monthly"
    plan.dayOfTheMonth = 1
    plan.dayOfTheWeek = 1
    plan.month = 6
    plan.frequency = 10
    plan.amount = 22.95
    plan.startDate = '10/1/2017'
    plan.endDate = '10/1/2035'
    plan.maxRetries = 4
    plan.primaryPaymentMethodId = 1
    plan.active = False

    plan.notes = "This is a recurring plan created by Joe Kleinwaechter"

    # Let's attach a UDF for fun
    udf1 = UserDefinedField()
    udf2 = UserDefinedField()
    now = datetime.datetime.now()
    udf1.udfName = 'udf1'
    udf1.value = now.strftime('%d-%b-%y')
    udf2.udfName = 'udf2'
    udf2.value = now.strftime('%I:%M %p')
    plan.attachUserDefinedField(udf1)
    plan.attachUserDefinedField(udf2)

    rec = RecurringPaymentPlanRequest()
    rec.customerId = cid
    # rec.planId =  don't think I need anything here for create
    rec.attachPlan(plan)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("CreateRecurringPaymentPlan", rec.serialize(), cid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = RecurringPaymentPlanResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doCreateRecurringPayment failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Create Recurring Payment Plan transaction successful. CustomerId: " + str(rp.customerId) + " PlanId: " + str(rp.planId)
    print msg
    log.info(msg)

    return rp.planId


def doUpdateRecurringPaymentPlan(cid, pid):
    '''Perform Update Recurring Payment
        Input:
            cid - customer id
            pid - paymnet plan id
        Output:
            planId - the id of the payment plan
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    plan = RecurringPaymentPlan()
    plan.cycleType = "monthly"
    plan.dayOfTheMonth = 1
    plan.dayOfTheWeek = 1
    plan.month = 6
    plan.frequency = 10
    plan.amount = 22.95
    plan.startDate = '10/1/2017'
    plan.endDate = '10/1/2035'
    plan.maxRetries = 4
    plan.primaryPaymentMethodId = 1
    plan.active = False

    plan.notes = "More recurring plan updates"

    # Let's attach a UDF for fun
    udf1 = UserDefinedField()
    udf2 = UserDefinedField()
    now = datetime.datetime.now()
    udf1.udfName = 'udf1'
    udf1.value = now.strftime('%d-%b-%y')
    udf2.udfName = 'udf2'
    udf2.value = now.strftime('%I:%M %p')
    plan.attachUserDefinedField(udf1)
    plan.attachUserDefinedField(udf2)

    rec = RecurringPaymentPlanRequest()
    rec.customerId = cid
    rec.planId = pid
    rec.attachPlan(plan)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("UpdateRecurringPaymentPlan", rec.serialize(), cid, pid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = RecurringPaymentPlanResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doUpdateRecurringPayment failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Update Recurring Payment Plan transaction successful. CustomerId: " + str(rp.customerId) + " PlanId: " + str(rp.planId)
    print msg
    log.info(msg)

    return rp.planId


def doCreateInstallmentPaymentPlan(cid):
    '''Perform Create Installment Payment Plan
        Input:
            cid - customer id
        Output:
            planId - the id of the payment plan
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    plan = InstallmentPaymentPlan()
    plan.cycleType = 'monthly'
    plan.dayOfTheMonth = 1
    plan.dayOfTheWeek = 1
    plan.frequency = 1
    plan.numberOfPayments = 12
    plan.installmentAmount = 276.95
    plan.remainderAmount = 12.90

    plan.balloonPaymentAddedTo = 'FIRST'
    plan.remainderPaymentAddedTo = 'LAST'
    plan.startDate = '9/1/2017'
    plan.endDate = '10/1/2020'
    plan.maxRetries = 4
    plan.primaryPaymentMethodId = 1
    plan.notes = 'This is an installment plan'
    plan.active = True
    plan.notes = "This is an installment plan created by Joe Kleinwaechter"

    # Throw in some udf, because, why not?
    udf1 = UserDefinedField()
    udf2 = UserDefinedField()
    now = datetime.datetime.now()
    udf1.udfName = 'udf1'
    udf1.value = now.strftime('%d-%b-%y')
    udf2.udfName = 'udf2'
    udf2.value = now.strftime('%I:%M %p')
    plan.attachUserDefinedField(udf1)
    plan.attachUserDefinedField(udf2)

    ins = InstallmentPaymentPlanRequest()
    ins.customerId = cid
    ins.attachPlan(plan)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("CreateInstallmentPaymentPlan", ins.serialize(), cid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = InstallmentPaymentPlanResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doCreateInstallmentPayment failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Create Installment Payment Plan transaction successful. CustomerId: " + str(rp.customerId) + " PlanId: " + str(rp.planId)
    print msg
    log.info(msg)

    return rp.planId


def doUpdateInstallmentPaymentPlan(cid, pid):
    '''Perform Updte Installment Payment Plan
        Input:
            cid - customer id (required)
            pid - only required if doing an update to an existing plan
        Output:
            planId - the id of the payment plan
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    plan = InstallmentPaymentPlan()
    plan.cycleType = 'monthly'
    plan.dayOfTheMonth = 1
    plan.dayOfTheWeek = 1
    plan.frequency = 1
    plan.numberOfPayments = 12
    plan.installmentAmount = 276.95
    plan.remainderAmount = 12.90

    plan.balloonPaymentAddedTo = 'FIRST'
    plan.remainderPaymentAddedTo = 'LAST'
    plan.startDate = '09/01/2017'
    plan.endDate = '10/01/2020'
    plan.maxRetries = 4
    plan.primaryPaymentMethodId = 1
    plan.notes = 'This is an installment plan'
    plan.active = True

    # Attach a user defined field
    udf1 = UserDefinedField()
    udf2 = UserDefinedField()
    now = datetime.datetime.now()
    udf1.udfName = 'udf1'
    udf1.value = now.strftime('%d-%b-%y')
    udf2.udfName = 'udf2'
    udf2.value = now.strftime('%I:%M %p')
    plan.attachUserDefinedField(udf1)
    plan.attachUserDefinedField(udf2)
    plan.numberOfPayments = 15

    ins = InstallmentPaymentPlanRequest()
    ins.customerId = cid
    plan.notes = "More installment plan updates"
    ins.planId = pid
    ins.attachPlan(plan)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("UpdateInstallmentPaymentPlan", ins.serialize(), cid, pid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = InstallmentPaymentPlanResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doUpdateInstallmentPayment failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Update Installment Payment Plan transaction successful. CustomerId: " + str(rp.customerId) + " PlanId: " + str(rp.planId)
    print msg
    log.info(msg)

    return rp.planId


def doCreateVariablePaymentPlan(cid):
    '''Perform Create Recurring Payment
        Input:
            cid - customer id (required)
            pid - only required if doing an update to an existing plan
        Output:
            planId - the id of the payment plan
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    plan = VariablePaymentPlan()

    plan.planStartDate = " 12/01/2017"
    plan.maxRetries = 4
    plan.primaryPaymentMethodId = 1
    plan.active = True
    plan.notes = "This is a variable plan created by Joe Kleinwaechter"

    sched = ScheduledPayment()
    sched.amount = 200.00
    sched.paid = False
    sched.paymentDate = '12/05/2017'

    udf1 = UserDefinedField()
    udf2 = UserDefinedField()
    now = datetime.datetime.now()
    udf1.udfName = 'udf1'
    udf1.value = now.strftime('%d-%b-%y')
    udf2.udfName = 'udf2'
    udf2.value = now.strftime('%I:%M %p')
    plan.attachUserDefinedField(udf1)
    plan.attachUserDefinedField(udf2)
    plan.attachScheduledPayment(sched)

    var = VariablePaymentPlanRequest()

    var.customerId = cid
    # var.planId =  not necerdssary for create I believe
    var.attachPlan(plan)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("CreateVariablePaymentPlan", var.serialize(), cid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = VariablePaymentPlanResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doCreateVariablePayment failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Create Variable Payment Plan transaction successful. CustomerId: " + str(rp.customerId) + " PlanId: " + str(rp.planId)
    print msg
    log.info(msg)

    return rp.planId


def doUpdateVariablePaymentPlan(cid, pid):
    '''Perform Update ta Variable Payment Plan
        Input:
            cid - customer id
            pid - payment plan id
        Output:
            planId - the id of the payment plan
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    plan = VariablePaymentPlan()

    plan.planStartDate = " 12/01/2017"
    plan.maxRetries = 4
    plan.primaryPaymentMethodId = 1
    plan.active = True
    plan.notes = "More variable plan updates."

    sched = ScheduledPayment()
    sched.amount = 200.00
    sched.paid = False
    sched.paymentDate = '12/05/2017'

    # Attach a UDF - just because we can
    udf1 = UserDefinedField()
    udf2 = UserDefinedField()
    now = datetime.datetime.now()
    udf1.udfName = 'udf1'
    udf1.value = now.strftime('%d-%b-%y')
    udf2.udfName = 'udf2'
    udf2.value = now.strftime('%I:%M %p')
    plan.attachUserDefinedField(udf1)
    plan.attachUserDefinedField(udf2)
    plan.attachScheduledPayment(sched)

    var = VariablePaymentPlanRequest()

    var.customerId = cid
    var.planId = pid
    var.attachPlan(plan)

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("UpdateVariablePaymentPlan", var.serialize(), cid, pid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = VariablePaymentPlanResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doUpdateVariablePayment failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Variable Payment Plan transaction successful. CustomerId: " + str(rp.customerId) + " PlanId: " + str(rp.planId)
    print msg
    log.info(msg)

    return rp.planId


def doGetPaymentPlan(cid, pid):
    ''' Retrieve an identified payment plan
        Input:
            cid - customer id (required)
            pid - plan id
        Output:
            planId - the id of the payment plan
        Raises:
            Exceptions raised by wpTransact()
    '''

    # 1. Fill in the Request Object
    var = GetPaymentPlanRequest()

    var.customerId = cid
    var.planId = pid

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("GetPaymentPlan", var.serialize(), cid, pid)
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = GetPaymentPlanResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):
        errMsg = "doGetPaymentPlan failed. Result: " + str(rp.result) + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        raise WpBadResponseError(errMsg)

    msg = "Get Payment Plan transaction successful. Type: " + rp.planType + " CustomerId: " + str(rp.customerId) + " PlanId: " + str(rp.planId)
    print msg
    log.info(msg)

    return rp.planId
