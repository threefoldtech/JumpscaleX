from Jumpscale import j

_CONDITION_TYPE_NIL = 0
_CONDITION_TYPE_UNLOCK_HASH = 1
_CONDITION_TYPE_ATOMIC_SWAP = 2
_CONDITION_TYPE_LOCKTIME = 3
_CONDITION_TYPE_MULTI_SIG = 4

class ConditionFactory(j.application.JSBaseClass):
    """
    Condition Factory class
    """

    def from_json(self, obj):
        ct = obj.get('type', 0)
        if ct == _CONDITION_TYPE_NIL:
            return ConditionNil.from_json(obj)
        if ct == _CONDITION_TYPE_UNLOCK_HASH:
            return ConditionUnlockHash.from_json(obj)
        if ct == _CONDITION_TYPE_ATOMIC_SWAP:
            return ConditionAtomicSwap.from_json(obj)
        if ct == _CONDITION_TYPE_LOCKTIME:
            return ConditionLockTime.from_json(obj)
        if ct == _CONDITION_TYPE_MULTI_SIG:
            return ConditionMultiSignature.from_json(obj)
        raise ValueError("unsupport condition type {}".format(ct))


    def nil_new(self):
        """
        Create a new Nil Condition, which can be fulfilled by any SingleSig. Fulfillment.
        """
        return ConditionNil()

    def unlockhash_new(self, unlockhash=None):
        """
        Create a new UnlockHash Condition, which can be
        fulfilled by the matching SingleSig. Fulfillment.
        """
        return ConditionUnlockHash(unlockhash=unlockhash)

    def atomicswap_new(self, sender=None, receiver=None, hashed_secret=None, lock_time=0):
        """
        Create a new AtomicSwap Condition, which can be
        fulfilled by the AtomicSwap Fulfillment.
        """
        return ConditionAtomicSwap(
            sender=sender, receiver=receiver,
            hashed_secret=hashed_secret, lock_time=lock_time)

    def locktime_new(self, lock_time=0, condition=None):
        """
        Create a new LockTime Condition, which can be fulfilled by a fulfillment
        when the relevant timestamp/block has been reached as well as the fulfillment fulfills the internal condition.
        """
        return ConditionLockTime(locktime=lock_time, condition=condition)

    def multi_signature_new(self, min_nr_sig=0, unlockhashes=None):
        """
        Create a new MultiSignature Condition, which can be fulfilled by a matching MultiSignature Fulfillment.
        """
        return ConditionMultiSignature(unlockhashes=unlockhashes, min_nr_sig=min_nr_sig)


    def test(self):
        """
        js_shell 'j.clients.tfchain.types.conditions.test()'
        """

        # some util test methods
        def test_encoded(encoder, obj, expected):
            encoder.add(obj)
            output = encoder.data.hex()
            if expected != output:
                msg = "{} != {}".format(expected, output)
                raise Exception("unexpected encoding result: " + msg)
        def test_sia_encoded(obj, expected):
            test_encoded(j.data.rivine.encoder_sia_get(), obj, expected)
        def test_rivine_encoded(obj, expected):
            test_encoded(j.data.rivine.encoder_rivine_get(), obj, expected)


        # Nil conditions are supported
        for n_json in [{}, {"type": 0}, {"type": 0, "data": None}, {"type": 0, "data": {}}]:
            cn = self.from_json(n_json)
            assert cn.json() == {"type": 0}
            test_sia_encoded(cn, '000000000000000000')
            test_rivine_encoded(cn, '0000')

        # UnlockHash conditions are supported
        uh_json = {"type":1,"data":{"unlockhash":"000000000000000000000000000000000000000000000000000000000000000000000000000000"}}
        cuh = self.from_json(uh_json)
        assert cuh.json() == uh_json
        test_sia_encoded(cuh, '012100000000000000000000000000000000000000000000000000000000000000000000000000000000')
        test_rivine_encoded(cuh, '0142000000000000000000000000000000000000000000000000000000000000000000')

        # AtomicSwap conditions are supported
        as_json = {"type":2,"data":{"sender":"01e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f70b1ccc65e2105","receiver":"01a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc353bdcf54be7d8","hashedsecret":"abc543defabc543defabc543defabc543defabc543defabc543defabc543defa","timelock":1522068743}}
        cas = self.from_json(as_json)
        assert cas.json() == as_json
        test_sia_encoded(cas, '026a0000000000000001e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35abc543defabc543defabc543defabc543defabc543defabc543defabc543defa07edb85a00000000')
        test_rivine_encoded(cas, '02d401e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35abc543defabc543defabc543defabc543defabc543defabc543defabc543defa07edb85a00000000')

        # MultiSig conditions are supported
        ms_json = {"type":4,"data":{"unlockhashes":["01e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f70b1ccc65e2105","01a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc353bdcf54be7d8"],"minimumsignaturecount":2}}
        cms = self.from_json(ms_json)
        assert cms.json() == ms_json
        test_sia_encoded(cms, '0452000000000000000200000000000000020000000000000001e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35')
        test_rivine_encoded(cms, '049602000000000000000401e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35')

        # LockTime conditions are supported:
        # - wrapping a nil condition
        lt_n_json = {"type":3,"data":{"locktime":500000000,"condition":{"type": 0}}}
        clt_n = self.from_json(lt_n_json)
        assert clt_n.json() == lt_n_json
        test_sia_encoded(clt_n, '0309000000000000000065cd1d0000000000')
        test_rivine_encoded(clt_n, '03120065cd1d0000000000')
        # - wrapping an unlock hash condition
        lt_uh_json = {"type":3,"data":{"locktime":500000000,"condition":uh_json}}
        clt_uh = self.from_json(lt_uh_json)
        assert clt_uh.json() == lt_uh_json
        test_sia_encoded(clt_uh, '032a000000000000000065cd1d0000000001000000000000000000000000000000000000000000000000000000000000000000')
        test_rivine_encoded(clt_uh, '03540065cd1d0000000001000000000000000000000000000000000000000000000000000000000000000000')
        # - wrapping a multi-sig condition
        lt_ms_json = {"type":3,"data":{"locktime":500000000,"condition":ms_json}}
        clt_ms = self.from_json(lt_ms_json)
        assert clt_ms.json() == lt_ms_json
        test_sia_encoded(clt_ms, '035b000000000000000065cd1d00000000040200000000000000020000000000000001e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35')
        test_rivine_encoded(clt_ms, '03a80065cd1d000000000402000000000000000401e89843e4b8231a01ba18b254d530110364432aafab8206bea72e5a20eaa55f7001a6a6c5584b2bfbd08738996cd7930831f958b9a5ed1595525236e861c1a0dc35')


