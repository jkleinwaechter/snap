#!/usr/bin/python
''' These are the transactions illustrated in Tokens
    Reference:
        https://www.worldpay.com/us/developers/apidocs/tokenization.html

    The main operations are:
        doCreateToken
'''
import logging
from pprint import pformat

from wpauthobjects import Card
from wptokenobjects import TokenRequest
from wpresponseobjects import TokenResponseParameters
from wptotal import wpTransact
from wptestcard import test

log = logging.getLogger(__name__)  # this allows the name of the current module to be placed in the log entry


def doCreateToken(cid="", saveToVault=False):
    '''Perform assign a customer a token
        Input:
            cid - optional - customer id to associate with this token.
            saveToVault - optional. Save the token in the customer's vault
        Output:
            Token
        Raises:
            Exceptions raised by wpTransact()
    '''
    test.random()  # get a random test data set

    # Step 1 Create an AuthorizationRequest Object and fill it in
    card = Card()
    card.number = test.getCardPAN()
    card.cvv = test.getCVV()
    card.expirationDate = test.getExpirationDate()

    tr = TokenRequest()
    tr.attachCard(card)
    tr.addToVault = saveToVault
    tr.customerId = cid  # let the system assign a token

    # 2. Send the transaction on a serialized Request Object
    try:
        response = wpTransact("CreateToken", tr.serialize())
    except:  # pass the exception up. Nothing to do here at the moment
        raise

    # 3. Deserialize the result into a Response Object
    rp = TokenResponseParameters(response)
    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    if (rp.responseCode != 1):  # response from Worldpay indicates failure
        errMsg = "CreateToken transaction failed. Result: " + rp.result + " Response Code: " + str(rp.responseCode) + " Message: " + rp.message
        print errMsg
        log.info(errMsg)
        return rp.responseCode

    token = rp.token

    log.info(">>>Response>>> \n%s", pformat(rp, indent=1))

    # return the response code
    msg = "CreateToken transaction successful. Token: " + str(token)
    print msg
    log.info(msg)
    return token
