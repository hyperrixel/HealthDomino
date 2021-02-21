"""
HealthDomino
============

HealthDomino is a GDPR or HIPAA compatible data driven service, that helps
the user to store, manage, share or use their own personal medical records or
health data securely with the advantages of being anonymous or with revealed
identity at the same time.

WHY PYTHON?
-----------
We use Python for planning, modeling and prototyping purposes. We think Python
code is much easier to read at the first time.

The use of Python doesn't mean that we'll develop our production ready solution
in Python or in Python only. We transform our solutions to C++ or Java quite
often.

THIS FILE
---------
This file contains the mock server functionality. Aside of the expected behavior
nothing is well implemented.
"""
from base64 import b64encode
from copy import deepcopy
from os import urandom
from hashlib import sha256



class Server(object):



    # Those dictionaries represent databases. They can be stored on different nodes.
    hddo_inner = {}
    hddo_nounces = {}
    hddo_outer = {}
    hddo_reserved = {}
    users = {}



    @classmethod
    def acceptHDDO(cls, hddo, transmission_id):

        print('[Server] Accepting HealthDominoDataObject... ', end='')
        result = ''
        if hddo.innerHash in Server.hddo_reserved.keys():
            if transmission_id == Server.hddo_reserved[hddo.innerHash]:
                print('Success.')
                nounce = urandom(64)
                outer_hash = sha256(hddo.toHashable() +  nounce).hexdigest()
                while outer_hash in Server.hddo_outer.keys():
                    nounce = urandom(64)
                    outer_hash = sha256(hddo.toHashable() +  nounce).hexdigest()
                Server.hddo_nounces[hddo.innerHash] = nounce
                Server.hddo_outer[outer_hash] = hddo.innerHash
                Server.hddo_inner[hddo.innerHash] = hddo
                del Server.hddo_reserved[hddo.innerHash]
                result = outer_hash
            else:
                print('Failed because of bad transmission_id.')
        else:
            print('Failed because transmission is not prepared.')
        return result




    @classmethod
    def createAccountIfAvailable(cls, account_pha, account_public_key):

        print('[Server] Checking PHA availability... ', end='')
        result = account_pha not in Server.users.keys()
        if result:
            print('Success.')
            Server.users[account_pha] = account_public_key
            print('[Server] Account "{}" registered succefully.'.format(account_pha))
        else:
            print('Failed.')
        return result



    @classmethod
    def deleteHDDO(cls, hddo, hash_base):

        result = False
        print('[Server] Searching for HealthDominoDataObject... ', end='')
        if hddo.innerHash in Server.hddo_inner.keys():
            print('Success.')
            print('[Server] Comparing HealthDominoDataObjects... ', end='')
            if hddo.toHashable() == Server.hddo_inner[hddo.innerHash].toHashable():
                print('Success.')
                print('[Server] Validating hashBase... ', end='')
                base_str = '{}{}'.format(hash_base, Server.hddo_inner[hddo.innerHash].toHashBase())
                test_inner_hash = sha256(base_str.encode('utf-8')).hexdigest()
                if test_inner_hash == Server.hddo_inner[hddo.innerHash].innerHash:
                    print('Success.')
                    print('[Server] Deleting HealthDominoDataObject occurences... ', end='')
                    del Server.hddo_nounces[hddo.innerHash]
                    del Server.hddo_inner[hddo.innerHash]
                    del Server.hddo_outer[hddo.outerHash]
                    print('Finished.')
                    result = True
                else:
                    print('Failed.')
            else:
                print('Failed.')
        else:
            print('Failed.')
        return result



    @classmethod
    def isValidUser(cls, account_pha):

        return account_pha in Server.users.keys()



    @classmethod
    def reserveIfAvailable(cls, inner_hash):

        print('[Server] Checking HDDO transmission availability... ', end='')
        if inner_hash not in Server.hddo_inner.keys() and inner_hash not in Server.hddo_reserved.keys():
            print('Success.')
            Server.hddo_reserved[inner_hash] = b64encode(urandom(64))
            return Server.hddo_reserved[inner_hash]
        else:
            print('Failed.')
            return ''

    @classmethod
    def sendBroadcast(cls, inner_hash):

        result = []
        print('[Server] Broadcast intiative accepted.')
        print('[Server] Searching for HealthDominoDataObject... ')
        if inner_hash in Server.hddo_inner.keys():
            print('Success.')
            print('[Server] Validating HealthDominoDataObject against broadcast availability... ')
            if len(Server.hddo_inner[inner_hash].script) > 0:
                print('Success.')
                result = deepcopy(Server.hddo_inner[inner_hash].script)
                print('[Server] BROADCAST: Connection is available for script "{}"'.format(' '.join(result)))
            else:
                print('Failed.')
        else:
            print('Failed.')
        return result
