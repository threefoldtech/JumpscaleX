import os
from Jumpscale import j

from .HubDirectClient import HubDirectClient

JSConfigs = j.application.JSBaseConfigsClass


class HubDirectFactory(JSConfigs):
    """
    """

    __jslocation__ = "j.clients.zhubdirect"
    _CHILDCLASS = HubDirectClient

    def _init(self, **kwargs):
        self.__imports__ = "ovc"

    def generate(self):
        """
        generate the client out of the raml specs

        kosmos 'j.clients.zhubdirect.generate()'

        """
        path = j.sal.fs.getDirName(os.path.abspath(__file__)).rstrip("/")
        c = j.tools.raml.get(path)
        # c.specs_get('https://github.com/zero-os/hub-direct-server/tree/master/apidocs/api.raml') # broken...
        c.client_python_generate()
