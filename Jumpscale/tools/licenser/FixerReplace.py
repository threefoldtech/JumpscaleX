from Jumpscale import j


GPL3 = """

# Copyright (C) 2019 :  TF TECH NV in Belgium see https://www.threefold.tech/
# This file is part of jumpscale at <https://github.com/threefoldtech>.
# jumpscale is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# jumpscale is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License v3 for more details.
#
# You should have received a copy of the GNU General Public License
# along with jumpscale or jumpscale derived works.  If not, see <http://www.gnu.org/licenses/>.
"""


JSBASE = j.application.JSBaseClass


class FixerReplacer(j.application.JSBaseClass):
    def file_process(self, path, write=False):
        out = ""
        C = j.sal.fs.readFile(path)
        if C.find("Copyright (C) 2019") != -1:
            return
        C = GPL3 + "\n\n" + C
        self._log_info("will copyright:%s" % path)
        if write:
            j.sal.fs.writeFile(path, C)

    def dir_process(self, path, extensions=["py"], recursive=True, write=False):
        path = j.sal.fs.pathNormalize(path)
        for ext in extensions:
            for p in j.sal.fs.listFilesInDir(path, recursive=recursive, filter="*.%s" % ext, followSymlinks=False):
                self._log_debug("process file:%s" % p)
                self.file_process(path=p, write=write)
