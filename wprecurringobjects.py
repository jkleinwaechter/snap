#!/usr/bin/python
'''These are the request objects used to make card present/not present calls.
    Reference
        https://www.worldpay.com/us/developers/apidocs/recurringbilling.html

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


class RecurringPaymentPlan(object):
    '''This is the payment plan referenced in the main Recurring Request Object'''

    def __init__(self):
        log.debug("RecurringPaymentPlan class:")
        self.amount = 0.0  # This isn't in the original !!docx!!
        self.cycleType = ""
        self.dayOfTheMonth = 0
        self.dayOfTheWeek = 0
        self.month = ""
        self.frequency = 0
        self.endDate = ""
        self.active = False
        self.notes = ""
        self.planId = 0
        self.startDate = ""
        self.nextPaymentDate = ""
        self.maxRetries = 0
        self.primaryPaymentMethodId = ""
        self.secondaryPaymentMethodId = ""
        self.userDefinedFields = []

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "amount": self.amount,
            "cycleType": self.cycleType,
            "dayOfTheMonth": self.dayOfTheMonth,
            "dayOfTheWeek": self.dayOfTheWeek,
            "month": self.month,
            "frequency": self.frequency,
            "endDate": self.endDate,
            "active": self.active,
            "notes": self.notes,
            "planId": self.planId,
            "startDate": self.startDate,
            "nextPaymentDate": self.nextPaymentDate,
            "maxRetries": self.maxRetries,
            "primaryPaymentMethodId": self.primaryPaymentMethodId,
            "secondaryPaymentMethodId": self.secondaryPaymentMethodId,
            "userDefinedFields": self.userDefinedFields
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachUserDefinedField(self, udf):
        ''' add another UserDefinedField to the array. There is a limit of 50 UDFs'''
        self.userDefinedFields.append(udf.serialize())


class InstallmentPaymentPlan(object):
    '''This is the installment payment plan referenced in the main Installment Request Object'''

    def __init__(self):
        log.debug("InstallmentPaymentPlan class:")
        self.cycleType = ""
        self.dayOfTheMonth = 0
        self.dayOfTheWeek = 0
        self.month = ""
        self.frequency = 0
        self.totalAmount = 0.0
        self.numberOfPayments = 0
        self.installmentAmount = 0.0
        self.balloonAmount = 0.0
        self.balloonPaymentAddedTo = ""
        self.remainderAmount = 0.0
        self.remainderPaymentAddedTo = ""
        self.active = False
        self.notes = ""
        self.primaryPaymentMethodId = ""
        self.secondaryPaymentMethodId = ""
        self.startDate = ""  # This is not in the original !!docx!!
        self.userDefinedFields = []

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "cycleType": self.cycleType,
            "dayOfTheMonth": self.dayOfTheMonth,
            "dayOfTheWeek": self.dayOfTheWeek,
            "month": self.month,
            "frequency": self.frequency,
            "totalAmount": self.totalAmount,
            "numberOfPayments": self.numberOfPayments,
            "installmentAmount": self.installmentAmount,
            "balloonAmount": self.balloonAmount,
            "balloonPaymentAddedTo": self.balloonPaymentAddedTo,
            "remainderAmount": self.remainderAmount,
            "remainderPaymentAddedTo": self.remainderPaymentAddedTo,  # !!Doc!! error
            "active": self.active,
            "notes": self.notes,
            "primaryPaymentMethodId": self.primaryPaymentMethodId,
            "primaryPaymentMethodId": self.primaryPaymentMethodId,
            "startDate": self.startDate,
            "userDefinedFields": self.userDefinedFields
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachUserDefinedField(self, udf):
        ''' add another UserDefinedField to the array. There is a limit of 50 UDFs'''
        self.userDefinedFields.append(udf.serialize())


class VariablePaymentPlan(object):
    '''This is the payment plan referenced in the main Variable Payment Request Object'''

    def __init__(self):
        log.debug("VariablePaymentPlan class:")
        self.planStartDate = ""
        self.planEndDate = ""
        self.primaryPaymentMethodId = ""  # this shows up twice in the !!docx!!
        self.secondaryPaymentMethodId = ""  # this shows up twice in the !!docx!!
        self.nextPaymentDate = ""
        self.active = False
        self.notes = ""
        self.planId = 0
        self.startDate = ""
        self.nextPaymentDate = ""
        self.maxRetries = 0
        self.scheduledPayments = []
        self.userDefinedFields = []  # this shows up twice in the !!docx!!

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "planStartDate": self.planStartDate,
            "planEndDate": self.planEndDate,
            "primaryPaymentMethodId": self.primaryPaymentMethodId,
            "secondaryPaymentMethodId": self.secondaryPaymentMethodId,
            "nextPaymentDate": self.nextPaymentDate,
            "active": self.active,
            "notes": self.notes,
            "planId": self.planId,
            "startDate": self.startDate,
            "nextPaymentDate": self.nextPaymentDate,
            "maxRetries": self.maxRetries,
            "scheduledPayments": self.scheduledPayments,
            "userDefinedFields": self.userDefinedFields

        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachUserDefinedField(self, udf):
        ''' add another UserDefinedField to the array. There is a limit of 50 UDFs'''
        self.userDefinedFields.append(udf.serialize())

    def attachScheduledPayment(self, sched):
        ''' add another scheduled payment'''
        self.scheduledPayments.append(sched.serialize())


class ScheduledPayment(object):
    def __init__(self, d={}):
        if d is None:
            return
        self.amount = 0.0
        self.scheduledDate = ""
        self.numberOfRetries = 0
        self.paid = False
        self.paymentDate = ""
        self.paymentMethodId = ""
        self.planId = 0
        self.processed = ""
        self.scheduleId = 0
        self.transactionId = 0

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "amount": self.amount,
            "scheduledDate": self.scheduledDate,
            "numberOfRetries": self.numberOfRetries,
            "paid": self.paid,
            "paymentDate": self.paymentDate,
            "paymentMethodId": self.paymentMethodId,
            "planId": self.planId,
            "processed": self.processed,
            "scheduleId": self.scheduleId,
            "transactionId": self.transactionId
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d


'''
    The following classes are the main request objects.
