from Jumpscale import j
from .Syncer import Syncer


class SyncerFactory(j.application.JSBaseConfigsClass):
    __jslocation__ = "j.tools.syncer"

    _CHILDCLASS = Syncer

    def sync(self, monitor=False):
        """
        execute to sync all syncers
        will push default code directories to remove ssh host
        """
        for name in self._children:
            self.syncers[name].sync()

        if monitor:
            self.monitor()

    def test(self):
        """
        kosmos 'j.tools.syncer.test()'
        :return:
        """

        cl = j.clients.ssh.get(name="test1", addr="167.71.65.114", port=22)
        cl.save()

        cl2 = j.clients.ssh.get(name="test2", addr="167.71.65.114", port=22)
        cl2.save()

        s = j.tools.syncer.get()

        s.sshclients_add([cl, cl2])

        s.sync(monitor=True)
