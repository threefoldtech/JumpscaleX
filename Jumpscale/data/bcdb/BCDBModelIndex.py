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
# INT_BIN_EMPTY = b"\xff\xff\xff\xff"  # is the empty value for in our key containers


class BCDBModelIndex(j.application.JSBaseClass):
    def __init__(self, bcdbmodel, reset=False):
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

        self.bcdbmodel = bcdbmodel
        self.bcdb = bcdbmodel.bcdb
        self.schema = bcdbmodel.schema

        self._ids_redis_use = True  # let only use redis for now for the id's
        self._ids_redis = self.bcdb._redis_index
        self._ids_last = {}  # need to keep last id per namespace

        self.storclient = self.bcdb.storclient
        self._sonic = None

        self.readonly = self.bcdbmodel.readonly

        self._init_index()

        if reset:
            self.destroy()

    @property
    def sonic(self):
        if not self._sonic:
            self._sonic = j.clients.sonic.get_client_bcdb()
        return self._sonic

    def destroy(self, nid=None):
        """
        if nid is None will remove all namespaces indexes
        otherwise only remove indexing info for that specific namespace as identified by nid
        :param nid:
        :return:
        """
        self._key_index_destroy(nid=nid)
        self._ids_destroy(nid=nid)
        if j.sal.nettools.tcpPortConnectionTest("localhost", 1491):
            # means there is a sonic
            self._text_index_destroy_()
        else:
            self._log_warning("there was no sonic server active, could not delete the index")

    def set(self, obj):
        """
        create index with multiple methods for this object

        :param obj:
        :return:
        """
        self._sql_index_set(obj)
        self._key_index_set(obj)
        self._text_index_set(obj)
        assert obj.nid
        self._id_set(obj.id, nid=obj.nid)

    def delete(self, obj):
        """
        remove everything from index for this object
        :param obj:
        :return:
        """
        assert obj.nid
        if obj.id is not None:
            self._id_delete(obj.id)
            self._sql_index_delete(obj)
            self._key_index_delete(obj)
            self._text_index_delete(obj)

    ###### Full text indexing
    def _chunks(self, txt, length):
        if not txt:
            return None
        for i in range(0, len(txt), length):
            if i + length > len(txt):
                yield txt[i:]
            else:
                yield txt[i : i + length]

    def _clean_text_for_sonic(self, text):
        """
        cleaning the text and ignore json files and code blocks
        :param text: raw text to be indexed in sonic
        :return: clean text (str) or None
        """
        if not isinstance(text, str) or not text or text.startswith("{") or text.startswith("`"):
            return None
        else:
            return text.replace("\n", " ")

    def _text_index_keys_get_(self, property_name, val, obj_id, nid=1):
        """
        gets the keys to be used to index data to sonic:
        Collection: {BCDB_NAME}
        Bucket: {NAMESPACEID}:{SCHEMA_ID}
        Object: {obj_id}:{property_name}
        Data: {value}
        """
        if val:
            return (
                self.bcdb.name,
                "{}:{}".format(nid, self.bcdbmodel.sid),
                "{}:{}".format(obj_id, property_name),
                self._clean_text_for_sonic(val),
            )
        else:
            return self.bcdb.name, "{}:{}".format(nid, self.bcdbmodel.sid), "{}:{}".format(obj_id, property_name)

    def _text_index_set_(self, property_name, val, obj_id, nid=1):
        args = self.bcdbmodel._text_index_content_pre_(property_name, val, obj_id, nid)
        bucket, collection, object_tag, text = self._text_index_keys_get_(*args)
        for chunk in self._chunks(text, int(self.sonic.bufsize) // 2):
            self.sonic.push(bucket, collection, object_tag, chunk)

    def _text_index_delete_(self, property_name, val, obj_id, nid=1):
        keys = self._text_index_keys_get_(property_name, None, obj_id, nid)
        self.sonic.flush_object(*keys)

    def _text_index_destroy_(self):
        self.sonic.flush(self.bcdb.name)

    ###### INDEXER ON KEYS:

    def _key_index_hsetkey_get(self, nid=1):
        """
        :param namespaceid: default is 1 namespace = 1
        :return: hset key for the storing the index in redis

        use as

        key = self._key_index_hsetkey_get(nid)

        """
        return "bcdb:%s:%s:%s:index" % (self.bcdb.name, nid, self.bcdbmodel.sid)

    def _key_index_set_(self, property_name, val, obj_id, nid=1):
        """

        :param property_name: property name to index
        :param val: the value of the property which we want to index
        :param obj_id: id of the obj
        :return:
        """
        key = "%s__%s" % (property_name, val)
        ids = self._key_index_getids(key, nid=nid)
        if obj_id is None:
            raise j.exceptions.Base("id cannot be None")
        if obj_id not in ids:
            ids.append(obj_id)
        data = j.data.serializers.msgpack.dumps(ids)
        hash = self._key_index_redis_get(key)  # this to have a smaller key to store in mem
        self._log_debug("set key:%s (id:%s)" % (key, obj_id))
        j.clients.credis_core.hset(self._key_index_hsetkey_get(nid=nid).encode() + b":" + hash[0:2], hash[2:], data)

    def _key_index_delete_(self, property_name, val, obj_id, nid=1):
        assert nid
        key = "%s__%s" % (property_name, val)
        ids = self._key_index_getids(key, nid=nid)
        if obj_id is None:
            raise j.exceptions.Base("id cannot be None")
        if obj_id in ids:
            ids.pop(ids.index(obj_id))
        hash = self._key_index_redis_get(key)
        if ids == []:
            j.clients.credis_core.hdel(self._key_index_hsetkey_get(nid=nid).encode() + b":" + hash[0:2], hash[2:])
        else:
            data = j.data.serializers.msgpack.dumps(ids)
            hash = self._key_index_redis_get(key)
            self._log_debug("set key:%s (id:%s)" % (key, obj_id))
            j.clients.credis_core.hset(self._key_index_hsetkey_get(nid=nid).encode() + b":" + hash[0:2], hash[2:], data)

    def _key_index_destroy(self, nid=1):

        k = self._key_index_hsetkey_get(nid=nid) + ":*"
        for key in j.clients.credis_core.keys(k):
            j.clients.credis_core.delete(key)

    def _key_index_getids(self, key, nid=1):
        """
        return all the id's which are already in redis
        :param key:
        :return: [] if not or the id's which are relevant for this namespace
        """

        hash = self._key_index_redis_get(key)

        r = j.clients.credis_core.hget(self._key_index_hsetkey_get(nid=nid).encode() + b":" + hash[0:2], hash[2:])
        if r is not None:
            # means there is already one
            self._log_debug("get key(exists):%s" % key)
            ids = j.data.serializers.msgpack.loads(r)

        else:
            self._log_debug("get key(new):%s" % key)
            ids = []
        return ids

    def _key_index_redis_get(self, key):
        """
        returns 10 bytes as key (non HR readable)
        :param key:
        :return:
        """
        # schema id needs to be in to make sure its different key per schema
        key2 = key + str(self.schema._md5)
        # can do 900k per second
        hash = blake2b(str(key2).encode(), digest_size=10).digest()
        return hash

    # def get_id_from_key(self, key):
    #     """
    #
    #     :param sid: schema id
    #     :param key: key used to store
    #     :return:
    #     """
    #     ids = self._key_index_getids(key,nid=nid)
    #     if len(ids) == 1:
    #         return ids[0]
    #     elif len(ids) > 1:
    #         # need to fetch obj to see what is alike
    #         j.shell()

    def _key_index_find(self, delete_if_not_found=False, nid=1, **args):
        """
        find the possible candidates (id's only)
        e.g.
        self._key_index_find(name="myname",nid=2)
        :return:
        """
        if len(args.keys()) == 0:
            raise j.exceptions.Base("get from keys need arguments")
        ids_prev = []
        ids = []
        for propname, val in args.items():
            key = "%s__%s" % (propname, val)
            ids = self._key_index_getids(key, nid=nid)
            if ids_prev != []:
                ids = [x for x in ids if x in ids_prev]
            ids_prev = ids

        return ids

    ##### ID METHODS, this allows us to see which id's are in which namespace

    def _id_redis_listkey_get(self, nid=1):
        """
        :param namespaceid: default is 1 namespace = 1
        :return: list key for the storing the id's in redis

        use as

        key = self._id_redis_listkey_get(nid)

        """
        return "bcdb:%s:%s:%s:ids" % (self.bcdb.name, nid, self.bcdbmodel.sid)

    def _ids_destroy(self, nid=1):
        self._ids_redis.delete(self._id_redis_listkey_get(nid=nid))

    def _ids_init(self, nid=1):
        """
        we keep track of id's per namespace and per model, this to allow easy enumeration
        :return:
        """

        if nid not in self._ids_last:
            if self._ids_redis_use:
                r = self._ids_redis
                self._ids_last[nid] = 0
                redis_list_key = self._id_redis_listkey_get(nid)
                chunk = r.lindex(redis_list_key, -1)  # get the last element, works because its an ordered list
                if not chunk:
                    # means we don't have the list yet
                    self._ids_last[nid] = 0
                else:
                    last = struct.unpack("<I", chunk)[0]
                    self._ids_last[nid] = last  # need to know the last one
            else:
                raise j.exceptions.Base("needs to be 100% checked")
                # next one always happens
                ids_file_path = "%s/ids_%s.data" % (nid, self._data_dir)
                if not j.sal.fs.exists(ids_file_path) or j.sal.fs.fileSize(ids_file_path) == 0:
                    j.sal.fs.touch(ids_file_path)
                    self._ids_last[nid] = 0
                else:
                    llen = j.sal.fs.fileSize(ids_file_path)
                    # make sure the len is multiplication of 4 bytes
                    assert float(llen / 4) == llen / 4
                    f = open(ids_file_path, "rb")
                    f.seek(llen - 4, 0)
                    bindata = f.read(4)
                    self._ids_last[nid] = struct.unpack(b"<I", bindata)[0]
                    f.close()

    def _id_set(self, id, nid=1):
        self._ids_init(nid=nid)
        bin_id = struct.pack("<I", id)
        if id > self._ids_last[nid]:
            if self._ids_redis_use:
                r = self._ids_redis
                redis_list_key = self._id_redis_listkey_get(nid)
                r.rpush(redis_list_key, bin_id)
            else:
                # this allows us to know which objects are in a specific model namespace, otherwise we cannot iterate
                ids_file_path = "%s/ids_%s.data" % (nid, self._data_dir)
                j.sal.fs.writeFile(ids_file_path, bin_id, append=True)
            self._ids_last[nid] = id

    def _id_iterator(self, nid=1):
        """
        if nid==None then will iterate over all namespaces

        ```
        for obj_id in m.id_iterator:
            o=m.get(obj_id)
        ```
        :return:
        """
        self._ids_init(nid=nid)
        if self._ids_redis_use:
            r = self._ids_redis
            if nid is None:
                for nid in r.keys("bcdb:%s:*" % (self.bcdb.name)):
                    self._id_iterator(nid=nid)
            redis_list_key = self._id_redis_listkey_get(nid)
            l = r.llen(redis_list_key)
            if l > 0:
                for i in range(0, l):
                    obj_id = self._id_get_objid_redis(i, nid=nid)
                    # print(obj_id)
                    yield obj_id

            else:
                # IS TOO HARSH NEED TO FIND OTHER SOLUTION FOR IT
                self._log_warning(
                    "iterator was empty for bcdb:%s, will rebuild from backend, IS DANGEROUS" % self.bcdb.name
                )
                for obj in list(self.bcdb.get_all()):
                    if obj._schema.url == self.schema.url:
                        self.set(obj)
                        yield obj.id

        else:
            ids_file_path = "%s/ids_%s.data" % (nid, self._data_dir)
            # print("idspath:%s"%ids_file_path)
            with open(ids_file_path, "rb") as f:
                while True:
                    chunk = f.read(4)
                    if chunk:
                        obj_id = struct.unpack("<I", chunk)[0]
                        yield obj_id
                    else:
                        break

    def _id_get_objid_redis(self, pos, nid=1, die=True):
        r = self._ids_redis
        chunk = r.lindex(self._id_redis_listkey_get(nid=nid), pos)
        if not chunk:
            if die:
                raise j.exceptions.Base("should always get something back?")
            return None
        return struct.unpack("<I", chunk)[0]

    def _id_delete(self, id, nid=1):
        self._ids_init(nid=nid)
        if self._ids_redis_use:
            id = int(id)
            r = self._ids_redis
            bin_id = struct.pack("<I", id)
            redis_list_key = self._id_redis_listkey_get(nid)
            # should remove all redis elements of the list with this id
            r.execute_command("LREM", redis_list_key, 0, bin_id)
        else:
            ids_file_path = "%s/ids_%s.data" % (nid, self._data_dir)
            out = b""
            for id_ in self._id_iterator:
                if id_ != id:
                    out += struct.pack("<I", id_)
            j.sal.fs.writeFile(ids_file_path, out)

    def _id_exists(self, id, nid=1):
        """ 
        Check if an object eist based on its id 
        TODO: Improve it with a binary search 
        """
        self._ids_init(nid=nid)

        if self._ids_redis_use:
            id = int(id)
            r = self._ids_redis
            redis_list_key = self._id_redis_listkey_get(nid)
            l = r.llen(redis_list_key)
            if l > 0:
                last_id = self._id_get_objid_redis(-1, nid=nid)
                # this gives me an estimate where to look for the info in the list
                trypos = int(l / last_id * id)
                if trypos == last_id:
                    potentialid = self._id_get_objid_redis(trypos, die=False, nid=nid)
                if not potentialid:
                    raise j.exceptions.Base("can't get a model from data:%s" % bdata)
                elif potentialid == id:
                    # lucky
                    return True
                elif potentialid is None or potentialid > id:
                    # walk back
                    for i in range(trypos, 0, -1):
                        potentialid = self._id_get_objid_redis(i, nid=nid)
                        if potentialid == id:
                            return True
                        if potentialid < id:
                            return False  # we're already too low
                elif potentialid < id:
                    # walk forward
                    for i in range(0, trypos):
                        potentialid = self._id_get_objid_redis(i, nid=nid)
                        if potentialid == id:
                            return True
                        if potentialid > id:
                            return False  # we're already too high
                else:
                    raise j.exceptions.Base("did not find, should not get here")

                return False
        else:
            ids_file_path = "%s/ids_%s.data" % (nid, self._data_dir)
            raise j.exceptions.Base("not implemented yet")

    def __str__(self):
        out = "modelindex:%s\n" % self.schema.url
        return out

    __repr__ = __str__
