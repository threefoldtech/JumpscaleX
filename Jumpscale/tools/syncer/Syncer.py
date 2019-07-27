from Jumpscale import j
import time
from watchdog.observers import Observer
from .MyFileSystemEventHandler import MyFileSystemEventHandler
import gevent


class Syncer(j.application.JSBaseConfigClass):
    """
    make sure there is an ssh client first, can be done by

    j.clients.ssh.get...

    :param name:
    :param sshclient_name: name as used in j.clients.ssh
    :param paths: specified as
        e.g.  "{DIR_CODE}/github/threefoldtech/0-robot:{DIR_TEMP}/0-robot,..."
        e.g.  "{DIR_CODE}/github/threefoldtech/0-robot,..."
        can use the {} arguments
        if destination not specified then is same as source

    if not specified is:
        paths = "{DIR_CODE}/github/threefoldtech/jumpscaleX,{DIR_CODE}/github/threefoldtech/digitalmeX"

    """

    _SCHEMATEXT = """
        @url = jumpscale.syncer.1
        name* = "" (S)
        sshclient_names = [] (LS)
        paths = [] (LS)
        ignoredir = [] (LS)
        t = ""  (S)  
        """

    def sshclients_add(self, sshclients=None):
        """

        :param sshclients: name of sshclient, sshclient or list of sshclient or names
        :return:
        """
        assert sshclients
        from Jumpscale.clients.ssh.SSHClientBase import SSHClientBase

        if j.data.types.list.check(sshclients):
            for item in sshclients:
                self.sshclients_add(item)
            return
        elif isinstance(sshclients, SSHClientBase):
            cl = sshclients
        elif isinstance(sshclients, str):
            name = sshclients
            if not j.clients.ssh.exists(name=name):
                raise RuntimeError("cannot find sshclient:%s for syncer:%s" % (name, self))

            cl = j.clients.ssh.get(name=name)
        else:
            raise RuntimeError("only support name of sshclient or the sshclient instance itself")

        if cl.name not in self.sshclients:
            self.sshclients[cl.name] = cl

    def _init(self, **kwargs):

        self.sshclients = {}
        self.monitor_greenlet = None

        for name in self.sshclient_names:
            self.sshclients_add(name)

        self.IGNOREDIR = [".git", ".github"]
        self._executor = None

        # self.paths = []
        if self.paths == []:
            self.paths.append("{DIR_CODE}/github/threefoldtech/jumpscaleX")
            self.paths.append("{DIR_CODE}/github/threefoldtech/digitalmeX")
            self.save()

        self._log_debug(self)

    def _get_paths(self, executor=None):
        """

        :return: [[src,dest],...]
        """
        res = []
        for item in self.paths:

            if not item.startswith("/") and not item.startswith("{"):
                item = j.sal.fs.getcwd() + "/" + item
            item = item.replace("//", "/")

            items = item.split(":")
            if len(items) == 1:
                src = items[0]
                dst = src
            elif len(items) == 2:
                src = items[0]
                dst = items[1]
            else:
                raise RuntimeError("can only have 2 parts")
            src = j.core.tools.text_replace(src)
            if not executor:
                dst = None
            else:
                if "{" in dst:
                    dst = executor._replace(dst)
            res.append((src, dst))
        return res

    def _path_dest_get(self, executor=None, src=None):
        assert executor
        assert src
        for src_model, dest_model in self._get_paths(executor=executor):
            if src.startswith(src_model):
                dest = j.sal.fs.joinPaths(dest_model, j.sal.fs.pathRemoveDirPart(src, src_model))
                return dest
        raise RuntimeError("did not find:%s" % src)

    def monitor(self, start=True):
        from .MyFileSystemEventHandler import FileSystemMonitor

        self.monitor_greenlet = FileSystemMonitor(syncer=self)
        if j.servers.rack.current:
            j.servers.rack.current.greenlets["fs_sync_monitor"] = self.monitor_greenlet

        self.monitor_greenlet.start()

    def handler(self, event, action="copy"):
        # self._log_debug("%s:%s" % (event, action))
        for key, sshclient in self.sshclients.items():

            if sshclient.executor.isContainer:
                continue

            ftp = sshclient.sftp
            changedfile = event.src_path
            if event.src_path.endswith((".swp", ".swx")):
                return
            elif event.is_directory:
                if changedfile.find("/.git") != -1:
                    return
                elif changedfile.find("/__pycache__/") != -1:
                    return
                elif changedfile.find(".egg-info") != -1:
                    return
                if event.event_type == "modified":
                    return
                self._log_info("directory changed")
                return self.sync(monitor=False)  # no need to continue
            else:
                self._log_info("file changed: %s" % changedfile)
                error = False

                if error is False:
                    print(changedfile)
                    if changedfile.find("/.git") != -1:
                        return
                    elif changedfile.find("/__pycache__/") != -1:
                        return
                    elif changedfile.find("/_tmp_/") != -1:
                        return
                    elif changedfile.endswith(".pyc"):
                        return
                    elif changedfile.endswith("___"):
                        return
                    dest = self._path_dest_get(executor=sshclient.executor, src=changedfile)
                    e = ""

                    if action == "copy":
                        self._log_debug("copy: %s:%s" % (changedfile, dest))
                        print("copy: %s:%s" % (changedfile, dest))
                        try:
                            sshclient.file_copy(changedfile, dest)
                        except Exception as e:
                            self._log_error("Couldn't sync file: %s:%s" % (changedfile, dest))
                            self._log_error("** ERROR IN COPY, WILL SYNC ALL")
                            self._log_error(str(e))
                            error = True
                    elif action == "delete":
                        self._log_debug("delete: %s:%s" % (changedfile, dest))
                        try:
                            cmd = "rm %s" % dest
                            sshclient.exec_command(cmd)
                        except Exception as e:
                            self._log_error("Couldn't remove file: %s" % (dest))
                            if "No such file" in str(e):
                                return
                            else:
                                error = True
                                # raise RuntimeError(e)
                    else:
                        raise j.exceptions.RuntimeError(
                            "action not understood in filesystemhandler on sync:%s" % action
                        )

                    if error:
                        try:
                            self._log_debug(e)
                        except BaseException:
                            pass
                        self.sync(monitor=False)
                        error = False

    def delete(self):
        for item in j.clients.ssh.find(name=self.sshclient_name):
            item.delete()
        j.application.JSBaseConfigClass.delete(self)

    def sync(self, monitor=True, start=True):
        """
        sync all code to the remote destinations, uses config as set in jumpscale.toml

        """

        for key, sshclient in self.sshclients.items():

            if sshclient.executor.isContainer:

                continue

            j.shell()
            w

            for item in self._get_paths(executor=sshclient.executor):
                source, dest = item
                self._log_info("upload:%s to %s" % (source, dest))
                for i in range(2):
                    sshclient.executor.upload(
                        source,
                        dest,
                        recursive=True,
                        createdir=True,
                        rsyncdelete=True,
                        ignoredir=self.IGNOREDIR,
                        ignorefiles=None,
                    )

        if monitor:
            self.monitor(start=start)
