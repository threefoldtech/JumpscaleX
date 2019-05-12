from Jumpscale import j


def main(self):
    """
    to run:

    kosmos 'j.data.bcdb.test(name="keys")'

    """

    SCHEMA = """
    @url = threefoldtoken.wallet.test
    @name = wallet
    name* = "wallet"
    jwt = "" (S)                # JWT Token
    addr* = ""                   # Address
    ipaddr* = (ipaddr)           # IP Address
    email* = "" (S)              # Email address
    username* = "" (S)           # User name
    
    
    """

    bcdb = j.data.bcdb.get("test")
    m = bcdb.model_get_from_schema(SCHEMA)

    m.reset()

    o = m.new()
    assert o._model.schema.url == "threefoldtoken.wallet.test"
    o.addr = "something"
    o.email = "myemail"
    o.username = "myuser"
    o.save()

    assert o._model.schema.url == "threefoldtoken.wallet.test"

    o2 = m.get_by_addr(o.addr)[0]
    assert len(m.get_by_addr(o.addr)) == 1
    o3 = m.get_by_email(o.email)[0]
    o4 = m.get_by_username(o.username)[0]

    assert o2.id == o.id
    assert o3.id == o.id
    assert o4.id == o.id

    o = m.new()
    o.name = "test2"
    o.addr = "something2"
    o.email = "myemail2"
    o.username = "myuser"
    o.save()

    o = m.new()
    o.name = "test3"
    o.addr = "something2"
    o.email = "myemail2"
    o.username = "myuser2"
    o.save()

    assert o._model.schema.url == "threefoldtoken.wallet.test"

    l = m.get_by_username("myuser")
    assert len(l) == 2

    l = m.get_from_keys(email="myemail2", username="myuser")
    assert len(l) == 1

    assert len(m.get_all()) == 3
    o_check = m.get_all()[-1]
    assert o_check.id == o.id
    rkey = bcdb._hset_index_key_get(schema=m.schema)
    o.delete()
    for key in j.clients.credis_core.keys(rkey + b":*"):
        for key2 in j.clients.credis_core.hkeys(key):
            data_ = j.clients.credis_core.hget(key, key2)
            data__ = j.data.serializers.msgpack.loads(data_)
            if o.id in data__:
                raise RuntimeError("the id should not be in the redis index")

    m2 = bcdb.model_get_from_schema(SCHEMA)
    assert m2.schema.sid == m.schema.sid

    SCHEMA3 = """
    @url = threefoldtoken.wallet.test2
    @name = wallet
    name* = "wallet3"
    jwt = "" (S)                # JWT Token
    addr* = "aa"                   # Address
    ipaddr* = "" (ipaddr)           # IP Address
    email* =  (S)              # Email address 
    nr = 10 (I)
    nr2 =  (I)
    nr3 =  (N)
    nr4 = 5 (N)
    date = (D)   
    
    """
    m3 = bcdb.model_get_from_schema(SCHEMA3)
    o = m3.new()

    # default
    assert o.addr == "aa"
    assert o.ipaddr == "0.0.0.0"
    assert o.email == ""
    assert o.nr == 10
    assert o.nr2 == 2147483647
    assert o.nr3 == b"\x00\x97\x00\x00\x00\x00"
    assert o.nr3_usd == 0
    assert o.nr4_usd == 5
    assert o.date == 0

    o.ipaddr = "192.168.1.1"
    o.email = "ename"
    o.addr = "test"
    o.name = "test2"
    o.save()
    assert o._model.schema.url == "threefoldtoken.wallet.test2"

    data = bcdb._hset_index_key_get(schema=m3.schema, returndata=True)
    redisid = data[bcdb.name][m3.schema.url]
    rkey = bcdb._hset_index_key_get(schema=m3.schema)
    assert rkey.decode().endswith(
        str(redisid)
    )  # check that the raw info is same as the info from function

    assert len(j.clients.credis_core.keys(rkey + b":*")) == 4

    assert len(m3.get_all()) == 1

    assert [i for i in m3.id_iterator] == [
        m3.get_all()[0].id
    ]  # should only be the 1 id in there

    assert len(m3.get_by_addr("test")) == 1

    assert len(m3.get_from_keys(addr="test", email="ename", ipaddr="192.168.1.1")) == 1
    assert len(m3.get_from_keys(addr="test", email="ename", ipaddr="192.168.1.2")) == 0

    a = j.servers.zdb.client_admin_get()
    zdbclient2 = a.namespace_new("test2", secret="12345")

    bcdb2 = j.data.bcdb.new("test2", zdbclient2, reset=True)
    assert len(m3.get_from_keys(addr="test", email="ename", ipaddr="192.168.1.1")) == 1
    bcdb2.reset()
    assert len(m3.get_from_keys(addr="test", email="ename", ipaddr="192.168.1.1")) == 1

    # now we know that the previous indexes where not touched

    m4 = bcdb2.model_get_from_schema(SCHEMA3)
    o = m4.new()
    o.ipaddr = "192.168.1.1"
    o.email = "ename"
    o.addr = "test"
    o.save()

    assert o._model.schema.url == "threefoldtoken.wallet.test2"

    myid = o.id + 0  # make copy

    assert len(m4.get_from_keys(addr="test", email="ename", ipaddr="192.168.1.1")) == 1

    o5 = m4.get_from_keys(addr="test", email="ename", ipaddr="192.168.1.1")[0]
    assert o5.id == myid

    bcdb.reset()

    assert m3.get_from_keys(addr="test", email="ename", ipaddr="192.168.1.1") == []
    assert len(m4.get_from_keys(addr="test", email="ename", ipaddr="192.168.1.1")) == 1

    bcdb2.reset()

    # check 2 bcdb are empty (doesnt work yet): #TODO:*3
    # assert len(j.sal.fs.listDirsInDir("/sandbox/var/bcdb/test"))==0
    # assert len(j.sal.fs.listDirsInDir("{DIR_BASE}/var/bcdb/test2"))==0
    # assert len(j.sal.fs.listDirsInDir("{DIR_VAR}/bcdb/test2"))==0

    self._log_info("TEST DONE")
    return "OK"