from abc import abstractmethod

from .BaseDataType import BaseDataTypeClass

class ConditionBaseClass(BaseDataTypeClass):
    @classmethod
    def from_json(cls, obj):
        ff = cls()
        assert ff.type == obj.get('type', 0)
        ff.from_json_data_object(obj.get('data', {}))
        return ff

    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def from_json_data_object(self, data):
        pass

    @abstractmethod
    def json_data_object(self):
        pass

    def json(self):
        obj = {'type': self.type}
        data = self.json_data_object()
        if data:
            obj['data'] = data
        return obj

    @abstractmethod
    def sia_binary_encode_data(self, encoder):
        pass

    def sia_binary_encode(self, encoder):
        """
        Encode this Condition according to the Sia Binary Encoding format.
        """
        encoder.add_array(bytearray([int(self.type)]))
        data_enc = j.data.rivine.encoder_sia_get()
        self.sia_binary_encode_data(data_enc)
        encoder.add_slice(data_enc.data)

    @abstractmethod
    def rivine_binary_encode_data(self, encoder):
        pass
    
    def rivine_binary_encode(self, encoder):
        """
        Encode this Condition according to the Rivine Binary Encoding format.
        """
        encoder.add_int8(int(self.type))
        data_enc = j.data.rivine.encoder_rivine_get()
        self.rivine_binary_encode_data(data_enc)
        encoder.add_slice(data_enc.data)


