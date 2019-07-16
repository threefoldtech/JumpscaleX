from Jumpscale import j
from .GrafanaClient import GrafanaClient


class GrafanaFactory(j.application.JSBaseConfigsClass):

    __jslocation__ = "j.clients._template"
    _CHILDCLASS = GrafanaClient

    def _init(self, **kwargs):
        self.clients = {}

    def test(self):
        self.get(url="...", name="sss")
        self.count()
        self.find()  # TODO: will find all
        self.find(url="ss")  # TODO: check
