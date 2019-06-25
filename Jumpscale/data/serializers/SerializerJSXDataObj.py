from Jumpscale import j
from .SerializerBase import SerializerBase


class SerializerJSXDataObj(SerializerBase):
    def __init__(self):
        SerializerBase.__init__(self)

    def dumps(self, obj, model=None, test=True):
        """
        obj is the dataobj for JSX

        j.data.serializers.jsxdata.dumps(..

        :param obj:
        :param test: if True will be slow !!!
        :return:
        """
        assert isinstance(obj, j.data.schema._JSXObjectClass)

        try:
            obj._cobj.clear_write_flag()
            data = obj._cobj.to_bytes_packed()
        except Exception as e:
            # need to catch exception much better (more narrow)
            obj._cobj_ = obj._cobj.as_builder()
            data = obj._cobj_.to_bytes_packed()

        if not model:
            version = 1
            data2 = version.to_bytes(1, "little") + bytes(bytearray.fromhex(obj._schema._md5)) + data
            j.core.db.hset(
                "debug1", obj._schema._md5, "%s:%s:%s" % (obj.id, obj._schema._md5, obj._schema.url)
            )  # DEBUG
        else:
            version = 10
            sid = obj._model.sid
            assert isinstance(sid, int)
            assert sid > 0
            data2 = version.to_bytes(1, "little") + sid.to_bytes(2, "little") + data
            j.core.db.hset("debug10", sid, "%s:%s:%s" % (obj.id, obj._schema._md5, obj._schema.url))  # DEBUG

        if test:
            # if not md5 in j.data.schema.md5_to_schema:
            self.loads(data=data2, model=model)

        return data2

    def loads(self, data, model=None):
        """
        j.data.serializers.jsxdata.loads(..
        :param data:
        :return: obj
        """
        versionnr = int.from_bytes(data[0:1], byteorder="little")
        if versionnr == 1:
            md5bin = data[1:17]
            md5 = md5bin.hex()
            data2 = data[17:]
            if md5 in j.data.schema.md5_to_schema:
                schema = j.data.schema.md5_to_schema[md5]
                obj = schema.new(capnpdata=data2, model=model)
                return obj
            else:
                j.shell()
                if not model:
                    raise RuntimeError("could not find schema with md5:%s, no model specified" % md5)
                j.shell()
                raise RuntimeError("could not find schema with md5:%s" % md5)
        elif versionnr == 10:
            sid = int.from_bytes(data[1:3], byteorder="little")
            data2 = data[3:]
            model2 = model.bcdb.model_get_from_sid(sid)  # weird concept but it could be we get other model based on sid
            return model2.schema.new(capnpdata=data2, model=model)
        else:
            raise RuntimeError("version wrong")
