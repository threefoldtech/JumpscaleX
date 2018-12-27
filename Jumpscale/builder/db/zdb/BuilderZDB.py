from Jumpscale import j

JSBASE = j.builder.system._BaseClass
import socket


class BuilderZDB(j.builder.system._BaseClass):

    _SCHEMATEXT = """
        @url = jumpscale.builder.grafana.1
        name* = "" (S)
        addr = "" (S)
        port = 7777 (I)
        adminsecret = "" (S)
        mode = ""
        datadir = ""
        """

    def _init(self):
        self._logger_enable()

    def configure(self, name="main", addr="127.0.0.1", port=9900, datadir="", mode="seq", adminsecret="123456"):
        self.name = name
        self.addr = addr
        self.port = port
        self.mode = mode
        self.adminsecret = adminsecret
        self.datadir = datadir


    def isrunning(self):
        idir =  "%s/index/"%(self.datadir)
        ddir =  "%s/data/"%(self.datadir)
        if not j.sal.fs.exists(idir):
            return False
        if not j.sal.fs.exists(ddir):
            return False
        if not j.sal.nettools.tcpPortConnectionTest(self.addr,self.port):
            return False
        try:
            cl=self.client_admin_get()
            return cl.ping()
        except Exception as e:
            j.shell()


    def start(self, destroydata=False):
        """
        start zdb in tmux using this directory (use prefab)
        will only start when the server is not life yet

        js_shell 'j.servers.zdb.start(reset=True)'

        """


        if not destroydata and j.sal.nettools.tcpPortConnectionTest(self.addr, self.port):
            r = j.clients.redis.get(ipaddr=self.addr, port=self.port)
            r.ping()
            return()

        if destroydata:
            self.destroy()

        self.tmuxcmd.start()


        self._logger.info("waiting for zdb server to start on (%s:%s)" % (self.addr, self.port))

        res = j.sal.nettools.waitConnectionTest(self.addr, self.port)
        if res is False:
            raise RuntimeError("could not start zdb:'%s' (%s:%s)" % (self.name, self.addr, self.port))

        self.client_admin_get() #should also do a test, so we know if we can't connect

    def stop(self):
        self._logger.info("stop zdb")
        self.tmuxcmd.stop()


    @property
    def tmuxcmd(self):

        idir =  "%s/index/"%(self.datadir)
        ddir =  "%s/data/"%(self.datadir)
        j.sal.fs.createDir(idir)
        j.sal.fs.createDir(ddir)

        # zdb doesn't understand hostname
        addr = socket.gethostbyname(self.addr)


        cmd="zdb --listen %s --port %s --index %s --data %s --mode %s --admin %s --protect"%(addr,self.port,idir,ddir,self.mode,self.adminsecret)

        return j.tools.tmux.cmd_get(name="zdb_%s"%self.name,
                    window=self.tmux_window,pane=self.tmux_panel,
                    cmd=cmd,path="/tmp",ports=[self.port],
                    process_strings = ["wwwww:"])

    def destroy(self):
        self.stop()
        self._logger.info("destroy zdb")
        j.sal.fs.remove(self.datadir)
        # ipath = self.datadir+ "bcdbindex.db" % self.name

    @property
    def datadir(self):
        return "/sandbox/var/zdb/%s/"%self.name

    def client_admin_get(self):
        """

        """
        cl = j.clients.zdb.client_admin_get(addr=self.addr,
                                            port=self.port,
                                            secret=self.adminsecret,
                                            mode=self.mode)
        return cl

    def client_get(self, nsname="default", secret="1234"):
        """
        get client to zdb

        """
        cl = j.clients.zdb.client_get(nsname=nsname, addr=self.addr, port=self.port, secret=secret, mode=self.mode)

        assert cl.ping()

        return cl

    def start_test_instance(self, destroydata=True, namespaces=[], admin_secret="123456", namespaces_secret="1234"):
        """

        js_shell 'j.servers.zdb.start_test_instance(reset=True)'

        start a test instance with self.adminsecret 123456
        will use port 9900
        and name = test

        production is using other ports and other secret

        :return:
        """
        self.name = "test"
        self.port = 9901
        self.mode = "seq"
        self.adminsecret = admin_secret
        self.tmux_panel = "p11"

        self.start()

        cla = self.client_admin_get()
        if destroydata:
            j.clients.redis._cache_clear() #make sure all redis connections gone

        for ns in namespaces:
            if not cla.namespace_exists(ns):
                cla.namespace_new(ns,secret=namespaces_secret)
            else:
                if destroydata:
                    cla.namespace_delete(ns)
                    cla.namespace_new(ns,secret=namespaces_secret)

        if destroydata:
            j.clients.redis._cache_clear() #make sure all redis connections gone

        return self.client_admin_get()

    def build(self):
        """
        js_shell 'j.servers.zdb.build()'
        """
        j.builder.zero_os.zos_db.build(install=True, reset=True)

    def test(self, build=False):
        """
        js_shell 'j.servers.zdb.test(build=True)'
        """
        if build:
            self.build()
        self.destroy()
        self.start_test_instance()
        self.stop()
        self.start(mode='seq')
        cl = self.client_get(nsname="test")

        print("TEST OK")
