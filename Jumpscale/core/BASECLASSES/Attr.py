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
                raise RuntimeError(
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
            msg = "could not find attribute:%s in %s" % (name, whereami)
            raise RuntimeError(msg)

        return self.__getattribute__(name)

    def __setattr__(self, key, value):

        if key.startswith("_"):
            self.__dict__[key] = value
            return

        if isinstance(self, j.application.JSConfigClass):

            assert "data" not in self.__dict__

            if "_data" in self.__dict__ and key in self._model.schema.propertynames:
                # if value != self._data.__getattribute__(key):
                self._log_debug("SET:%s:%s" % (key, value))
                self._data.__setattr__(key, value)
                return

        if not self._protected or key in self._properties:
            self.__dict__[key] = value
        else:
            raise RuntimeError("protected property:%s" % key)