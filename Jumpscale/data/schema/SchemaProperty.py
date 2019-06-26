from Jumpscale import j

JSBASE = j.application.JSBaseClass


class SchemaProperty(j.application.JSBaseClass):
    def __init__(self):
        JSBASE.__init__(self)
        self.name = ""
        self.jumpscaletype = None
        self.comment = ""
        self.nr = 0
        self._default = None
        self.index = False  # as used in sqlite
        self.index_key = False  # is for indexing the keys
        self.index_text = False  # is for full text index
        self.unique = False  # to check if type is unique or not
        if self.name in ["schema"]:
            raise RuntimeError("cannot have property name:%s" % self.name)

    @property
    def capnp_schema(self):
        return self.jumpscaletype.capnp_schema_get(self.name_camel, self.nr)

    @property
    def default(self):
        if self._default:
            return self._default
        return self.jumpscaletype.default_get()

    @property
    def has_jsxobject(self):
        return self.is_list_jsxobject or self.is_jsxobject

    @property
    def is_list_jsxobject(self):
        if self.jumpscaletype.NAME == "list" and self.jumpscaletype.SUBTYPE.NAME == "JSXOBJ":
            return True
        return False

    @property
    def is_jsxobject(self):
        if self.jumpscaletype.BASETYPE == "JSXOBJ":
            return True
        return False

    @property
    def is_list(self):
        if self.jumpscaletype.NAME == "list":
            return True
        return False

    @property
    def default_as_python_code(self):
        try:
            c = self.jumpscaletype.python_code_get(self.default)
        except Exception as e:
            print("ERROR")
            print(e)
            raise (e)
        return c

    @property
    def name_camel(self):
        out = ""
        for item in self.name.split("_"):
            if out is "":
                out = item.lower()
            else:
                out += item.capitalize()
        return out

    @property
    def name_str(self):
        return "%-20s" % self.name

    @property
    def js_typelocation(self):
        return self.jumpscaletype._jsx_location

    def __str__(self):
        if not self.jumpscaletype.NAME == "list":
            out = "prop:%-25s %s" % (self.name, self.jumpscaletype.NAME)
        else:
            out = "prop:%-25s %s" % (self.name, self.jumpscaletype)

        # if self.pointer_type:
        #     out += " !%s" % self.pointer_type
        return out

    __repr__ = __str__
