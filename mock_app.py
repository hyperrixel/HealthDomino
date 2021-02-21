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
This file contains the mock application functionality. Aside of the expected
behavior nothing is well implemented.
"""
from base64 import b64decode, b64encode
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from hashlib import sha256
from mock_server import Server
from os import urandom
from tempfile import TemporaryFile



class App(object):



    user_pha = ''
    user_private_key = ''
    user_public_key = ''



    @classmethod
    def decryptForUser(cls, content):

        return PKCS1_OAEP.new(RSA.importKey(App.user_private_key)).decrypt(b64decode(content)).decode('utf-8')



    @classmethod
    def getUserPHA(cls):

        if App.user_pha == '':
            App.registerUser()
        return App.user_pha



    @classmethod
    def getUserPrivateKey(cls):

        if App.user_private_key == '':
            App.registerUser()
        return App.user_private_key



    @classmethod
    def getUserPublicKey(cls):

        if App.user_public_key == '':
            App.registerUser()
        return App.user_public_key



    @classmethod
    def encryptForUser(cls, content):

        if App.user_private_key == '':
            App.registerUser()

        return b64encode(PKCS1_OAEP.new(RSA.importKey(App.user_private_key)).encrypt(content.encode('utf-8')))



    @classmethod
    def prepareTransmission(cls, inner_hash: str) -> str:

        print('[App] Preparing transmission of a HealthDominoDataObject...')
        return Server.reserveIfAvailable(inner_hash)


    @classmethod
    def registerUser(cls):

        if App.user_pha == '' and App.user_private_key == '' and App.user_public_key == '':
            print('[App] Registering user.')
            pha = sha256(urandom(16)).hexdigest()
            print('[App] Please stroke the rabbit to help creating a key pair just for you. Thanks.')
            key_pair = RSA.generate(2048)
            private_key = key_pair.exportKey()
            public_key = key_pair.publickey().exportKey()
            print('[App] The rabbit is happy. Keys generated sucessfully.')
            print('[App] Registering account...')
            while not Server.createAccountIfAvailable(pha, public_key):
                pha = sha256(urandom(16)).hexdigest()
            App.user_pha = pha
            App.user_private_key = private_key
            App.user_public_key = public_key
            print('[App] Your Personal Health Address is: {}'.format(App.user_pha))
            print('      You don\'t have to remember it, this App will remember.')



    @classmethod
    def requestDelete(cls, hddo, hash_base):

        print('[App] Requesting deletion of HealthDominoDataObject with innerHash {}.'.format(hddo.innerHash))
        result = Server.deleteHDDO(hddo, hash_base)
        print('[App] All occurences of the HealthDominoDataObject is deleted.')



    @classmethod
    def transmitHDDO(cls, hddo, transmission_id):

        print('[App] Transmitting HealthDominoDataObject...')
        return Server.acceptHDDO(hddo, transmission_id)
