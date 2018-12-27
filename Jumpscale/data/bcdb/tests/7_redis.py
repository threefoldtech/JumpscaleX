from Jumpscale import j

import redis


def main(self):
    """
    to run:

    js_shell 'j.data.bcdb.test(name="redis")'

    use a bcdb which is using sqlite

    REQUIREMENTS:

    ```
    apt-get install python3.6-dev
    mkdir -p /root/opt/bin
    js_shell 'j.servers.zdb.build()'
    pip3 install pycapnp peewee cryptocompare

    #MAKE SURE YOU DON't USE THE SSH CONFIG, USE THE LOCAL CONFIG
    js_shell 'j.tools.myconfig'

    ```


    """

    # TODO: need to use prefab to check the prerequisites are installed if not DO

    def do(zdb=False):

        j.sal.nettools.waitConnectionTest(
            "127.0.0.1", port=6380, timeoutTotal=20)

        redis_cl = j.clients.redis.get(ipaddr="localhost", port=6380)

        schema = """
        @url = despiegk.test2
        llist2 = "" (LS)
        name* = ""
        email* = ""
        nr* = 0
        date_start* = 0 (D)
        description = ""
        token_price* = "10 USD" (N)
        cost_estimate:hw_cost = 0.0 #this is a comment
        llist = []
        llist3 = "1,2,3" (LF)
        llist4 = "1,2,3" (L)
        """
        schema = j.core.text.strip(schema)
        self._logger.debug("set schema to 'despiegk.test2'")
        redis_cl.set("schemas:despiegk.test2", schema)
        self._logger.debug('compare schema')
        schema2 = redis_cl.get("schemas:despiegk.test2")
        # test schemas are same

        assert _compare_strings(schema, schema2)

        self._logger.debug("delete data")
        # removes the data mainly tested on sqlite db now
        redis_cl.delete("objects:despiegk.test2")

        self._logger.debug('there should be 0 objects')
        assert redis_cl.hlen("objects:despiegk.test2") == 0

        schema = j.data.schema.get(schema)

        self._logger.debug("add objects")

        def get_obj(i):
            schema_obj = schema.new()
            schema_obj.nr = i
            schema_obj.name = "somename%s" % i
            schema_obj.token_price = "10 EUR"
            return schema_obj

        try:
            schema_obj = get_obj(0)
            id = redis_cl.hset("objects:despiegk.test2", 0, schema_obj._json)
            raise RuntimeError(
                "should have raise runtime error when trying to write to index 0")
        except redis.exceptions.ResponseError as err:
            # runtime error is expected when trying to write to index 0
            pass

        for i in range(1, 11):
            print(i)
            o = get_obj(i)
            id = redis_cl.hset("objects:despiegk.test2", "new", o._json)

        if zdb:
            self._logger.debug("validate list")
            cl = j.clients.zdb.client_get()
            assert cl.list() == [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        id = int(id.decode())

        self._logger.debug("validate added objects")
        # there should be 10 items now there
        assert redis_cl.hlen("objects:despiegk.test2") == 10
        assert redis_cl.hdel("objects:despiegk.test2", 5) == 1
        assert redis_cl.hlen("objects:despiegk.test2") == 9
        assert redis_cl.hget("objects:despiegk.test2", 5) is None
        assert redis_cl.hget("objects:despiegk.test2", 5) == redis_cl.hget(
            "objects:despiegk.test2", "5")

        if zdb:
            self._logger.debug("validate list2")
            assert cl.list() == [0, 2, 3, 4, 6, 7, 8, 9, 10, 11]

        # the i's are moving around don't know why, is ok I guess (despiegk)
        resp = redis_cl.hget("objects:despiegk.test2", id)
        json = j.data.serializers.json.loads(resp)
        json2 = j.data.serializers.json.loads(o._ddict_json)
        json2['id'] = id

        assert json == json2

        self._logger.debug("update obj")
        o.name = "UPDATE"
        ret = redis_cl.hset("objects:despiegk.test2", id, o._json)
        assert id == int(ret.decode())  # checks right id is returned

        resp = redis_cl.hget("objects:despiegk.test2", id)
        json3 = j.data.serializers.json.loads(resp)
        assert json3['name'] == "UPDATE"
        json4 = j.data.serializers.json.loads(o._ddict_json)

        assert json != json3  # should have been updated in db, so no longer same
        json4['id'] = id
        assert json4 == json3

        try:
            redis_cl.hset("objects:despiegk.test2", 25, o._json)
            raise RuntimeError("should have been in error")
        except Exception as e:
            assert str(e).find(
                "cannot update object with id:25, it does not exist") != -1
            # should not be able to set because the id does not exist

    def check_after_restart():
        redis_cl = j.clients.redis.get(ipaddr="localhost", port=6380)

        assert redis_cl.hlen("objects:despiegk.test2") == 9

        json = redis_cl.hget("objects:despiegk.test2", 3)
        ddict = j.data.serializers.json.loads(json)

        assert ddict["id"] == 3

        self._logger.debug("clean up database")
        redis_cl.delete("objects:despiegk.test2")

        # there should be 0 objects
        assert redis_cl.hlen("objects:despiegk.test2") == 0

    def sqlite_test():
        # SQLITE BACKEND
        self.redis_server_start(
            port=6380, background=True, zdbclient_addr=None)
        do()
        # restart redis lets see if schema's are there autoloaded
        self.redis_server_start(
            port=6380, background=True, zdbclient_addr=None)
        check_after_restart()

    def zdb_test():
        # ZDB test
        c = j.clients.zdb.client_admin_get()
        c.reset()  # removes the namespace from zdb, all is gone, need to create again
        c.namespace_new("test", secret="1234")
        self.redis_server_start(port=6380, background=True)
        do()

    sqlite_test()
    zdb_test()

    self._logger.debug("TEST OK")

    return ("OK")


def _compare_strings(s1, s2):
    # TODO: move somewhere into jumpscale tree
    def convert(s):
        if isinstance(s, bytes):
            s = s.decode()
        return s

    return convert(s1).strip() == convert(s2).strip()
