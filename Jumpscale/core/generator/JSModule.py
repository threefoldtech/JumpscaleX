from .JSClass import JSClass

# from .JSGroup import JSGroup
import os
import re
from pathlib import Path

LOCATIONS_ERROR = ["j.errorhandler", "j.core", "j.application", "j.exceptions", "j.logger", "j.application", "j.dirs"]


def _check_jlocation(location, classname=""):
    """
    will return true if the location is ok
    :param location:
    :return:
    """
    if classname == "JSBaseClassConfig" or not location.startswith("j."):
        return False
    location = location.lower()
    for item in LOCATIONS_ERROR:
        if location.startswith(item):
            return False
    return True


class LineChange:
    def __init__(self, jsmodule, line_nr, line_old, line_new):
        self.jsmodule = jsmodule
        self._j = self.jsmodule._j
        self.line_old = line_old
        self.line_new = line_new
        self.line_nr = line_nr

    def __repr__(self):
        out = "##### line change [%s]\n\n" % self.line_nr
        out += "- %s\n" % self.jsmodule.path
        out += "- line old : '%s'\n" % (self.line_old)
        out += "- line new : '%s'\n" % (self.line_new)
        return out

    __str__ = __repr__


class JSModule:
    def __init__(self, md, path, jumpscale_repo_name, js_lib_path):
        name = os.path.basename(path)
        name = name[:-3]
        self.jsgroup = None
        self._j = md._j
        self.md = md
        self.path = path
        self.name = name
        self.jumpscale_repo_name = jumpscale_repo_name
        self.lines_changed = {}
        self.classes = {}
        self.js_lib_path = js_lib_path

    def jsclass_get(self, name):
        """
        is file in module
        :param name:
        :return:
        """
        if not name in self.classes:
            self.classes[name] = JSClass(self, name)
        return self.classes[name]

    def line_change_add(self, nr, line_old, line_new):
        self.lines_changed[nr] = LineChange(
            self, nr, line_old, line_new
        )  # MEANS WE CANNOT DO CHANGE OVER LINE MORE THAN ONCE, but is ok !

    def write_changes(self):
        """
        write the changed lines back to the file
        :return:
        """
        if self.lines_changed != {}:
            lines = self.code.split("\n")
            for nr, lc in self.lines_changed.items():
                lines[nr] = lc.line_new
            code_out = "\n".join(lines)
            file = open(self.path, "w")
            file.write(code_out)
            file.close()

    @property
    def location(self):
        for name, klass in self.classes.items():
            if klass.location != "":
                return klass.location
        return ""

    @property
    def jsgroup_name(self):
        if self.location != "":
            splitted = self.location.split(".")
            if len(splitted) > 3:
                return splitted[1:-1]
            return splitted[1:2]
        return ""

    @property
    def jname(self):
        if self.location != "":
            splitted = self.location.split(".")
            return splitted[-1]
        return ""

    @property
    def code(self):
        p = Path(self.path)
        try:
            return p.read_text()
        except Exception as e:
            print("WARNING: following text has non ascii chars inside:%s" % self.path)
            return self._j.core.text.strip_to_ascii(p.read_bytes().decode())
            #
            # self._j.shell()
            # print("COULD NOT READ TEXT FROM:%s"%self.path)
            # # print(str(e))
            # raise e

    def process(self, methods_find=False, action_method=None, action_args={}):
        """
        when action method specified will do:
            action_args = action_method(jsmodule=self,classobj=classobj,line=line,args=action_args)

        """
        res = {}
        classobj = None
        code = self.code
        nr = -1
        for line in code.split("\n"):
            nr += 1
            if line.startswith("class "):
                classname = line.replace("class ", "").split(":")[0].split("(", 1)[0].strip()
                classobj = self.jsclass_get(classname)

            if line.find("__jslocation__") != -1:
                if classobj is None:
                    raise j.exceptions.Base("Could not find class in '%s' while loading jumpscale lib." % line)
                if line.find("=") != -1 and line.find("IGNORELOCATION") == -1:
                    location = line.split("=", 1)[1].replace('"', "").replace("'", "").strip()
                    if _check_jlocation(location):
                        if classobj.location != "":
                            raise j.exceptions.Base("there cannot be 2 jlocations:'%s' in class:%s" % (location, self))
                        classobj.location = location
                        self.name = classname

            if line.find("__imports__") != -1:
                if classobj is None:
                    raise j.exceptions.Base("Could not find class in %s while loading jumpscale lib." % path)
                importItems = line.split("=", 1)[1].replace('"', "").replace("'", "").strip()
                classobj.imports = [item.strip() for item in importItems.split(",") if item.strip() != ""]

            if methods_find and classobj is not None:
                if line.startswith("    def "):
                    pre = line.split("(", 1)[0]
                    method_name = pre.split("def", 1)[1].strip()
                    if not method_name.startswith("_"):
                        classobj.method_add(nr, method_name)

            if action_method is not None:
                action_args = action_method(jsmodule=self, classobj=classobj, nr=nr, line=line, args=action_args)

        return action_args

    @property
    def importlocation(self):
        """
        :return: e.g. clients.tarantool.TarantoolFactory
        """
        js_lib_path = os.path.dirname(self.js_lib_path.rstrip("/"))  # get parent
        c = self.path.replace(js_lib_path, "").lstrip("/")
        # c is e.g. clients/tarantool/TarantoolFactory.py
        c = c[:-3]  # remove the py part
        c = c.replace("/", ".")
        return c

    @property
    def markdown(self):
        out = str(self)
        if self.lines_changed != {}:
            out += "\n#### lines changed\n\n"
            for nr, line in self.lines_changed.items():
                out += "- %-4s %s" % (nr, line)
        for name, klass in self.classes.items():
            out += klass.markdown
        return out

    def __repr__(self):
        out = "## Module: %s\n\n" % (self.name)
        out += "- path: %s\n" % (self.path)
        out += "- importlocation: %s\n\n" % (self.importlocation)
        return out

    __str__ = __repr__
