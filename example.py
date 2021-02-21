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
This file contains a demo workflow with clarifications.
Please try to interpret the content and the output of this file like a log
of a real-world workflow.
"""
from copy import deepcopy
from hddo import HealthDominoDataObject, RawData
from mock_app import App
from mock_other import get_readable_time, now, ScriptEngine
from mock_server import Server
from random import choice, randrange, uniform


# The ultimate first step of a process is to start the imagined application and
# make connection with the server. In the case of HealthDomino it means, thath
# the application and the server establishes an SSH connection.
#
# After this step they aggree in the outer encrypting layer which can be
# selected from custom list that is available on both sides. This can ensure
# a fair balance between actual performance and security level. With other
# words this is kind of scalability.
#
# Mext step is to agree in a sequence of different encondings forward . This
# ensures that encoding is assyncronous and cannot get compromised that easily.



# For all cases let's ganerate a Personal Health Address for our user
# The print messages demonstrate a potential use-case where the generation
# of keys is gamified by stroking a rabbit.
personal_health_address = App.registerUser()


###############
# SCENARIO 1. #
###############
print('\n\n###############')
print('# SCENARIO 1. #')
print('###############\n\n')



# Let'S assume, the user a device that sands body temperature to the smartphone
# and there is an application on the smartphone that uses HealthDomino.

# The data is something like this:
scenario_1_data = {}
scenario_1_data['device'] = 'thermometer'
scenario_1_data['measuremnet_type'] = 'body_temperature'
scenario_1_data['measuremnet_unit'] = 'celsius'
scenario_1_data['value'] = 36.7
scenario_1_data['measured_at'] = 1613862953

# The onDataReceived handler of the application does something like this.
print('[App][Log] Data received at {}'.format(get_readable_time(now())))
scenario_1_datapoint = RawData('{}.{}.{}'.format(scenario_1_data['device'],
                                                 scenario_1_data['measuremnet_type'],
                                                 scenario_1_data['measuremnet_unit']),
                               scenario_1_data['value'],
                               scenario_1_data['measured_at'])
print('[App][Log] RawData generated:\n{}'.format(scenario_1_datapoint))



# The appliaction wraps the raw datapoint to a HealthDominoDataObject for further
# usage. In a real-world case some encoding would be also applied, but now
# for better readability we skip this step.
#
# Encodings can be good sources of protection since they are stored seaparately.
print('[App][Log] RawData wrapped with HealthDominoDataObject.')
scenario_1_hddo = HealthDominoDataObject(scenario_1_datapoint)



# Just to follow state changes of the HealthDominoDataObject, let's print it.
print(scenario_1_hddo)



# Just to rest simple let's close and transmit that HealthDominoDataObject without
# any additional info.
print('[App][Log] Closing HealthDominoDataObject.')
scenario_1_hddo.close()
print(scenario_1_hddo)

print('[App][Log] Transmitting HealthDominoDataObject.')
scenario_1_hddo.transmit()
print(scenario_1_hddo)

print('\n\nThe hashBase is: {}\n\n'.format(scenario_1_hddo.hashBase))

# Let's delete this object without revealing identity.
App.requestDelete(HealthDominoDataObject.toSendable(scenario_1_hddo),
                  scenario_1_hddo.hashBase)

###############
# SCENARIO 2. #
###############
print('\n\n###############')
print('# SCENARIO 2. #')
print('###############\n\n')



# To demonstrate how broadcast messages can work first let's create a couple of
# RawData object and transmit them all to the server.

# To enabel broadcast compatibility, every HealthDominoDataObject will have a
# custom script based on the user's private key. This way of scripting is not
# secure at all but can demonstrate how broadcasts work.
sig_key = hash(App.user_private_key)
script_template = ['<SigKey>', '0', 'HD_ADD', '0']
hddo_container = []
for i in range(randrange(30, 40)):
    raw_datapoint = RawData('human_measure.weight.kg', round(uniform(50.0, 70.0), 2))
    hddo_container.append(HealthDominoDataObject(raw_datapoint))
    script_result = sig_key + i
    this_script = deepcopy(script_template)
    this_script[1] = str(i)
    this_script[3] = str(script_result)
    hddo_container[-1].addScript(this_script)
    hddo_container[-1].close()
    hddo_container[-1].transmit()



# Since user applications usually doesn't initiate broadcasts let's connect the
# Server directly and initiate one. Before doing this let's choice a datapoint.
test_inner_hash = choice(list(Server.hddo_inner.keys()))

# With the innerHash we can initiate the broadcast.
test_script = Server.sendBroadcast(test_inner_hash)

# In this example we can easily find the concerned datapoint but in a real-world
# solution only the owner of the right signature key can accept the connection
# request.