class ConditionNil(ConditionBaseClass):
    """
    ConditionNil class
    """

    @property
    def type(self):
        return _CONDITION_TYPE_NIL

    def from_json_data_object(self, data):
        assert data in (None, {})

    def json_data_object(self):
        return None
    
    def sia_binary_encode_data(self, encoder):
        pass # nothing to do

    def rivine_binary_encode_data(self, encoder):
        pass # nothing to do


from enum import IntEnum

class UnlockHashType(IntEnum):
    NIL = 0
    PUBLIC_KEY = 1
    ATOMIC_SWAP = 2
    MULTI_SIG = 3

    @classmethod
    def from_json(cls, obj):
        if type(obj) is str:
            obj = int(obj)
        else:
            assert type(obj) is int
        return cls(obj) # int -> enum

    def json(self):
        return int(self)


class UnlockHash(BaseDataTypeClass):
    """
    An UnlockHash is a specially constructed hash of the UnlockConditions type,
    with a fixed binary length of 33 and a fixed string length of 78 (string version includes a checksum).
    """

    _TYPE_SIZE_HEX = 2
    _CHECKSUM_SIZE = 6
    _CHECKSUM_SIZE_HEX = (_CHECKSUM_SIZE*2)
    _HASH_SIZE = 32
    _HASH_SIZE_HEX = (_HASH_SIZE*2)
    _TOTAL_SIZE_HEX = _TYPE_SIZE_HEX + _CHECKSUM_SIZE_HEX + _HASH_SIZE_HEX

    def __init__(self, type=None, hash=None):
        self._type = UnlockHashType.NIL
        self.type = type
        self._hash = j.clients.tfchain.types.hash_new()
        self.hash = hash

    @classmethod
    def from_json(cls, obj):
        assert type(obj) is str
        assert len(obj) == UnlockHash._TOTAL_SIZE_HEX

        t = UnlockHashType(int(obj[:UnlockHash._TYPE_SIZE_HEX]))
        h = j.clients.tfchain.types.hash_new(value=obj[UnlockHash._TYPE_SIZE_HEX:UnlockHash._TYPE_SIZE_HEX+UnlockHash._HASH_SIZE_HEX])
        uh = cls(type=t, hash=h)
        
        if t == UnlockHashType.NIL:
            assert h.value == (b'\x00'*UnlockHash._HASH_SIZE)
        else:
            expected_checksum = uh._checksum()[:UnlockHash._CHECKSUM_SIZE].hex()
            checksum = obj[-UnlockHash._CHECKSUM_SIZE_HEX:]
            assert expected_checksum == checksum

        return uh
    
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        if value == None:
            value = UnlockHashType.NIL
        else:
            assert isinstance(value, UnlockHashType)
        self._type = value

    @property
    def hash(self):
        return self.hash
    @hash.setter
    def hash(self, value):
        self._hash.value = value

    def __str__(self):
        checksum = self._checksum()[:UnlockHash._CHECKSUM_SIZE].hex()
        return "{}{}{}".format(bytearray([int(self._type)]).hex(), self._hash.value.hex(), checksum)

    def _checksum(self):
        if self._type == UnlockHashType.NIL:
            return b'\x00'*UnlockHash._CHECKSUM_SIZE
        e = j.data.rivine.encoder_rivine_get()
        e.add_int8(int(self._type))
        e.add(self._hash)
        return bytearray.fromhex(j.data.hash.blake2_string(e.data))

    __repr__ = __str__

    json = __str__

    def sia_binary_encode(self, encoder):
        """
        Encode this unlock hash according to the Sia Binary Encoding format.
        """
        encoder.add_byte(int(self._type))
        encoder.add(self._hash)
    
    def rivine_binary_encode(self, encoder):
        """
        Encode this unlock hash according to the Rivine Binary Encoding format.
        """
        encoder.add_int8(int(self._type))
        encoder.add(self._hash)


