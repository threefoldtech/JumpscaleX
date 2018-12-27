

'''Definition of several primitive type properties (integer, string,...)'''

from .CustomTypes import *
from .CollectionTypes import *
from .PrimitiveTypes import *
from Jumpscale import j

class Types(j.application.JSBaseClass):
    
    __jslocation__ = "j.data.types"

    def _init(self):
        self.dict = Dictionary()
        self.list = List()
        self.guid = Guid()
        self.path = Path()
        self.bool = Boolean()
        self.boolean = Boolean()
        self.int = Integer()
        self.integer = self.int
        self.float = Float()
        self.string = String()
        self.str = self.string
        self.bytes = Bytes()
        self.multiline = StringMultiLine()
        self.set = Set()
        self.ipaddr = IPAddress()
        self.ipaddress = IPAddress()
        self.iprange = IPRange()
        self.ipport = IPPort()
        self.tel = Tel()
        self.yaml = YAML()
        self.json = JSON()
        self.email = Email()
        self.date = Date()
        self.numeric = Numeric()
        self.percent = Percent()
        self.hash = Hash()
        self.object = Object()
        self.jsobject = JSObject()
        self.url = Url()
        self.enumerations = {}

        self._dict = Dictionary
        self._list = List
        self._guid = Guid
        self._path = Path
        self._bool = Boolean
        self._int = Integer
        self._float = Float
        self._string = String
        self._bytes = Bytes
        self._multiline = StringMultiLine
        self._set = Set
        self._ipaddr = IPAddress
        self._iprange = IPRange
        self._ipport = IPPort
        self._tel = Tel
        self._yaml = YAML
        self._json = JSON
        self._email = Email
        self._date = Date
        self._numeric = Numeric
        self._percent = Percent
        self._hash = Hash
        self._object = Object
        self._jsobject = JSObject
        self._url = Url
        self._enumeration = Enumeration

        self.types_list = [self.bool, self.dict, self.list, self.bytes,
                           self.guid, self.float, self.int, self.multiline,
                           self.string, self.date, self.numeric, self.percent, self.hash, self.object, self.jsobject,
                           self.url]

    def type_detect(self, val):
        """
        check for most common types
        """
        for ttype in self.types_list:
            if ttype.check(val):
                return ttype
        raise RuntimeError("did not detect val for :%s" % val)

    def get_custom(self, ttype, **kwargs):
        """
        e.g. for enum, but there can be other types in future who take certain input
        :param ttype:
        :param kwargs: e.g. values="red,blue,green" can also a list for e.g. enum
        :return:

        e.g. for enumeration

        j.data.types.get_custom("e",values="blue,red")

        """
        ttype = ttype.lower().strip()
        if ttype in ["e","enum"]:
            cl = self._enumeration
            cl= cl(values=kwargs["values"])
            self.enumerations[cl._md5] = cl
            return self.enumerations[cl._md5]
        else:
            raise j.exceptions.RuntimeError("did not find custom type:'%s'" % ttype)


    def get(self, ttype, return_class=False):
        """
        type is one of following
        - s, str, string
        - i, int, integer
        - f, float
        - b, bool,boolean
        - tel, mobile
        - d, date
        - n, numeric
        - h, hash       #set of 2 int
        - p, percent
        - o, jsobject
        - ipaddr, ipaddress
        - ipport, tcpport
        - iprange
        - email
        - multiline
        - list
        - dict
        - yaml
        - set
        - guid
        - url, u
        - e,enum        #enumeration
        """
        ttype = ttype.lower().strip()
        if ttype in ["s", "str", "string"]:
            res = self._string
        elif ttype in ["i","int", "integer"]:
            res = self._int
        elif ttype in ["f","float"]:
            res = self._float
        elif ttype in ["o","obj","object"]:
            res = self._object
        elif ttype in ["b","bool", "boolean"]:
            res = self._bool
        elif ttype in ["tel", "mobile"]:
            res = self._tel
        elif ttype in ["ipaddr", "ipaddress"]:
            res = self._ipaddr
        elif ttype in ["iprange", "ipaddressrange"]:
            res = self._iprange
        elif ttype in ["ipport", "ipport"]:
            res = self._ipport
        elif ttype in ["jo", "jsobject"]:
            res = self._jsobject
        elif ttype == "email":
            res = self._email
        elif ttype == "multiline":
            res = self._multiline
        elif ttype in ["d", "date"]:
            res = self._date
        elif ttype in ["h", "hash"]:
            res = self._hash
        elif ttype in ["p", "perc","percent"]:
            res = self._percent
        elif ttype in ["n", "num","numeric"]:
            res = self._numeric
        elif ttype.startswith("l"):
            tt = self._list() #need to create new instance
            if return_class:
                raise RuntimeError("cannot return class if subtype specified")
            if len(ttype)==2:
                tt.SUBTYPE  = self.get(ttype[1],return_class=True)()
                return tt
            elif len(ttype)==1:
                assert tt.SUBTYPE == None
                return tt
            else:
                raise RuntimeError("list type len needs to be 1 or 2")
        elif ttype == "dict":
            res = self._dict
        elif ttype == "yaml":
            res = self._yaml
        elif ttype == "json":
            res = self._json
        elif ttype == "set":
            res = self._set
        elif ttype == "guid":
            res = self._guid
        elif ttype == "url" or ttype=="u":
            res = self._url
        else:
            raise j.exceptions.RuntimeError("did not find type:'%s'" % ttype)

        if return_class:
            return res
        else:
            return res()


    def test(self, name=""):
        """
        js_shell 'j.data.types.test()'

        if want run specific test ( write the name of test ) e.g. j.data.schema.test(name="base")
        """
        self._test_run(name=name)


    def fix(self,val,default):
        """
        will convert val to type of default

        , separated string goes to [] if default = []
        """
        if val is None or val == "" or val==[]:
            return default

        if j.data.types.list.check(default):
            res=[]
            if j.data.types.list.check(val):
                for val0 in val:
                    if val0 not in res:
                        res.append(val0)
            else:
                val=str(val).replace("'","")
                if "," in val:
                    val=[item.strip() for item in val.split(",")]
                    for val0 in val:
                        if val0 not in res:
                            res.append(val0)
                else:
                    if val not in res:
                        res.append(val)
        elif j.data.types.bool.check(default):
            if str(val).lower() in ['true',"1","y","yes"]:
                res=True
            else:
                res=False
        elif j.data.types.int.check(default):
            res=int(val)
        elif j.data.types.float.check(default):
            res=int(val)
        else:
            res=str(val)
        return res
