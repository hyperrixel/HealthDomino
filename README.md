[![Generic badge](https://img.shields.io/badge/Version-v_0.1-4a5781.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/State-proof_of_concept-00b4e3.svg)](https://shields.io/)<br>

# HealthDomino

GDPR and HIPAA compatible file format and transmission protocol for eHealth data

[![HealthDomino](https://github.com/hyperrixel/HealthDomino/blob/main/asset/logo_1080p.png "HealthDomino")](https://youtu.be/tyYRclJ_Utw)

# About us

## Who we are

We are two deep learning developers and data scientists who are interested in the fields of healthcare. We work in a lot of different fields of AI developing. Nowadays, most companies like to hire developers who are outsiders, who have other skills and education. We are lawyers who have jumped from law to programming and deep learning. We had a lot of opportunities from Facebook and Udacity. These companies maintain scholarship programs to get knowledge from people around the world. We were two of them. Computer Vision Nanodegree or Deep Learning Nanodegree were supported by Facebook. Besides the knowledge, we got a lot of new viewpoints and the possibility to help others. We are thankful and we are trying to give back something to the community and to the people around the Globe. Under these signs, we created a lot of open source projects.
We like to work in hackathon-style. Hackathon is more than a normal challenge where a bunch of people develop and everybody is a rival. It is an opportunity to get together, to know each other’s way of thinking and to create connections that exist longer than a 2 or 3 days challenge. It is about to dare dream something and build from scratch within days. Hackathon is an attitude. Hackathon is a life-form. Every day is a hackathon in our life.

## Our relevant projects

### DOF – Deep Model Core Output Framework [Hackathon winner]

[![Generic badge](https://img.shields.io/badge/-hackathon%20winner-yellow)](https://shields.io/)
[Repository here.](https://github.com/hyperrixel/dof)

### MGP – Medical Gateway Platform

[Repository here.](https://github.com/hyperrixel/MedicalGatewayPlatform)

### Aaion [Hackathon global finalist]

[![Generic badge](https://img.shields.io/badge/-hackathon%20global%20finalist-yellow)](https://shields.io/)
[Repository here.](https://github.com/hyperrixel/aaion)

# Problem description

## Actuality

In the age of IoT and big data, there is a lot of data that could be collected and used in healthcare. New smart devices pop up day by day. Based on the location of the user, there are different regulations for data collecting, processing or handling. Sensitive and health data should be handled in a proper way that fits for the regulations of *GDPR* or *HIPAA*. 

## Anonymity and the right to erasure

In an ideal world everyone wants to store data fully anonymous that is separated by the data subject, while at the same time the data can be easily deleted when the data subject modifies their own earlier given statement. When the data is permanently separated from the data subject, it is not possible for the data subject to bear their own rights granted by GDPR. It has to be a slight connection between the data and the data subject. However, this *connection can be anonymous and secure at the same time*.

## Hackers

In daily life we can hear slogans like “data is the new oil” that describe the data is a real and valuable asset. Such as a lot of cash in a bank is desirable for robbers, data assets are attracted attention of hackers. There is no 100% perfect defence from hackers.However, we can make their job harder. When we can create enough aggravating circumstances, the data will be relatively worthless, since the hacker has to work a lot and consume a lot of time and energy for small success. We know, they won’t be changes their attitude, but it is enough that they will search for other data from other companies. 

# Real-world impact

## What it does

### Workflow

![Workflow](https://github.com/hyperrixel/HealthDomino/blob/main/asset/workflow.png "Workflow")

### User side

HealthDomino is GDPR and HIPAA compatible file format and transmission protocol for eHealth data. It helps the user to process and transmit the collected *raw data* from various sources for example smart devices, medical records, user inputs. The collected raw data get immediately transformed into an *encoded data* with a user-side encoding script. This script is changing in every run. The next phase is when the user encrypts the encoded data. The parameters of the encryption script renews at each time of run. So if the user sends the same raw data at two or more times, the hashes will be different.

### Server side

In the transmission phase the user sends the data into the central server. This transmission contains 3 async connections for the encrypted data, the encoding script and the user’s public key. After that all 3 data is on the server side, the server decrypts the data package via the user's public key. The result of the process is the encoded data. This key and the given *encrypted data* will be thrown out after this phase. Due to security reasons, the server re-encrypts this encoded data. On the server side each vulnerable data is stored in different places. It can mean different databases or different servers as well. One server for the *re-encrypted data*, one for the encoding key and one for the encryption key.

The data can be unpack anytime by the server and can be normalized or aggregated for use in deep learning tasks or statistical analysis. 

### Anonymity

Users can be anonymous during the whole process. There is no need to share sensitive data if they don’t want to. When a user wants to delete a unique datapoint or all datapoints, they can easily do it by providing the removable innerhash value and their own unique hashbase. This hashbase value is different in any datapoint and it is known only by the user.

### Broadcast message

Due to broadcasting service, data processors can send messages to the user without knowing the user’s real identity. It is possible since the response data package can be read by that user who sent the original data. The user can decide to accept or decline the message. The user can make or revoke consent statements anytime.

## Uniqueness

multilevel and multifactor encryption
broadcast message system
multistep data validation
providing anonymity and GDPR compatible
data labeling
future oriented scalability
hard to hack

## Datasources

The collected *raw data* can come from various sources:

- wearable smart devices
- other smart devices
- basic health supplement
- image from screening examination
- result of clinical examination
- attributes of user

## Security

HealthDomino uses working methods from steganography and cryptography to protect data. The user side encoding and encrypting scripts renew run by run, datapoint by datapoint. So if the user shares the same data two times, the hashes will be different. On the server side, all vulnerable data are stored in different databases. 

What if one of the databases is compromised?

- `encryption scripts`: decrypt every data and create a new encryption versions
- `encoding scripts`:  broadcast to the user to encode the data again and send back
- `encrypted data`: it is advised to broadcast to the user for providing a new encoded version again and re-encrypt the new datasets at server side

# Technologies

The demo of HealthDomino is written in Python, as it is prototype-friendly and it can easily read or adapt into other programming languages. Building blocks of our solution are used and tested on various fields from finance to IT security. Using hashes is a very common method in cryptography. 

# UML classmethod

![UML classmethod](https://github.com/hyperrixel/HealthDomino/blob/main/asset/UML_classmethod.png "UML classmethod")

# Future plans

We would like to make this project into a real-life solution. Since it is highly scalable, it can fit for the needs of future usage. 
