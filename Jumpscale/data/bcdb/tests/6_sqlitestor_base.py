from Jumpscale import j


def main(self):
    """
    to run:

    js_shell 'j.data.bcdb.test(name="sqlitestor_base")'

    use a bcdb which is using sqlite

    """

    bcdb, _ = self._load_test_model(reset=True, sqlitestor=True)

    mpath = self._dirpath+"/tests/models"
    assert j.sal.fs.exists(mpath)

    # make sure we remove the maybe already previously generated model file
    for item in j.sal.fs.listFilesInDir(mpath, filter="*.py"):
        j.sal.fs.remove(item)

    bcdb.models_add(mpath)

    model = bcdb.model_get('jumpscale.bcdb.test.house')
    assert model.get_all() == []

    assert model.bcdb.zdbclient is None

    model_obj = model.new()
    model_obj.cost = "10 USD"
    model_obj.save()
    model.cache_reset()
    data = model.get(model_obj.id)
    assert data.cost_usd == 10
    assert model_obj.cost_usd == 10

    model.cache_reset()
    model_obj.cost = "11 USD"
    model_obj.save()
    data = model.get(model_obj.id)
    # is with cash
    assert data.cost_usd == 11
    model.cache_reset()
    assert model.obj_cache == {}  # cache needs to be empty
    data = model.get(model_obj.id)
    assert data.cost_usd == 11
    assert model.obj_cache != {}  # now there needs to be something in

    model.cache_reset()
    model_obj = model.new()
    model_obj.cost = "12 USD"
    model_obj.save()
    assert model.obj_cache != {}  # now there needs to be something in

    assert model_obj.id == 2

    model.get(1)._ddict == {'name': '',
                            'active': False,
                            'cost': b'\x00\x97\x0b\x00\x00\x00',
                            'room': [],
                            'id': 2}

    model.get(2)._ddict == {'name': '',
                            'active': False,
                            'cost': b'\x00\x97\x0c\x00\x00\x00',
                            'room': [],
                            'id': 2}

    assert model.index.select().first().cost == 11.0  # is always in usd

    print("TEST FOR MODELS DONE in SQLITE")

    return ("OK")
