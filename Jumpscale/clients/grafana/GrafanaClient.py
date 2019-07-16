from Jumpscale import j
import requests
from requests.auth import HTTPBasicAuth

JSConfigClient = j.application.JSBaseConfigClass


class GrafanaClient(JSConfigClient):

    _SCHEMATEXT = """
        @url = jumpscale.clients.grafana.client
        name* = "" (S)
        url = "" (S)
        username = "" (S)
        password = "" (S)
        verify_ssl = False (B)
        """

    def _init(self, **kwargs):
        self._httpclient = None

    def ping(self):
        pass

    def test(self):
        pass

        # IMPLEMENT some basic test using the client


# remark: can use the self.caching framework where relevant, this to speed up remote operations
