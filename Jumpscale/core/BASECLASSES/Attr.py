# Copyright (C) July 2018:  TF TECH NV in Belgium see https://www.threefold.tech/
# In case TF TECH NV ceases to exist (e.g. because of bankruptcy)
#   then Incubaid NV also in Belgium will get the Copyright & Authorship for all changes made since July 2018
#   and the license will automatically become Apache v2 for all code related to Jumpscale & DigitalMe
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
# LICENSE END


from Jumpscale import j

### CLASS DEALING WITH THE ATTRIBUTES SET & GET


class Attr:
    def __getattr__(self, name):
        # if private or non child then just return

        if name in self._children:
            return self._children[name]

        if isinstance(self, j.application.JSConfigClass):
            if name in self._model.schema.propertynames:
                return self._data.__getattribute__(name)

        if isinstance(self, j.application.JSConfigsClass):

            if (
                name.startswith("_")
                or name in self._methods_names_get()
                or name in self._properties_names_get()
                or name in self._dataprops_names_get()
            ):
                return self.__getattribute__(name)  # else see if we can from the factory find the child object

            r = self._get(name=name, die=False)
            if not r:
                raise j.exceptions.Base(
                    "try to get attribute: '%s', instance did not exist, was also not a method or property, was on '%s'"
                    % (name, self._key)
                )
            return r

        try:
            r = self.__getattribute__(name)
        except AttributeError as e:
            try:
                whereami = self._key
            except:
                whereami = self._name
            msg = "could not find attribute:%s in %s (error was:%s)" % (name, whereami, e)
            raise j.exceptions.Base(msg)

        return self.__getattribute__(name)

    def __setattr__(self, key, value):

        if key.startswith("_"):
            self.__dict__[key] = value
            return

        if isinstance(self, j.application.JSConfigClass):

            if key == "data":
                raise j.exceptions.Base("protected property:%s" % key)

            if "_data" in self.__dict__ and key in self._model.schema.propertynames:
                # if value != self._data.__getattribute__(key):
                # self._log_debug("SET:%s:%s" % (key, value))
                self._data.__setattr__(key, value)
                return

        if not self._protected or key in self._properties:
            self.__dict__[key] = value
        else:
            raise j.exceptions.Base("protected property:%s" % key)
