# Copyright (C) July 2018:  TF TECH NV in Belgium see https://www.threefold.tech/
# In case TF TECH NV ceases to exist (e.g. because of bankruptcy)
#   then Incubaid NV also in Belgium will get the Copyright & Authorship for all changes made since July 2018
#   and the license will automatically become Apache v2 for all code related to Jumpscale & DigitalMe
# This file is part of jumpscale at <https://github.com/threefoldtech>.
# jumpscale is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# jumpscale is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License v3 for more details.
#
# You should have received a copy of the GNU General Public License
# along with jumpscale or jumpscale derived works.  If not, see <http://www.gnu.org/licenses/>.
# LICENSE END


from pyblake2 import blake2b
from Jumpscale import j


import struct
from .BCDBDecorator import *

JSBASE = j.application.JSBaseClass
INT_BIN_EMPTY = b"\xff\xff\xff\xff"  # is the empty value for in our key containers

# from .BCDBModelIndex import BCDBModelIndex
from .BCDBIndexMeta import BCDBIndexMeta


class BCDBModel(j.application.JSBaseClass):
    def __init__(self, bcdb, schema=None, reset=False):
        """

        delivers interface how to deal with data in 1 schema

        for query example see http://docs.peewee-orm.com/en/latest/peewee/query_examples.html

        e.g.
        ```
        query = self.index.name.select().where(index.cost > 0)
        for item in self.select(query):
            print(item.name)
        ```
        """

        JSBASE.__init__(self)

        # we should have a schema
        if not schema:
            if hasattr(self, "_SCHEMA"):  # schema when defined on the class itself
                schema = j.data.schema.get_from_text(self._SCHEMA)
            else:
                schema = self._schema_get()  # _schema_get is overrided by classes like ACL USER CIRCLE NAMESPACE
                if not schema:
                    j.exceptions.JSBUG("BCDB Model needs a schema object or text")
        else:
            if isinstance(schema, str):
                schema = j.data.schema.get_from_text(schema)
            else:  # schema must be a schema object
                assert schema.url

        assert isinstance(schema, j.data.schema.SCHEMA_CLASS)

        if self.schema.url in bcdb._schema_url_to_model:
            raise j.exceptions.JSBUG("should never have 2 bcdbmodels for same url")

        self.bcdb = bcdb

        self.readonly = False
        self.autosave = False  # if set it will make sure data is automatically set from object
        self.nosave = False

        if self.storclient and self.storclient.type == "ZDB":
            # is unique id for a bcdbmodel (unique per storclient !)
            self.key = "%s_%s" % (self.storclient.nsname, self.schema.url)
        else:
            self.key = self.schema.url
        self.key = self.key.replace(".", "_")

        self._data_dir = j.sal.fs.joinPaths(self.bcdb._data_dir, self.key)
        j.sal.fs.createDir(self._data_dir)

        self._kosmosinstance = None

        indexklass = self._index_class_generate()
        self.index = indexklass(bcdbmodel=self, reset=reset)

        self._sonic_client = None
        # self.cache_expiration = 3600

        self._triggers = []

        if reset:
            self.destroy()

    def _index_class_generate(self):
        """

        :param schema: is schema object j.data.schema... or text
        :return: class of the model which is used for indexing

        """
        self._log_debug("generate schema index:%s" % self.schema.url)

        # model with info to generate
        imodel = BCDBIndexMeta(schema=self.schema)
        imodel.include_schema = True
        tpath = "%s/templates/BCDBModelIndexClass.py" % j.data.bcdb._dirpath
        name = "bcdbindex_%s" % self.schema.url
        name = name.replace(".", "_")
        myclass = j.tools.jinja2.code_python_render(
            name=name, path=tpath, objForHash=self.schema._md5, reload=True, schema=self, bcdb=self.bcdb, index=imodel
        )

        return myclass

    @property
    def schema(self):
        return j.data.schema.get_from_url(self.schema.url)

    @property
    def mid(self):
        return self.bcdb.meta._mid_from_url(self.schema.url)

    def schema_change(self, schema):
        assert isinstance(schema, j.data.schema.SCHEMA_CLASS)
        # make sure model has the latest schema
        if self.schema._md5 != schema._md5:
            self.schema = schema
            self._triggers_call(None, "schema_change", None)

    @property
    def sonic_client(self):
        if not self._sonic_client:
            self._sonic_client = j.clients.sonic.get_client_bcdb()
        return self._sonic_client

    def _schema_get(self):
        return None

    @property
    def storclient(self):
        return self.bcdb.storclient

    def trigger_add(self, method):
        """
        see docs/baseclasses/data_mgmt_on_obj.md

        triggers are called with obj,action,propertyname as kwargs

        return obj or None

        :param method:
        :return:
        """
        if method not in self._triggers:
            self._triggers.append(method)

    def _triggers_call(self, obj, action=None, propertyname=None):
        """
        will go over all triggers and call them with arguments given
        see docs/baseclasses/data_mgmt_on_obj.md

        """
        model = self
        kosmosinstance = self._kosmosinstance
        for method in self._triggers:
            obj2 = method(model=model, obj=obj, kosmosinstance=kosmosinstance, action=action, propertyname=propertyname)
            if isinstance(obj2, j.data.schema._JSXObjectClass):
                # only replace if right one returned, otherwise ignore
                obj = obj2
            else:
                if obj2 is not None:
                    raise j.exceptions.Base("obj return from action needs to be a JSXObject or None")
        return obj

    # def cache_reset(self):
    #     self.obj_cache = {}

    @queue_method
    def index_ready(self):
        """
        doesn't do much, just makes sure that we wait that queue has been processed upto this point
        :return:
        """
        return True

    @queue_method
    def index_rebuild(self, nid=1):
        self.stop()
        self.index.destroy(nid=nid)
        self._log_warning("will rebuild index for:%s" % self)
        for obj in self.iterate(nid=nid):
            self.set(obj, store=False, index=True)

    @queue_method
    def delete(self, obj):
        if not isinstance(obj, j.data.schema._JSXObjectClass):
            if isinstance(obj, int):
                obj = self.get(obj)
            else:
                raise j.exceptions.Base("specify id or obj")
        assert obj.nid
        if obj.id is not None:
            self._triggers_call(obj=obj, action="delete")
            # if obj.id in self.obj_cache:
            #     self.obj_cache.pop(obj.id)
            if not self.storclient:
                self.bcdb.sqlclient.delete(key=obj.id)
            else:
                self.storclient.delete(obj.id)
            self.index.delete(obj)

    def check(self, obj):
        if not isinstance(obj, j.data.schema._JSXObjectClass):
            raise j.exceptions.Base("argument needs to be a jsx data obj")
        assert obj.nid

    @queue_method
    def set_dynamic(self, data, obj_id=None, nid=1):
        """
        if string -> will consider to be json
        if binary -> will consider data for capnp
        if obj -> will check of JSOBJ
        if ddict will put inside JSOBJ
        """
        if j.data.types.string.check(data):

            data = j.data.serializers.json.loads(data)
            if obj_id == None and "id" in data:
                obj_id = data["id"]
            if nid == None:
                if "nid" in data:
                    nid = data["nid"]
                else:
                    raise j.exceptions.Base("need to specify nid")
            obj = self.schema.new(datadict=data, bcdb=self.bcdb)
            obj.nid = nid
        elif j.data.types.bytes.check(data):
            obj = self.schema.new(serializeddata=data, bcdb=self.bcdb)
            if obj_id is None:
                raise j.exceptions.Base("objid cannot be None")
            if not obj.nid:
                if nid:
                    obj.nid = nid
                else:
                    raise j.exceptions.Base("need to specify nid")
        elif isinstance(data, j.data.schema._JSXObjectClass):
            obj = data
            if obj_id is None and obj.id is not None:
                obj_id = obj.id
            if not obj.nid:
                if nid:
                    obj.nid = nid
                else:
                    raise j.exceptions.Base("need to specify nid")
        elif j.data.types.dict.check(data):
            if obj_id == None and "id" in data:
                obj_id = data["id"]
            if "nid" not in data or not data["nid"]:
                if nid:
                    data["nid"] = nid
                else:
                    raise j.exceptions.Base("need to specify nid")
            obj = self.schema.new(datadict=data)
            obj.nid = nid
        else:
            raise j.exceptions.Base("Cannot find data type, str,bin,obj or ddict is only supported")
        if not obj.id:
            obj.id = obj_id  # do not forget
        return self.set(obj)

    def get_by_name(self, name, nid=1):
        args = {"name": name}
        return self.find(nid=nid, **args)

    def search(self, text, property_name=None):
        # FIXME: get the real nids
        objs = self.sonic_client.query(self.bcdb.name, "1:{}".format(self.mid), text)
        res = []
        for obj in objs:
            parts = obj.split(":")
            if (property_name and parts[1] == property_name) or (not property_name):
                res.append(self.get(parts[0]))
        return res

    def find(self, nid=1, **args):
        """
        is a the retrieval part of a very fast indexing system
        e.g.
        self.get_from_keys(name="myname",nid=2)
        :return:
        """
        delete_if_not_found = False
        # if no args are provided that mean we will do a get all
        if len(args.keys()) == 0:
            res = []
            for obj in self.iterate(nid=nid):
                if obj is None:
                    raise j.exceptions.Base("iterate should not return None, ever")
                res.append(obj)
            return res

        ids = self.index._key_index_find(nid=nid, **args)

        def check2(obj, args):
            dd = obj._ddict
            for propname, val in args.items():
                if not propname in dd:
                    raise j.exceptions.JSBUG(
                        "find was done on argument:%s which does not exist in model." % propname, data=obj
                    )
                if dd[propname] != val:
                    return False
            return True

        res = []
        for id_ in ids:
            res2 = self.get(id_, die=True)
            if res2 is None:
                if delete_if_not_found:
                    for key, val in args.items():
                        self._key_index_delete(key, val, id_, nid=nid)
            else:
                # we now need to check if there was no false positive
                if check2(res2, args):
                    res.append(res2)
                # else:
                #     self._log_warning("index system produced false positive")

        return res

    # @queue_method_results
    def set(self, obj, index=True, store=True):
        """
        :param obj
        :return: obj
        """
        self.check(obj)

        if store:

            # later:
            if obj.acl_id is None:
                obj.acl_id = 0

            if obj._acl is not None:
                if obj.acl.id is None:
                    # need to save the acl
                    obj.acl.save()
                else:
                    acl2 = obj._model.bcdb.acl.get(obj.acl.id)
                    if acl2 is None:
                        # means is not in db
                        obj.acl.save()
                    else:
                        if obj.acl.md5 != acl2.md5:
                            obj.acl.id = None
                            obj.acl.save()  # means there is acl but not same as in DB, need to save
                            self._obj_cache_reset()
                obj.acl_id = obj.acl.id

            try:
                bdata = obj._data
            except Exception as e:
                if str(e).find("has no such member") != -1:
                    msg = str(e).split("no such member", 1)[1].split("stack:")
                    raise j.exceptions.Base("Could not serialize capnnp message:%s" % msg)
                else:
                    raise e

            bdata_encrypted = j.data.nacl.default.encryptSymmetric(bdata)
            assert obj.nid > 0
            l = [obj.nid, obj.acl_id, bdata_encrypted]
            data = j.data.serializers.msgpack.dumps(l)

            obj = self._triggers_call(obj, action="set_pre")

            # PUT DATA IN DB
            if obj.id is None:
                # means a new one
                obj.id = self.storclient.set(data)
                # self._log_debug("NEW:\n%s" % obj)
            else:
                try:
                    self.storclient.set(data, key=obj.id)
                except Exception as e:
                    if str(e).find("only update authorized") != -1:
                        raise j.exceptions.Base("cannot update object:%s\n with id:%s, does not exist" % (obj, obj.id))
                    raise

        if index:
            self.index.set(obj)

        obj = self._triggers_call(obj=obj, action="set_post")

        return obj

    def _dict_process_out(self, ddict):
        """
        whenever dict is needed this method will be called before returning
        :param ddict:
        :return:
        """
        return ddict

    def _dict_process_in(self, ddict):
        """
        when data is inserted back into object
        :param ddict:
        :return:
        """
        return ddict

    def new(self, data=None, nid=1):
        if data and isinstance(data, dict):
            data = self._dict_process_in(data)
        elif j.data.types.json.check(str(data)):
            data = j.data.serializers.json.loads(data)

        if data:
            if isinstance(data, dict):
                obj = self.schema.new(datadict=data, bcdb=self.bcdb)
            elif isinstance(data, bytes):
                obj = self.schema.new(serializeddata=data, bcdb=self.bcdb)
            else:
                raise j.exceptions.Base("need dict")
        else:
            obj = self.schema.new(bcdb=self.bcdb)
        obj = self._methods_add(obj)
        obj.nid = nid
        obj = self._triggers_call(obj=obj, action="new")
        return obj

    def _methods_add(self, obj):
        return obj

    @queue_method_results
    def get(self, obj_id, return_as_capnp=False, usecache=True, die=True):
        """
        @PARAM id is an int or a key
        @PARAM capnp if true will return data as capnp binary object,
               no hook will be done !
        @RETURN obj    (.index is in obj)
        """

        if obj_id in [None, 0, "0", b"0"]:
            raise j.exceptions.Base("id cannot be None or 0")

        # if self.obj_cache is not None and usecache:
        #     # print("use cache")
        #     if obj_id in self.obj_cache:
        #         epoch, obj = self.obj_cache[obj_id]
        #         if j.data.time.epoch > self._cache_expiration + epoch:
        #             self.obj_cache.pop(obj_id)
        #             # print("dirty cache")
        #         else:
        #             # print("cache hit")
        #             return obj

        data = self.storclient.get(obj_id)

        if not data:
            if die:
                raise j.exceptions.Base("could not find obj with id:%s" % obj_id)
            else:
                return None

        obj = self.bcdb._unserialize(obj_id, data, return_as_capnp=return_as_capnp)

        if obj._schema.url == self.schema.url:
            obj = self._triggers_call(obj=obj, action="get")
        else:
            raise j.exceptions.Base("no object with id {} found in {}".format(obj_id, self))

        # self.obj_cache[obj_id] = (j.data.time.epoch, obj)  #FOR NOW NO CACHE, UNSAFE
        return obj

    def destroy(self, nid=1):
        self._log_warning("destroy: %s nid:%s" % (self, nid))
        assert isinstance(nid, int)
        assert nid > 0
        for obj_id in self.index._id_iterator(nid=nid):
            self.storclient.delete(obj_id)
        self.index.destroy()
        j.sal.fs.remove(self._data_dir)

    def iterate(self, nid=1):
        """
        walk over objects which are of type of this model
        """
        for obj_id in self.index._id_iterator(nid=nid):
            # self._log_debug("iterate:%s" % obj_id)
            assert obj_id > 0
            o = self.get(obj_id, die=False)
            if not o:
                continue
            yield o

    def _text_index_content_pre_(self, property_name, val, obj_id, nid=1):
        """ A hook to be called before setting to the full text index
        """
        return property_name, val, obj_id, nid

    def __str__(self):
        out = "model:%s\n" % self.schema.url
        # out += j.core.text.prefix("    ", self.schema.text)
        return out

    __repr__ = __str__
