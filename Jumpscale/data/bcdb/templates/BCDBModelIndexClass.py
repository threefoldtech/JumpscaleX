from Jumpscale import j

class {{BASENAME}}:

    def _init_index(self):
        self.index = None
        {%- if index.active %}
        self._log_info("init index:%s"%self.schema.url)

        p = j.clients.peewee

        db = self.bcdb.sqlclient.sqlitedb
        # print(db)

        class BaseModel(p.Model):
            class Meta:
                print("*%s"%db)
                database = db

        class Index_{{schema.key}}(BaseModel):
            id = p.IntegerField(unique=True)
            nid = p.IntegerField(index=True) #need to store the namespace id
            {%- for field in index.fields %}
            {{field.name}} = p.{{field.type}}(index=True)
            {%- endfor %}

        self.index = Index_{{schema.key}}
        self.index.create_table(safe=True)

        {%- endif %}

    {% if index.active %}
    def index_set(self,obj):
        idict={}
        {%- for field in index.fields %}
        {%- if field.jumpscaletype.NAME == "numeric" %}
        idict["{{field.name}}"] = obj.{{field.name}}_usd
        {%- else %}
        idict["{{field.name}}"] = obj.{{field.name}}
        {%- endif %}
        {%- endfor %}
        assert obj.id
        assert obj.nid
        idict["id"] = obj.id
        idict["nid"] = obj.nid
        if not self.index.select().where(self.index.id == obj.id).count()==0:
            #need to delete previous record from index
            self.index.delete().where(self.index.id == obj.id).execute()
        self.index.insert(**idict).execute()


    def index_destroy(self,nid=None):
        """
        will remove all namespaces indexes
        :param nid:
        :return:
        """
        if nid:
            self.index.delete().where(self.index.nid == nid).execute()
        else:
            self.index.drop_table()
            self.index.create_table()
        self._index_keys_destroy(nid=nid)

    {% endif %}


    {%- if index.active_keys %}
    def index_keys_set(self,obj):
        {%- for property_name in index.fields_key %}
        val = obj.{{property_name}}
        if val not in ["",None]:
            val=str(val)
            # self._log_debug("key:{{property_name}}:%s:%s"%(val,obj.id))
            self._index_key_set("{{property_name}}",val,obj.id,nid=obj.nid)
        {%- endfor %}

    def index_keys_delete(self,obj):
        {%- for property_name in index.fields_key %}
        val = obj.{{property_name}}
        if val not in ["",None]:
            val=str(val)
            self._log_debug("delete key:{{property_name}}:%s:%s"%(val,obj.id))
            self._index_key_delete("{{property_name}}",val,obj.id,nid=obj.nid)
        {%- endfor %}


    {%- for property_name in index.fields_key %}
    def get_by_{{property_name}}(self,{{property_name}},nid=1):
        return self.get_from_keys({{property_name}}=str({{property_name}}),nid=nid)
    {%- endfor %}

    {%- endif %}
