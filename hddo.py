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
This file contains the two most important objects; HealthDominoDataObject
and RawData.
"""
from base64 import b64encode
from copy import deepcopy
from hashlib import sha256
import json
from mock_app import App
from mock_other import ScriptEngine
from os import urandom
from time import localtime, strftime, time



class RawData(object):
    """
    This class represents a data element
    """



    DEFAULT_TIMESTAMP = 0
    LABELING_0 = 0



    def __init__(self, data_label: str, data_value: any,
                 timestamp: int=0,
                 labeling_version: int=0):
        """
        Initializes a RawData object
        ============================

        Parameters
        ----------
        data_label : str
            The label of the given data. Label must fit the rules of the actual
            labeling version. The possibility to change the labeling version
            at the level of a RawData object lets the system to have endless
            felxibility.
        data_value : any
            The value can be anything that matches the actual label. The
            validation of the value is impossible, since RawData can hold
            raw and encoded data values as well.
        timestamp : int, optional (0 if omitted)
            The time value of the actual data. If it's omitted or is set to 0,
            time value will be the time of instantiation.
        labeling_version : int, optional (0 if omitted)
            The version of labeling system used on storing the data. This number
            will be very useful in the future, since it can facilitate the use
            of RawData object according to yet unknown conditions as well.

        Throws
        ------
        HDDOInitException
            If the labeling doesn't match the requirements.

        Classmethods
        ------------
            fromJSON(json_string)
            validateLabel(label, labeling_version)

        Notes
        -----
        I.
            RawData object can hold any kind of data. The fact that a HDDO
            contains only one top RawData object, doesn't necessarily mean
            that the HDDO conatains one data element only. Top RawData object
            can be potentially anything e.g. an array/list/container of
            RawData objects as well.
        II.
            At the moment any labeling is accepted which matches the criterion
            of being a dot separated taxonomy alike string with 2 or 3 levels.
            In the production ready version real taxonomy requirements will be
            implemented.
        III.
            Always keep in mind, that the value of a RawData object might be
            encoded with a simple or advanced encoding function, therfore having
            a simple RawData object without its parent (in most cases the
            concerning HealthDominoDataObject) can lead to bad data.
        """

        if self.validateLabel(data_label, labeling_version=labeling_version):
            self.__label = data_label
            self.__version = labeling_version
        else:
            raise HDDOInitException('Given label didn\'t pass validation')
        self.__value = data_value
        if timestamp == RawData.DEFAULT_TIMESTAMP:
            self.__timestamp = int(time())
        else:
            self.__timestamp = timestamp



    @classmethod
    def fromJSON(cls, json_string: str): # -> RawData is not written here due to Python 3.7 compatibility.
        """
        Retrieves RawData object from JSON string
        =========================================

        Parameters
        ----------
        json_string : str
            A string to transform to a RawData object.

        Returns
        -------
        RawData
            The object created from the string

        Throws
        ------
        HDDOInitException
            1.
                If the deserialization of the given string is not successful.
            2.
                If the data doesn't seem to be RawData.
            3.
                If the RawData object missing keys.
            4.
                If RawData version is not supported.
            5.
                If the timestamp is not valid.
            6.
                If the label is not valid.
            7.
                If an unsupported object type is serialized as the value of the
                RawData object.

        See also
        --------
            Documentation of .to_json() method.

        Notes
        -----
        I.
            However JSON is absolutely unsecure it is widely used in API
            communication. Since RawData object doesn't shows whether it is
            encoded or not, even JSON transmission or storing can be somewhat
            safe but it is never recommended.
        II.
            Some object are not serializable to JSON on its own and there is no
            canonical way to do it in Python. Thats why RawData object can raise
            error if the deserialization of a value type is not supported. This
            behavior will be definitely changed in production ready code since
            there are a lot easy way solve this issue.
        III.
            A data is considered unsupported only in case if it is deserialized
            as dict and has an object_type key.
        """

        try:
            content = json.loads(json_string)
        except json.decoder.JSONDecodeError:
            raise HDDOInitException('Given parameter doesn\'t seem to be a JSON string.')
        if isinstance(content, dict):
            if 'object_type' in content.keys():
                if content['object_type'] == 'RawData':
                    if len(content.keys()) != 5:
                        raise HDDOInitException('Given RawData object missing keys.')
                    for key in ['version', 'timestamp', 'label', 'value']:
                        if key not in content.keys():
                            raise HDDOInitException('Given RawData object missing keys.')
                    if content['version'] not in [0]:
                        raise HDDOInitException('RawData version is not supported.')
                    if isinstance(content['timestamp'], int):
                        if content['timestamp'] < 0 or content['timestamp'] > int(time()):
                            raise HDDOInitException('RawData timestamp is invalid.')
                    else:
                            raise HDDOInitException('RawData timestamp is invalid.')
                    if not RawData.validateLabel(content['label'], content['version']):
                        raise HDDOInitException('RawData label didn\'t passed the validation.')
                    if isinstance(content['value'], dict):
                        if 'object_type' in content['value'].keys():
                            if content['value']['object_type'] == 'RawData':
                                content['value'] = RawData.fromJSON(content['value'])
                            else:
                                raise HDDOInitException('RawData value contains unsupported object.')
                    return RawData(content['label'], content['value'], content['timestamp'], content['version'])
                else:
                    raise HDDOInitException('Given JSON string doesn\'t seem to contain RawData object.')
            else:
                raise HDDOInitException('Given JSON string doesn\'t seem to contain RawData object.')
        else:
            raise HDDOInitException('Given JSON string doesn\'t seem to contain RawData object.')



    @property
    def label(self) -> str:
        """
        Gets the label of the object
        ============================

        Returns
        -------
        str
            The label of the RawData object.
        """

        return self.__label



    @property
    def timestamp(self) -> int:
        """
        Gets the timestamp of the object
        ================================

        Returns
        -------
        int
            The timestamp of the RawData object.
        """

        return self.__timestamp



    def toJSON(self) -> str:
        """
        Gets the JSON representation of the object
        ==========================================

        Returns
        -------
        str
            JSON string, that can be used to restore the object.

        See also
        --------
            Documentation of the classmethod .from_json().

        Notes
        -----
        I.
            However JSON is absolutely unsecure it is widely used in API
            communication. Since RawData object doesn't shows whether it is
            encoded or not, even JSON transmission or storing can be somewhat
            safe but it is never recommended.
        II.
            Some object are not serializable to JSON on its own and there is no
            canonical way to do it in Python. Thats why RawData object uses this
            approach. In production ready or future releases this part might
            be solved on a totally different way.
        """
        try:
            _ = json.dumps(self.value)
            value = self.value
        except (TypeError, OverflowError):
            value = {}
            value['object_type'] = self.value.__class__.__name__
            if isinstance(self.value, RawData):
                type_str = '_{}__'.format(value['object_type'])
                for key, data in self.value.__dict__.items():
                    value[key.replace(type_str, '')] = data
            else:
                type_str = '_{}'.format(value['object_type'])
                for key, data in self.value.__dict__.items():
                    value[key.replace(type_str, '')] = data

        return json.dumps({'object_type' : 'RawData', 'version' : self.version,
                           'timestamp' : self.timestamp, 'label' : self.label,
                           'value' : value})



    @property
    def value(self) -> any:
        """
        Gets the value of the object
        ============================

        Returns
        -------
        any
            The value of the RawData object.
        """

        return self.__value



    @classmethod
    def validateLabel(cls, label: str, labeling_version: int) -> bool:
        """
        Validates a label string
        ========================

        Parameters
        ----------
        label : str
            The label string to validate.
        labeling_version : int
            The version ID to select the validation process.

        Returns
        -------
        bool
            True if the label fits the validation criteria, False if not.

        Notes
        -----
        I.
            This method is classmethod. It's reason is to give opportunity to
            pre-check the validity of a label before creating a RawData object
            or a HealthDominoDataObject.
        II.
            At the moment any labeling is accepted which matches the criterion
            of being a dot separated taxonomy alike string with 2 or 3 levels.
            In the production ready version real taxonomy requirements will be
            implemented.
        """

        return len(label.split('.')) in [2, 3]



    @property
    def version(self) -> int:
        """
        Gets the version of the object
        ==============================

        Returns
        -------
        int
            The version of the RawData object.
        """

        return self.__version



    def __hash__(self) -> int:
        """
        Gets the hash value of the object
        =================================

        Returns
        -------
        int
            The hash value of the RawData object.

        Notes
        -----
        I.
            In production ready version custom hash function should be written
            to ensure cross-platform and cross-language compatibility.
        II.
            Production ready type of hashes should be more likely strings instead
            of int because it will produced with much more advanced hash methods
            like for example SHA-256.
        """

        if isinstance(self.value, RawData):
            value = hash(self.value)
        else:
            value = self.value
        return hash((self.label, value, self.timestamp, self.version))



    def __repr__(self) -> str:
        """
        Gets code snippet to create the same object
        ===========================================

        Returns
        -------
        str
            The snippet to use to create the same object.
        """

        return 'RawData(\'{}\', {}, {}, {})'.format(self.label, repr(self.value),
                                                    self.timestamp, self.version)



    def __str__(self) -> str:
        """
        Gets the content of the object in human readable form
        =====================================================

        Returns
        -------
        str
            The content of the object in human readable form.
        """

        return 'RawData obect version {}\n- {:>5} : {}\n- {:>5} : {}\n- {:>5} : {}'.format(self.version,
                                                                                             'Time',
                                                                                             strftime('%m/%d/%Y %H:%M:%S', localtime(self.timestamp)),
                                                                                             'Label',
                                                                                             self.label,
                                                                                             'Value',
                                                                                             self.value)



class HealthDominoDataObject(object):
    """
    This class demonstrates the HDDO workflow
    """



    VERSION_0 = 0



    def __init__(self, data: RawData, HDDO_version: int=0,
                 compatibility_limit: int=0):
        """
        Initializes a HealthDominoDataObject
        ====================================

        Parameters
        ----------
        data : RawData
            RawData to store or transmit with this object.
        HDDO_version : int, optional (0 if omitted)
            The version identifier of the HealthDominoDataObject
        compatibility_limit : int, optional (0 if omitted)
            The version identifier to restrict backward compatibility of a
            HealthDominoDataObject. This will be useful in future releases when
            more sophisticated data protections will be available. With this
            variable the user can control whether to let others with loewr
            security level acess their data or not.

        Notes
        -----
        I.
            HealthDominoDataObject is targetted to serve for multiple purposes.
            It has a whole lifecycle from instantiation to transmission. On the
            other hand a non-trasmitted HealthDominoDataObject can be stored
            on local device as well.
        """

        self.__data = data
        self.__version = HDDO_version
        self.__compatibility_limit = compatibility_limit
        self.__script = []
        self.__series_signature = ''
        self.__pha = ''
        self.__identity_info = {}
        self.__message = ''
        self.__is_closed = False
        self.__hash_base = ''
        self.__inner_hash = ''
        self.__is_transmitted = False
        self.__outer_hash = ''



    def addInfo(label: str, value: str):
        """
        Adds a new element to the identity informations
        ===============================================

        Parameters
        ----------
        label : str
            The label to use for the new elemnt.
        value : str
            The value of the new element.

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the label already exists.
        """

        if not self.isClosed:
            if label not in self.__identity_info.keys():
                self.__identity_info[label] = value
            else:
                raise HDDOPermissionException('Tried to add existing identity information twice to a HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to add identity information to a closed HealthDominoDataObject.')



    def addMessage(self, message):
        """
        Adds message to the object
        ==========================

        Parameters
        ----------
        message : str
            The message to add to the object.

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the message is already added.
        """

        if not self.isClosed:
            if self.__message == '':
                self.__message = message
            else:
                raise HDDOPermissionException('Tried to add messsage twice to a closed HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to add message to a closed HealthDominoDataObject.')



    def addPHA(self):
        """
        Adds the user's Personal Health Address to the object
        =====================================================

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the Personal Health Address is already added.
        """

        if not self.isClosed:
            if self.__pha == '':
                self.__pha = App.getUserPHA()
            else:
                raise HDDOPermissionException('Tried to add Personal Health Address twice to a closed HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to add Personal Health Address to a closed HealthDominoDataObject.')



    def addScript(self, script):
        """
        Adds a script to the object
        ===========================

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the script is already added.
            3.
                If the script is invalid.
        """

        if not self.isClosed:
            if len(self.__script) == 0:
                if ScriptEngine.validate(script):
                    self.__script = script
                else:
                    raise HDDOPermissionException('Tried to add an invalid script to a HealthDominoDataObject.')
            else:
                raise HDDOPermissionException('Tried to add script twice to a HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to add script to a closed HealthDominoDataObject.')



    def addSeriesSignature(self, signature):
        """
        Adds series signature to the object
        ===================================

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the series signature is already added.
        """

        if not self.isClosed:
            if self.__series_signature == '':
                self.__series_signature = signature
            else:
                raise HDDOPermissionException('Tried to add series signature twice to a closed HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to add series signature to a closed HealthDominoDataObject.')



    def close(self):
        """
        Closes the object
        =================

        Throws
        ------
        HDDOPermissionException
            If the object is already closed.
        """

        if not self.isClosed:
            self.__is_closed = True
        else:
            raise HDDOPermissionException('Tried to close a closed HealthDominoDataObject.')



    @property
    def compatibilityLimit(self) -> int:
        """
        Gets the compatibility limit version of the object
        ==================================================

        Returns
        -------
        int
            The ID of the compatibilityLimit of the HealthDominoDataObject.
        """

        return self.__compatibility_limit



    @property
    def data(self) -> RawData:
        """
        Gets the data of the object
        ===========================

        Returns
        -------
        RawData
            The RawData object of the HealthDominoDataObject.
        """

        return self.__data



    def delInfo(label: str):
        """
        Deletes an existing element from the identity informations
        ==========================================================

        Parameters
        ----------
        label : str
            The label to delete.

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the label doesn't exist.
        """

        if not self.isClosed:
            if label in self.__identity_info.keys():
                del self.__identity_info[label]
            else:
                raise HDDOPermissionException('Tried to delete non-existing identity information in a HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to delete identity information from a closed HealthDominoDataObject.')



    def delMessage(self):
        """
        Removes the message from the object
        ===================================

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the message is not yet added.
        """

        if not self.isClosed:
            if self.__message != '':
                self.__message = ''
            else:
                raise HDDOPermissionException('Tried to remove non-existing message from a HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to remove message from a closed HealthDominoDataObject.')



    def delPHA(self):
        """
        Removes the user's Personal Health Address from the object
        ==========================================================

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the Personal Health Address is not yet added.
        """

        if not self.isClosed:
            if self.__pha != '':
                self.__pha = ''
            else:
                raise HDDOPermissionException('Tried to remove not added Personal Health Address from a HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to remove Personal Health Address from a closed HealthDominoDataObject.')



    def delScript(self):
        """
        Removes the script from the object
        ==================================

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the script is not yet added.
        """

        if not self.isClosed:
            if len(self.__script) > 0:
                self.__pha = ''
            else:
                raise HDDOPermissionException('Tried to remove not added script from a HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to remove script from a closed HealthDominoDataObject.')



    def delSeriesSignature(self):
        """
        Removes the series signature from the object
        ============================================

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the series signature is not yet added.
        """

        if not self.isClosed:
            if self.__series_signature != '':
                self.__series_signature = ''
            else:
                raise HDDOPermissionException('Tried to remove not added seriesSignature from a HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to remove seriesSignature from a closed HealthDominoDataObject.')



    @property
    def hashBase(self) -> str:
        """
        Gets the hash base of the object
        ================================

        Returns
        -------
        str
            The hashBase of the HealthDominoDataObject.
        """

        return self.__hash_base



    @property
    def identityInfo(self) -> dict:
        """
        Gets a copy of the identity info of the object
        ==============================================

        Returns
        -------
        dict
            A copy of the identityInfo dict of the HealthDominoDataObject.
            Empty dict if no identity info is added.

        Notes
        -----
            This property returns a copy instead of the original object. The
            reason of that is to ensure the control over the change of this
            property. To reach the same behavior in the production ready code,
            sligthly different approaches are also available depending on
            programming language and other requirements.
        """

        return deepcopy(self.__identity_info)



    @property
    def innerHash(self) -> str:
        """
        Gets the inner hash of the object
        =================================

        Returns
        -------
        str
            The innerHash of the HealthDominoDataObject.
            Empty string if the object is not closed yet.
        """

        return self.__inner_hash



    @property
    def isClosed(self) -> bool:
        """
        Gets whether the object is closed or not
        ========================================

        Returns
        -------
        bool
            True, if the HealthDominoDataObject is closed, False if not yet.
        """

        return self.__is_closed



    @property
    def isTransmitted(self) -> bool:
        """
        Gets whether the object is transmitted or not
        =============================================

        Returns
        -------
        bool
            True, if the HealthDominoDataObject is transmitted, False if not yet.
        """

        return self.__is_transmitted



    @property
    def message(self) -> str:
        """
        Gets the message of the object
        ==============================

        Returns
        -------
        str
            The messsage of the HealthDominoDataObject.
            Empty string if the object has no message.
        """

        return self.__message



    @property
    def outerHash(self) -> str:
        """
        Gets the outer hash of the object
        =================================

        Returns
        -------
        str
            The outerHash of the HealthDominoDataObject.
            Empty string if the object is not transmitted yet.
        """

        return self.__outer_hash



    @property
    def pha(self) -> str:
        """
        Gets the Personal Health Address of the object
        ==============================================

        Returns
        -------
        str
            The Personal Health Address that belongs to the HealthDominoDataObject.
            Empty string, if no Personal Health Address is given.
        """

        return self.__pha



    @property
    def script(self) -> list:
        """
        Gets a copy of the script of the object
        =======================================

        Returns
        -------
        list
            A copy of the script list of the HealthDominoDataObject.
            Empty list if no script list is added.

        Notes
        -----
            This property returns a copy instead of the original object. The
            reason of that is to ensure the control over the change of this
            property. To reach the same behavior in the production ready code,
            sligthly different approaches are also available depending on
            programming language and other requirements.
        """

        return deepcopy(self.__script)



    @property
    def seriesSignature(self) -> str:
        """
        Gets the series signature of the object
        =======================================

        Returns
        -------
        str
            The seriesSignature of the HealthDominoDataObject.
            Empty string if no serises signature is added.
        """

        return self.__series_signature



    def setMessage(self, message: str):
        """
        Sets new value to the message of the object
        ===========================================

        Parameters
        ----------
        message : str
            The new message string.

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the message is not yet added.
        """

        if not self.isClosed:
            if self.__message != '':
                self.__message = ''
            else:
                raise HDDOPermissionException('Tried to set non-existing message in a closed HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to set message in a closed HealthDominoDataObject.')



    def setInfo(label: str, value: str):
        """
        Sets the value of an existing element in the identity informations
        ==================================================================

        Parameters
        ----------
        label : str
            The label of the elemnt to set.
        value : str
            The value to set for the element.

        Throws
        ------
        HDDOPermissionException
            1.
                If the method is called on a closed object.
            2.
                If the label doesn't exist.
        """

        if not self.isClosed:
            if label in self.__identity_info.keys():
                self.__identity_info[label] = value
            else:
                raise HDDOPermissionException('Tried to set non-existing identity information in a HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to set identity information in a closed HealthDominoDataObject.')



    def toHashable(self) -> str:
        """
        Transforms the content of the object to a hashable string
        =========================================================

        Returns
        -------
        str
            String that matches the criteria of being able to get hashed.
        """

        return self.toHashBase().encode('utf-8')



    def toHashBase(self) -> str:
        """
        Transforms the content of the object to a string
        =================================================

        Returns
        -------
        str
            String that matches the is prepared of being able to get hashed.
        """

        if self.hashBase != '':
            self_repr = '{}'.format(self.hashBase)
        else:
            self_repr = ''
        self_repr += '{}{}{}'.format(str(self.data), self.version,
                                     self.compatibilityLimit)
        if len(self.script) > 0:
            self_repr += ' '.join(self.script)
        if self.seriesSignature != '':
            self_repr += self.seriesSignature
        if self.pha != '':
            self_repr += self.pha
        for key, value in self.identityInfo.items():
            self_repr += '{}{}'.format(key, value)
        if self.message != '':
            self_repr += self.message

        return self_repr



    @classmethod
    def toSendable(cls, hddo): # HealthDominoDataObject is not written here due to Python 3.7 compatibility.
        """
        Transforms HealthDominoDataObject to secure sendable object
        ===========================================================

        Parameters
        ----------
        hddo : HealthDominoDataObject
            The object to transform.

        Returns
        -------
        HealthDominoDataObject
            The transformed object.

        Notes
        -----
            The use of this classmethod is the canonical way to remove hashBase
            from a HealthDominoDataObject.
        """

        result = HealthDominoDataObject(hddo.data, hddo.version, hddo.compatibilityLimit)
        result.addScript(hddo.script)
        result.addSeriesSignature(hddo.seriesSignature)
        for label, value in hddo.identityInfo.items():
            result.addInfo(label, value)
        result.addMessage(hddo.message)
        result.close()
        result.reset_(hddo.pha, hddo.innerHash, hddo.outerHash)
        return result


    def transmit(self):
        """
        Transmits the object
        ====================

        Throws
        ------
        HDDOPermissionException
            1.
                If the object is not yet closed.
            2.
                If the object is already transmitted.
        """

        if self.isClosed:
            if not self.isTransmitted:
                self.__hash_base = b64encode(urandom(64)).decode('utf-8')
                inner_hash = sha256(self.toHashable()).hexdigest()
                transmission_id = App.prepareTransmission(inner_hash)
                while transmission_id == '':
                    self.__hash_base = b64encode(urandom(64)).decode('utf-8')
                    inner_hash = sha256(self.toHashable()).hexdigest()
                    transmission_id = App.prepareTransmission(inner_hash)
                self.__inner_hash = inner_hash
                sendable = HealthDominoDataObject.toSendable(self)
                self.__outer_hash = App.transmitHDDO(sendable, transmission_id)
                if self.__outer_hash != '':
                    self.__is_transmitted = True
            else:
                raise HDDOPermissionException('Tried to transmit a transmitted HealthDominoDataObject.')
        else:
            raise HDDOPermissionException('Tried to transmit a non-closed HealthDominoDataObject.')



    @property
    def version(self) -> int:
        """
        Gets the version of the object
        ==============================

        Returns
        -------
        int
            The version of the HealthDominoDataObject.
        """

        return self.__version



    def reset_(self, pha: str, inner_hash: str, outer_hash: str):
        """
        Helper function to recreate the object
        ======================================

        Parameters
        ----------
        pha : str
            Personal Health Address of the object.
        inner_hash : str
            The value of innerHash to restore.
        outer_hash : str
            The value of outerHash to restore.

        Notes
        -----
        I.
            If bothe innerHash and outerHash are non-empty. Also isTransmitted
            will be set to True.
        II.
            Please never use this function from outside.
        """

        self.__pha = pha
        self.__inner_hash = inner_hash
        self.__outer_hash = outer_hash
        if inner_hash != '' and outer_hash != '':
            self.__is_transmitted = True



    def __hash__(self) -> int:
        """
        Gets the hash value of the object
        =================================

        Returns
        -------
        int
            The hash value of the RawData object.

        Notes
        -----
        I.
            This hash function generates neither innerHash nore outerHash. To
            understand the differences between hashes, please compare this
            function with the calculation of innerHash and outerHash.
        II.
            In production ready version custom hash function should be written
            to ensure cross-platform and cross-language compatibility.
        III.
            Production ready type of hashes should be more likely strings instead
            of int because it will produced with much more advanced hash methods
            like for example SHA-256.
        """
        return hash((hash(self.data), self.version, self.compatibilityLimit,
                          self.script, self.seriesSignature, self.pha,
                          self.identityInfo, self.message))



    def __repr__(self) -> str:
        """
        Gets code snippet to create the same object
        ===========================================

        Returns
        -------
        str
            The snippet to use to create the same object.
        """

        return 'HealthDominoDataObject({}, {}, {})'.format(repr(self.data),
                                                           self.version,
                                                           self.compatibilityLimit)



    def __str__(self) -> str:
        """
        Gets the content of the object in human readable form
        =====================================================

        Returns
        -------
        str
            The content of the object in human readable form.
        """

        result = 'HealthDominoDataObject:\nBODY:\n=====\n{}\n=====\nHEAD:\n=====\n'.format(self.data)
        result += '{:>22}: {}\n{:>22}: {}\n'.format('version', self.version,
                                                    'compatibilitiLimit', self.compatibilityLimit)
        if len(self.script) > 0:
            result += '{:>22}: {}\n'.format('script', ' '.join(self.script))
        else:
            result += '{:>22}: {}\n'.format('script', 'NO-SCIRPT')
        if self.seriesSignature != '':
            result += '{:>22}: {}\n'.format('seriesSignature', self.seriesSignature)
        else:
            result += '{:>22}: {}\n'.format('seriesSignature', 'NOT-ADDED')
        if self.pha != '':
            result += '{:>22}: {}\n'.format('personalHealthAddress', self.pha)
        else:
            result += '{:>22}: {}\n'.format('personalHealthAddress', 'NOT-ADDED')
        if len(self.identityInfo) > 0:
            for key, value in self.identityInfo.items():
                result += '{:>22}: {} -> {}\n'.format('identityInfo', key, value)
        else:
            result += '{:>22}: {}\n'.format('identityInfo', 'NOT-ADDED')
        if self.message != '':
            result += '{:>22}: {}\n'.format('message', self.message)
        else:
            result += '{:>22}: {}\n'.format('message', 'NOT-ADDED')
        if self.isClosed:
            result += '======\nSTATE:\n======\n HealthDominoDataObject is already closed.\n'
        else:
            result += '======\nSTATE:\n======\n HealthDominoDataObject is not open for editing.\n'
        if self.isTransmitted:
            result += ' HealthDominoDataObject is already transmitted.\n'
            result += ' innerHash: {}\n'.format(self.innerHash)
            result += ' outerHash: {}'.format(self.outerHash)
        else:
            result += ' HealthDominoDataObject is not yet transmitted.\n'
        return result





class HDDOInitException(Exception):
    """
    This class is used to indicate HDDO creation specific errors.
    """

    pass



class HDDOPermissionException(Exception):
    """
    This class is used to indicate HDDO workflow specific errors.
    """

    pass