class ConditionUnlockHash(ConditionBaseClass):
    """
    ConditionUnlockHash class
    """
    def __init__(self, unlockhash=None):
        self._unlockhash = UnlockHash()

    @property
    def type(self):
        return _CONDITION_TYPE_UNLOCK_HASH

    @property
    def unlockhash(self):
        return self._unlockhash
    @unlockhash.setter
    def unlockhash(self, value):
        if not value:
            self._unlockhash = UnlockHash()
        else:
            assert isinstance(value, UnlockHash)
            assert value.type in (UnlockHashType.PUBLIC_KEY, UnlockHashType.NIL)
            self._unlockhash = value

    def from_json_data_object(self, data):
        self.unlockhash = UnlockHash.from_json(data['unlockhash'])

    def json_data_object(self):
        return {
            'unlockhash': self._unlockhash.json(),
        }
    
    def sia_binary_encode_data(self, encoder):
        encoder.add(self._unlockhash)

    def rivine_binary_encode_data(self, encoder):
        encoder.add(self._unlockhash)


class ConditionAtomicSwap(ConditionBaseClass):
    """
    ConditionAtomicSwap class
    """
    # TODO: replace lock_time with a user_friendly option that can define durations in a more human-readable way
    def __init__(self, sender=None, receiver=None, hashed_secret=None, lock_time=0):
        self._sender = UnlockHash()
        self.sender = sender
        self._receiver = UnlockHash()
        self.receiver = receiver
        self._hashed_secret = j.clients.tfchain.types.binary_data_new()
        self.hashed_secret = hashed_secret
        self._lock_time = 0
        self.lock_time = lock_time

    @property
    def type(self):
        return _CONDITION_TYPE_ATOMIC_SWAP

    @property
    def sender(self):
        return self._sender
    @sender.setter
    def sender(self, value):
        if not value:
            self._sender = UnlockHash()
        else:
            assert isinstance(value, UnlockHash)
            assert value.type in (UnlockHashType.PUBLIC_KEY, UnlockHashType.NIL)
            self._sender = value

    @property
    def receiver(self):
        return self._receiver
    @receiver.setter
    def receiver(self, value):
        if not value:
            self._receiver = UnlockHash()
        else:
            assert isinstance(value, UnlockHash)
            assert value.type in (UnlockHashType.PUBLIC_KEY, UnlockHashType.NIL)
            self._receiver = value
    
    @property
    def hashed_secret(self):
        return self._hashed_secret
    @hashed_secret.setter
    def hashed_secret(self, value):
        if not value:
            self._hashed_secret = j.clients.tfchain.types.binary_data_new()
        else:
            if type(value) is type(self._hashed_secret):
                self._hashed_secret = value
            else:
                self._hashed_secret.value = value

    @property
    def lock_time(self):
        return self._lock_time
    @lock_time.setter
    def lock_time(self, value):
        if not value:
            self._lock_time = 0
        else:
            assert isinstance(value, int)
            self._lock_time = int(value)

    def from_json_data_object(self, data):
        self.sender = UnlockHash.from_json(data['sender'])
        self.receiver = UnlockHash.from_json(data['receiver'])
        self.hashed_secret = j.clients.tfchain.types.binary_data_new(value=data['hashedsecret'])
        self.lock_time = int(data['timelock'])

    def json_data_object(self):
        return {
            'sender': self._sender.json(),
            'receiver': self._receiver.json(),
            'hashedsecret': self._hashed_secret.json(),
            'timelock': self._lock_time,
        }

    def sia_binary_encode_data(self, encoder):
        encoder.add_all(self._sender, self._receiver)
        encoder.add_array(self._hashed_secret.value)
        encoder.add(self.lock_time)

    def rivine_binary_encode_data(self, encoder):
        encoder.add_all(self._sender, self._receiver)
        encoder.add_array(self._hashed_secret.value)
        encoder.add(self.lock_time)


