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
from .JSConfigBase import JSConfigBase

"""
classes who use JSXObject for data storage but provide nice interface to enduser
"""


class JSConfig(JSConfigBase):
    def _init_pre(self, jsxobject=None, datadict={}, name=None, **kwargs):
        self._triggers = []

        # get the model from the parent if not there use the SCHEMATEXT
        if self._parent and "_model" in self._parent.__dict__:
            self._model = self._parent._model
        else:

            if "_SCHEMATEXT" in self.__class__.__dict__:
                s = self.__class__._SCHEMATEXT
            else:
                s = self._parent.__class__._SCHEMATEXT

            # is a fall back for situation we want to use a JSConfig class without factory JSConfigs
            self._model = j.application.bcdb_system.model_get(schema=s)

        # that way the triggers can know about this class and can call the triggers on this level
        self._model._kosmosinstance = self

        if jsxobject:
            self._data = jsxobject
        else:
            jsxobjects = []
            if name:
                jsxobjects = self._model.find(name=name)
            if len(jsxobjects) > 0:
                self._data = jsxobjects[0]
            else:
                self._data = self._model.new()  # create an empty object

        if datadict:
            self._data_update(datadict)

        if name and self._data.name != name:
            self._data.name = name

    @property
    def name(self):
        return self._data.name

    @property
    def _id(self):
        return self._data.id

    def _data_update(self, datadict):
        """
        will not automatically save the data, don't forget to call self.save()

        :param kwargs:
        :return:
        """
        # ddict = self._data._ddict  # why was this needed? (kristof)
        self._data._data_update(datadict=datadict)

    def delete(self):
        self._delete()

    def _delete(self):
        self._triggers_call(self, "delete")
        assert self._model
        self._model.delete(self._data)
        if self._parent:
            if self._data.name in self._parent._children:
                del self._parent._children[self._data.name]
        self._triggers_call(self, "delete_post")

    def save(self):
        self.save_()

    def save_(self):
        assert self._model
        self._triggers_call(self, "save")
        self._data.save()
        self._triggers_call(self, "save_post")

    def edit(self):
        """

        edit data of object in editor
        chosen editor in env var: "EDITOR" will be used

        :return:

        """
        path = j.core.tools.text_replace("{DIR_TEMP}/js_baseconfig_%s.toml" % self.__class__._location)
        data_in = self._data._toml
        j.sal.fs.writeFile(path, data_in)
        j.core.tools.file_edit(path)
        data_out = j.sal.fs.readFile(path)
        if data_in != data_out:
            self._log_debug(
                "'%s' instance '%s' has been edited (changed)" % (self._parent.__jslocation__, self._data.name)
            )
            data2 = j.data.serializers.toml.loads(data_out)
            self._data.data_update(data2)
        j.sal.fs.remove(path)

    def _dataprops_names_get(self, filter=None):
        """
        e.g. in a JSConfig object would be the names of properties of the jsxobject = data
        e.g. in a JSXObject would be the names of the properties of the data itself

        :return: list of the names
        """
        return self._filter(filter=filter, llist=self._model.schema.propertynames)
