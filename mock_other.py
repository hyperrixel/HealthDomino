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
This file contains the some other mock functionality. Aside of the expected
behavior nothing is well implemented.
"""
from time import localtime, strftime, time



class ScriptEngine(object):



    COMMANDS = ['HD_ADD', '<SigKey>']



    @classmethod
    def evaluate(cls, script: list, sig_key: int) -> int:

        pointer = 0
        memmory = [0, 0]
        for command in script[:-1]:
            if command.isnumeric():
                memmory[pointer] = int(command)
                pointer += 1
            elif command == '<SigKey>':
                memmory[pointer] = int(command)
                pointer += 1
            elif command == 'HD_ADD':
                memmory[0] = memmory[0] + memmory[1]
                pointer = 0
            if pointer > 1:
                pointer = 0
        return memmory[pointer] == int(script[-1])



    @classmethod
    def validate(cls, script: list) -> bool:

        for command in script:
            try:
                _ = int(command)
                is_int = True
            except:
                is_int = False
            if not is_int:
                if command not in ScriptEngine.COMMANDS:
                    print(command)
                    return False
        return True



def get_readable_time(timestamp):

    return strftime('%m/%d/%Y %H:%M:%S', localtime(timestamp))



def now():

    return int(time())