'''


class RecurringPaymentPlanRequest(object):
    '''This is the main class to be used when installing a recurring payment plan '''

    def __init__(self):
        log.debug("RecurringPaymentPlanRequest class:")
        # Required
        self.developerApplication = {}  # This is automatically provided by deserialization
        self.customerId = 0
        self.plan = {}
        # Conditional
        self.planId = 0  # This is only needed if updating an existing plan

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "developerApplication": self.developerApplication,
            "customerId": self.customerId,
            "plan": self.plan,
            "planId": self.planId,
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachPlan(self, spp):
        ''' add a Stored payment Plan to the request'''
        self.plan = spp.serialize()


class InstallmentPaymentPlanRequest(object):
    '''This is the main class to be used when installing and installment plan '''

    def __init__(self):
        log.debug("InstallmentPaymentPlanRequest class:")
        # Required
        self.developerApplication = {}  # This is automatically provided by deserialization
        self.customerId = 0
        self.plan = {}
        # Conditional
        self.planId = 0  # This is only needed if updating an existing plan

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "developerApplication": self.developerApplication,
            "customerId": self.customerId,
            "plan": self.plan,
            "planId": self.planId
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachPlan(self, spp):
        ''' add a Stored payment Plan to the request'''
        self.plan = spp.serialize()


class VariablePaymentPlanRequest(object):
    '''This is the main class to be used when installing a variable payment plan '''

    def __init__(self):
        log.debug("VariablePaymentPlanRequest class:")
        # Required
        self.developerApplication = {}  # This is automatically provided by deserialization
        self.customerId = 0
        self.plan = {}
        # Conditional
        self.planId = 0  # This is only needed if updating an existing plan

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "developerApplication": self.developerApplication,
            "customerId": self.customerId,
            "plan": self.plan,
            "planId": self.planId
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d

    def attachPlan(self, spp):
        ''' add a Stored payment Plan to the request'''
        self.plan = spp.serialize()


class GetPaymentPlanRequest(object):
    '''This is the main class to be used when retrieving a payment plan '''

    def __init__(self):
        log.debug("GetPaymentPlanRequest class:")
        # Required
        self.developerApplication = {}  # This is automatically provided by deserialization
        self.customerId = 0
        self.planId = 0  # This is only needed if updating an existing plan

    def serialize(self):
        self.developerApplication = worldpay.devAppId  # This always needs to be added
        s = {
            "developerApplication": self.developerApplication,
            "customerId": self.customerId,
            "planId": self.planId
        }

        d = dict((k, v) for k, v in s.iteritems() if v)  # Remove any keys that have an empty value
        return d
