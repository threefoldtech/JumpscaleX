from Jumpscale import j
import inspect
import os
import copy
import sys
import inspect
import types

class JSBase:

    def _obj_cache_reset(self):
        """
        this empties the runtime state of an obj and the logger and the testruns
        :return:
        """
        self.__class__._logger_ = None
        self.__class__._test_runs = {}
        self._cache_ = None
        self._objid_ = None

        for key,obj in self.__dict__.items():
            del obj

    def _class_init(self):

        if not hasattr(self.__class__,"_class_init_done"):
            # print("_class init:%s"%self.__class__.__name__)
            #only needed to execute once, needs to be done at init time, class inheritance does not exist
            self.__class__._dirpath_ = ""           #path of the directory hosting this class
            self.__class__._logger_ = None          #logger attached to this class
            self.__class__._cache_expiration = 3600 #expiration of the cache
            self.__class__._test_runs = {}
            self.__class__._test_runs_error = {}

            self.__class__.__name__ = j.core.text.strip_to_ascii_dense(str(self.__class__)).split(".")[-1].lower()
            #short location name:
            if '__jslocation__' in self.__dict__:
                self.__class__._location = self.__jslocation__
            elif '__jslocation__' in self.__class__.__dict__:
                self.__class__._location = self.__class__.__jslocation__
            elif '__jscorelocation__' in self.__dict__:
                self.__class__._location = self.__jslocation__
            else:
                self.__class__._location = self.__class__.__name__.lower()

            self.__class__._methods_ = []
            self.__class__._properties_ = []
            self.__class__._inspected_ = False

            # print("classinit_2:%s"%self.__class__)
            # print(self.__class__._properties_)

            self.__class__._class_init_done = True


    def __init__(self,init=True):
        self._class_init() #is needed to init class properties, needs to be first thing

        if init:
            self._init()

        self._obj_cache_reset()


    def _init(self):
        pass

    @property
    def _dirpath(self):
        if self.__class__._dirpath_ =="":
            self.__class__._dirpath_ = os.path.dirname(inspect.getfile(self.__class__))
        return self.__class__._dirpath_

    @property
    def _objid(self):
        if self._objid_ is None:
            id = self.__class__._location
            id2=""
            try:
                id2=self.data.name
            except:
                pass
            if id2=="":
                try:
                    if self.data.id is not None:
                        id2 = self.data.id
                except:
                    pass
            if id2=="":
                for item in ["instance", "_instance", "_id", "id", "name", "_name"]:
                    if item in self.__dict__ and self.__dict__[item]:
                        self._logger.debug("found extra for obj_id")
                        id2 = str(self.__dict__[item])
                        break
            if id2!="":
                self._objid_ = "%s_%s"%(id,id2)
            else:
                self._objid_ = id
        return self._objid_


    @property
    def _logger(self):
        if self.__class__._logger_ is None:
            self.__class__._logger_ = j.logger.get(self.__class__._location)
            self.__class__._logger_._parent = self
        return self.__class__._logger_

    def _logger_enable(self):
        self.__class__._logger_ = j.logger.get(self.__class__._location,force=True)
        self._logger.level = 0

    @property
    def _cache(self):
        if self._cache_ is None:
            self._cache_ = j.core.cache.get(self._objid, expiration=self._cache_expiration)
        return self._cache_

    def _inspect(self):
        if not self.__class__._inspected_:
            # print("INSPECT:%s"%self.__class__)
            assert self.__class__._methods_==[]
            assert self.__class__._properties_==[]
            for name,obj in  inspect.getmembers(self.__class__):
                if name.startswith("_"):
                    continue
                elif inspect.ismethod(obj):
                    self.__class__._methods_.append(name)
                elif inspect.ismethoddescriptor(obj):
                    j.shell()
                    w
                elif inspect.isfunction(obj):
                    self.__class__._methods_.append(name)
                elif inspect.isclass(obj):
                    j.shell()
                    w
                elif inspect.isgetsetdescriptor(obj):
                    j.shell()
                    w
                else:
                    self.__class__._properties_.append(name)

            for item in self.__dict__.keys():
                if item.startswith("_"):
                    continue
                if item not in self._methods_:
                    self.__class__._properties_.append(item)

            self.__class__._inspected_ = True
        # else:
        #     print("not inspect:%s"%self.__class__)


    def _properties(self):
        self._inspect()
            # methods = self._methods()
            # r=[]
            # for item in self.__dict__.keys():
            #     if item.startswith("_"):
            #         continue
            #     if item not in methods:
            #         self.__class__._properties_.append(item)
        return self.__class__._properties_

    def _methods(self):
        self._inspect()
        # if self.__class__._methods_ == []:
        #     for item in dir(self):
        #         if item.startswith("_"):
        #             continue
        #         possible_method = eval("self.%s"%item)
        #         if isinstance(possible_method,types.MethodType) and item not in self.__class__._methods_:
        #             self.__class__._methods_.append(item)
        return self.__class__._methods_


    def _properties_children(self):
        return []

    def _properties_model(self):
        return []

    @property
    def _ddict(self):
        res={}
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                v = self.__dict__[key]
                if not isinstance(v,types.MethodType):
                    res[key] = v
        return res

    def _warning_raise(self,msg,e=None,cat=""):
        """

        :param msg:
        :param e: the python error e.g. after try: except:
        :param cat: any dot notation
        :return:
        """
        msg="ERROR in %s\n"%self
        msg+="msg\n"

    def _error_bug_raise(self,msg,e=None,cat=""):
        """

        :param msg:
        :param e: the python error e.g. after try: except:
        :param cat: any dot notation
        :return:
        """
        if cat == "":
            out = "BUG: %s"%msg
        else:
            out = "BUG (%s): %s "%(cat,msg)
        out+=msg+"\n"
        raise RuntimeError(msg)

    def _error_input_raise(self,msg,cat=""):
        if cat == "":
            msg = "ERROR_INPUT: %s"%msg
        else:
            msg = "ERROR_INPUT (%s): %s "%(cat,msg)
        raise RuntimeError(msg)
        j.shell()
        print()
        sys.exit(1)

    def _error_monitor_raise(self,msg,cat=""):
        if cat == "":
            msg = "ERROR_MONITOR: %s"%msg
        else:
            msg = "ERROR_MONITOR (%s): %s "%(cat,msg)
        j.shell()
        print()
        sys.exit(1)

    def _done_check(self,name="",reset=False):
        if reset:
            self._done_reset(name=name)
        if name=="":
            return j.core.db.hexists("done",self._objid)
        else:
            return j.core.db.hexists("done","%s:%s"%(self._objid,name))

    def _done_set(self,name="",value="1"):
        if name=="":
            return j.core.db.hset("done",self._objid,value)
        else:
            return j.core.db.hset("done","%s:%s"%(self._objid,name),value)

    def _done_get(self,name=""):
        if name=="":
            return j.core.db.hget("done",self._objid)
        else:
            return j.core.db.hget("done","%s:%s"%(self._objid,name))

    def _done_reset(self,name=""):
        """
        if name =="" then will remove all from this object
        :param name:
        :return:
        """
        if name=="":
            for item in j.core.db.hkeys("done"):
                item=item.decode()
                print("reset todo:%s"%item)
                if item.find(self._objid)!=-1:
                    j.core.db.hdel("done",self._objid)
        else:
            return j.core.db.hdel("done","%s:%s"%(self._objid,name))

    def _test_error(self, name, error):
        j.errorhandler.try_except_error_process(error, die=False)
        self.__class__._test_runs_error[name] = error

    def _test_run(self, name="", obj_key="main", **kwargs):
        """

        :param name: name of file to execute can be e.g. 10_test_my.py or 10_test_my or subtests/test1.py
                    the tests are found in subdir tests of this file

                if empty then will use all files sorted in tests subdir, but will not go in subdirs

        :param obj_key: is the name of the function we will look for to execute, cannot have arguments
               to pass arguments to the example script, use the templating feature, std = main


        :return: result of the tests

        """

        res = self.__test_run(name=name, obj_key=obj_key, **kwargs)
        if self.__class__._test_runs_error != {}:
            for key, e in self.__class__._test_runs_error.items():
                self._logger.error("ERROR FOR TEST: %s\n%s" % (key, e))
            self._logger.error("SOME TESTS DIT NOT COMPLETE SUCCESFULLY")
        else:
            self._logger.info("ALL TESTS OK")
        return res

    def __test_run(self, name=None, obj_key="main", **kwargs):

        if name == '':
            name=None

        self._logger_enable()
        if name is not None:
            self._logger.info("##: TEST RUN: %s"%name.upper())

        if name is not None:

            if name.endswith(".py"):
                name = name[:-3]


            tpath = "%s/tests/%s" % (self._dirpath, name)
            tpath = tpath.replace("//", "/")
            if not name.endswith(".py"):
                tpath += ".py"
            if not j.sal.fs.exists(tpath):
                for item in j.sal.fs.listFilesInDir("%s/tests" % self._dirpath, recursive=False, filter="*.py"):
                    bname = j.sal.fs.getBaseName(item)
                    if "_" in bname:
                        bname2 = "_".join(bname.split("_", 1)[1:])  # remove part before first '_'
                    else:
                        bname2 = bname
                    if bname2.startswith(name):
                        self.__test_run(name=bname, obj_key=obj_key, **kwargs)
                        return
                return self._test_error(
                    name, RuntimeError("Could not find, test:%s in %s/tests/" % (name, self._dirpath)))

            self._logger.debug("##: path: %s\n\n" % tpath)
        else:
            items = [j.sal.fs.getBaseName(item) for item in
                     j.sal.fs.listFilesInDir("%s/tests" % self._dirpath, recursive=False, filter="*.py")]
            items.sort()
            for name in items:
                self.__test_run(name=name, obj_key=obj_key, **kwargs)

            return

        method = j.tools.codeloader.load(obj_key=obj_key, path=tpath)
        self._logger.debug("##:LOAD: path: %s\n\n" % tpath)
        try:
            res = method(self=self, **kwargs)
        except Exception as e:
            j.errorhandler.try_except_error_process(e, die=False)
            self.__class__._test_runs_error[name] = e
            return e
        self.__class__._test_runs[name] = res
        return res

    def __str__(self):
        # out = str(self.__class__)+"\n"
        out = "%s\n"%self.__class__._location
        try:
            out += "%s\n%s\n"%(self.__class__,str(j.data.serializers.yaml.dumps(self._ddict)))
        except Exception as e:
            pass
        return out

    __repr__ = __str__
