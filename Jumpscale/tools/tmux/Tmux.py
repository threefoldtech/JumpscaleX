
from Jumpscale import j
import libtmux as tmuxp
import time
import psutil

JSBASE = j.application.JSBaseClass

from .Session import Session
from .TmuxCmd import TmuxCmd

class Tmux(j.application.JSBaseClass):

    def __init__(self):
        self.__jslocation__ = "j.tools.tmux"
        JSBASE.__init__(self)

        self._server = None
        self._session = None
        self._windows_active = {}
        self._logger_enable()


    @property
    def session(self):
        """
        we only want to allow 1 tmux session, its already complex enough
        :return:
        """
        if self._session is None:
            try:
                sessions = self.server.list_sessions()
                self._session =  Session(session=sessions[0])
            except Exception as e:
                session1 = self.server.new_session("main")
                self._session = Session(session=session1)
        return self._session

    def _find_procs_by_name(self,name,startswith_is_ok=True):
        "Return a list of processes matching 'name'."
        ls = []
        for p in psutil.process_iter(attrs=['name']):
            # print(p.info['name'])
            if p.info['name'] is None:
                if p.status() == "zombie":
                    j.sal.process.kill(p.pid)
                    continue
            if startswith_is_ok:
                if p.info['name'].startswith(name):
                    ls.append(p)
            else:
                if p.info['name'] == name:
                    ls.append(p)
        return ls

    @property
    def server(self):
        if self._server is None:
            rc,out,err = j.core.tools.execute("tmux ls",die=False)
            if out.strip().count("\n")>0:
                raise RuntimeError("found too many tmux sessions, there should only be 1")

            if rc>0 and "out".find("no server")==-1:
                cmd = "/sandbox/bin/js_mux start"
                j.sal.process.executeWithoutPipe(cmd)
                time.sleep(0.1)
            elif rc>0:
                j.shell()

            rc,out,err=j.sal.process.execute("tmux -f /sandbox/cfg/.tmux.conf has-session -t main",die=False)
            if rc>0:
                raise RuntimeError("did not find tmux session -t main")

            self._server = tmuxp.Server()
            self._logger.info("tmux server is running")

        return self._server

    def kill(self):
        """
        js_shell 'j.tools.tmux.kill()'
        """
        self.session.kill()

    def pane_get(self,window="main", pane="main",reset=False):
        w=self.window_get(window=window)
        return w.pane_get(name=pane, killothers=False, reset=reset)

    def window_get(self,window="main",reset=False):
        s=self.session
        return s.window_get(window,reset=reset)

    def execute(self, cmd, window="main", pane="main",reset=True):
        """
        """
        p = self.pane_get(window=window,pane=pane,reset=reset)
        p.execute(cmd)
        return p

    def cmd_get(self,name,window="digitalme",pane="p11",cmd="",path=None,env={},ports=[],stopcmd=None,process_strings=[]):
        """

        example
        ```
        env={}
        env["color"]="blue"
        cmd = j.tools.tmux.cmd_get(name="test",pane="p21",cmd="ls /", env=env,stopcmd="killall...",process_strings=[])
        cmd.stop()
        cmd.start()
        ```


        :param name: name of the command
        :param window: window to use std multi
        :param pane: pane in the window, make sure there is no overlap
        :param cmd: command to execute in the pane
        :param path: path where to execute
        :param env: are the arguments wich will become env arguments, useful to pass variable to process
        :param ports: array of ports this process will use
        :param stopcmd: if specific command to use to stop a process
        :param process_strings: which strings to check if the process is running
        :return:
        """
        if not self.session.window_exists(window):
            if window == "multi":
                self.panes_multi_create(window_name=window)
            elif window == "digitalme":
                self.panes_digitalme_create(window_name=window)
            elif window == "2x2":
                self.panes_2x2_get(window_name=window)
            else:
                self.window_get(window=window, reset=True)

        return TmuxCmd(name=name,pane_name=pane,window_name=window,
                       cmd=cmd,path=path,env=env,ports=ports,stopcmd=stopcmd,process_strings=process_strings)

    def panes_2x2_get(self, window_name="multi", reset=True):

        window = self.window_get(window_name, reset=reset)

        if len(window.panes) == 4 and reset is False:
            p11 = window.pane_get(name="p11")
            p12 = window.pane_get(name="p12")
            p21 = window.pane_get(name="p21")
            p22 = window.pane_get(name="p22")


        else:
            #xy notation
            p11 = window.pane_get(name="p11", killothers=True)
            p12 = p11.splitVertical("p12")
            p21 = p11.splitHorizontal("p21")
            p22 = p12.splitHorizontal("p22")


        return p11,p12,p21,p22

    def panes_digitalme_create(self, window_name="digitalme", reset=True):

        window = self.window_get(window_name, reset=reset)

        if len(window.panes) == 6 and reset is False:
            return window
        else:
            #xy notation
            p11 = window.pane_get(name="p11", killothers=True)
            p13 = p11.splitVertical("p13")
            p21 = p11.splitHorizontal("p21")
            p22 = p13.splitHorizontal("p22")

            p12 = p11.splitVertical("p12")
            p14 = p13.splitVertical("p14")

            return window


    def panes_multi_create(self, window_name="multi", reset=False):
        """

        js_shell 'j.tools.tmux.panes_multi_get()'

        :param window_name:
        :param reset:
        :return:
        """


        window = self.window_get(window_name, reset=reset)

        if len(window.panes) == 13 and reset is False:
            return window

        p11,p13,p31,p33 = self.panes_2x2_get(window_name, reset=reset)
        p13.name_set("p13")
        p31.name_set("p31")
        p33.name_set("p33")
        p12 = p11.splitVertical("p12")
        p14 = p13.splitVertical("p14")
        p21 = p11.splitHorizontal("p21")
        p22 = p12.splitHorizontal("p22")
        p23 = p13.splitHorizontal("p23")
        p24 = p14.splitHorizontal("p24")

        p41 = p31.splitHorizontal("p41")
        p32 = p31.splitVertical("p32")
        p42 = p41.splitVertical("p42")



        return window


    def test(self):
        """
        js_shell 'j.tools.tmux.test()'

        :return:
        """

        self.panes_2x2_create()
        window = self.window_get("multi")
        for pane in window.panes:
            pane.execute("clear;echo %s" % pane.name)

        p = self.execute("ls /","multi","p22")

        assert p.process_obj.name()=="bash"
        assert p.process_obj_child == None

        p = self.execute("htop","multi","p22")

        assert p.process_obj.is_running()
        # assert p.process_obj.name()=="htop"

        assert len(p.process_obj_children)==1


        assert p.process_obj.name()=="bash"
        assert p.process_obj_child.name()=="htop"


        p = self.execute("find /tmp","test","test")
        res = p.out_get()
        p=self.pane_get("test2","test2",reset=True)

        self._logger.info("tests ok for tmux")


    def test_multi(self):
        """
        js_shell 'j.tools.tmux.test_multi()'

        :return:
        """
        j.tools.tmux.panes_multi_get()

        cmd = self.cmd_get(name="htop",window="multi",pane="p11",cmd="htop")
        cmd.start()

        j.shell()
