"""
Tfchain Client
"""

from Jumpscale import j

from Jumpscale.clients.http.HttpClient import HTTPError

# TODO: support a shuffle feature in the idGenerator module of JS
#       or make sure we can do it using the already available generateRandomInt functionality
import random

class TFChainExplorerClient(j.application.JSBaseClass):
    """
    Client to get data from a tfchain explorer.
    """

    def get(self, nodes, endpoint):
        """
        get data from an explorer at the endpoint from any explorer that is avaialble
        on one of the given urls. The list of urls is traversed in random order until
        an explorer returns with a 200 OK status.

        @param urls: the list of urls of all avaialble explorers
        @param endpoint: the endpoint to get the data from
        """
        assert len(nodes) > 0
        indices = list(range(len(nodes)))
        random.shuffle(indices)
        for idx in indices:
            try:
                node = nodes[idx]
                if isinstance(node, dict):
                    address = node['address']
                    password = node.get('password', '')
                else:
                    assert isinstance(node, str)
                    address = str(node)
                    password = ""
                if password:
                    raise Exception("PASSWORD NOT SUPPORTED YET")
                resp = j.clients.http.get(url=address+endpoint)
                if resp.getcode() == 200:
                    return resp.readline()
            except HTTPError as e:
                self._logger.debug("tfchain explorer get exception at endpoint {} on {}: {}".format(endpoint, address, e))
                pass
        raise Exception("no explorer was available to fetch endpoint {}".format(endpoint))

    def test(self):
        """
        js_shell 'j.clients.tfchain.explorer.test()'
        """
        resp = self.get(nodes=['https://explorer2.threefoldtoken.com'], endpoint='/explorer/constants')
        data = j.data.serializers.json.loads(resp)
        assert data['chaininfo']['Name'] == 'tfchain'
        assert data['chaininfo']['CoinUnit'] == 'TFT'