class ConditionLockTime(ConditionBaseClass):
    """
    ConditionLockTime class
    """
    # TODO: replace lock_time with a user_friendly option that can define durations in a more human-readable way
    def __init__(self, condition=None, locktime=0):
        self._condition = ConditionUnlockHash()
        self.condition = condition
        self._lock_time = 0
        self.locktime = locktime

    @property
    def type(self):
        return _CONDITION_TYPE_LOCKTIME

    @property
    def condition(self):
        return self._condition
    @condition.setter
    def condition(self, value):
        if not value:
            self._condition = ConditionUnlockHash()
        else:
            assert isinstance(value, ConditionBaseClass)
            self._condition = value

    @property
    def lock_time(self):
        return self._lock_time
    @lock_time.setter
    def lock_time(self, value):
        if not value:
            self._lock_time = 0
        else:
            assert isinstance(value, int)
            self._lock_time = int(value)

    def from_json_data_object(self, data):
        self.lock_time = int(data['locktime'])
        cond = j.clients.tfchain.types.conditions.from_json(obj=data['condition'])
        assert cond.type in(_CONDITION_TYPE_UNLOCK_HASH, _CONDITION_TYPE_MULTI_SIG, _CONDITION_TYPE_NIL)
        self._condition = cond

    def json_data_object(self):
        return {
            'locktime': self._lock_time,
            'condition': self._condition.json(),
        }

    def sia_binary_encode_data(self, encoder):
        encoder.add(self._lock_time)
        encoder.add_array(bytearray([int(self._condition.type)]))
        self._condition.sia_binary_encode_data(encoder)

    def rivine_binary_encode_data(self, encoder):
        encoder.add(self._lock_time)
        encoder.add_int8(int(self._condition.type))
        self._condition.rivine_binary_encode_data(encoder)

class ConditionMultiSignature(ConditionBaseClass):
    """
    ConditionMultiSignature class
    """
    # TODO: replace lock_time with a user_friendly option that can define durations in a more human-readable way
    def __init__(self, unlockhashes=None, min_nr_sig=0):
        self._unlockhashes = []
        if unlockhashes:
            for uh in unlockhashes:
                self.add_unlockhash(uh)
        self._min_nr_sig = 0
        self.required_signatures = min_nr_sig

    @property
    def type(self):
        return _CONDITION_TYPE_MULTI_SIG

    @property
    def unlockhashes(self):
        return self._unlockhashes
        
    def add_unlockhash(self, uh):
        if not uh:
            self._unlockhashes.append(UnlockHash())
        else:
            assert isinstance(uh, UnlockHash)
            self._unlockhashes.append(uh)

    @property
    def required_signatures(self):
        return self._min_nr_sig
    @required_signatures.setter
    def required_signatures(self, value):
        if not value:
            self._min_nr_sig = 0
        else:
            assert isinstance(value, int)
            self._min_nr_sig = int(value)

    def from_json_data_object(self, data):
        self._min_nr_sig = int(data['minimumsignaturecount'])
        self._unlockhashes = []
        for uh in data['unlockhashes']:
            uh = UnlockHash.from_json(uh)
            self._unlockhashes.append(uh)

    def json_data_object(self):
        return {
            'minimumsignaturecount': self._min_nr_sig,
            'unlockhashes': [uh.json() for uh in self._unlockhashes],
        }

    def sia_binary_encode_data(self, encoder):
        encoder.add(self._min_nr_sig)
        encoder.add_slice(self._unlockhashes)

    def rivine_binary_encode_data(self, encoder):
        encoder.add_int64(self._min_nr_sig)
        encoder.add_slice(self._unlockhashes)
