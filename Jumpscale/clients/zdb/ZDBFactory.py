import os
import uuid
from pprint import pprint

from Jumpscale import j

from .ZDBAdminClient import ZDBAdminClient
from .ZDBClientBase import ZDBClientBase
from .clients_impl import ZDBClientDirectMode, ZDBClientSeqMode, ZDBClientUserMode



_client_map = {
    'seq': ZDBClientSeqMode,
    'sequential': ZDBClientSeqMode,
    'user': ZDBClientUserMode,
    'direct': ZDBClientDirectMode,
}


class ZDBFactory(j.application.JSBaseConfigsClass):
    __jslocation__ = "j.clients.zdb"

#     _CHILDCLASS = ZDBAdminClient
    _CHILDCLASS = ZDBClientBase

    def client_admin_get(self, addr="localhost", port=9900, secret="123456", mode='seq'):
        return ZDBAdminClient(factory=self,addr=addr, port=port, secret=secret,mode=mode)

    def client_get(self, nsname="test", addr="localhost", port=9900, secret="1234", mode="seq"):
        """
        :param nsname: namespace name
        :param addr:
        :param port:
        :param secret:
        :return:
        """
        if mode not in _client_map:
            return ValueError("mode %s not supported" % mode)
        klass = _client_map[mode]
        return klass(factory=self,addr=addr, port=port, secret=secret, nsname=nsname)


    def _childclass_selector(self, childclass_name=None, data=None):
        if data is None:
            return ZDBClientBase
        if data.admin:
            return ZDBAdminClient
        else:
            if data.mode not in _client_map:
                raise ValueError("mode '%s' not supported" % data.mode)
            return _client_map[data.mode]

    def start_test_instance(self, destroydata=False, admin_secret="123456", namespaces_secret="1234"):
        """
        js_shell 'j.clients.zdb.start_test_instance(destroydata=True)'

        will start a ZDB server in tmux (will only start when not there yet or when reset asked for)
        erase all content
        and will return client to it

        """

        return j.servers.zdb.start_test_instance(destroydata=destroydata, admin_secret=admin_secret,
                                                 namespaces_secret=namespaces_secret)

    def test(self):
        """
        js_shell 'j.clients.zdb.test()'

        """

        cl = j.clients.zdb.start_test_instance()

        self._test_run(name="base")
        self._test_run(name="admin")
