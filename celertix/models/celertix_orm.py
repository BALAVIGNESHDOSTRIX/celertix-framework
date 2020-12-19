import inspect
from asyncpg  import create_pool, connect
from .celertix_sql import *
from .celertix_sql import CelertixSql as sql 
from .celertix_fields import *
from ..tools.celertix_global import clx
from ..tools.celertix_tools import CelertixTools as gtol


class Database:
    def __init__(self, dbuser=None, userpass=None, dbname=None, dbhost=None, dbport=None,maxquery=None,maxinclife=None):
        self.dbuser = dbuser
        self.userpass = userpass
        self.dbname = dbname
        self.dbhost = dbhost
        self.dbport = dbport
        self.maxquery = maxquery
        self.max_inac_con_life = maxinclife
        self.gresenv = None 

    @property
    async def register_db(self):
        return await connect(user=self.dbuser, password=self.userpass,
        host=self.dbhost, database=self.dbname,
        port=self.dbport)

    async def unregister_db(self, gresenvpool):
        async with gresenvpool.acquire() as dbcon:
            await dbcon.close()
            
    @classmethod
    def clspartum(cls):
        return cls()
  
    async def _execute(self, sqlcommand=None, conpool=None):
        return [dict(x) for x in await conpool.fetch(sqlcommand) if x]

    async def tables(self, conpool):
        return await self._execute(sqlcommand=sql.get_all_tables(), conpool=conpool)
    
    async def get_all_cols(self, conpool, tbname):
        return await self._execute(sqlcommand=sql.select_all_columns(tbname=tbname), conpool=conpool)
    

class Model(Database):
    def __init__(self, **kwargs):
        self._data = {'id': None}
        for key, value in kwargs.items():
            self._data[key] = value

    def __getattribute__(self, key):
        _data = object.__getattribute__(self, '_data')
        if key in _data:
            return _data[key]
        return object.__getattribute__(self, key)


    @classmethod
    def _get_name(cls):
        return str(cls._name).replace('.', '_')
    
    #Migrate Fields to Database
    @classmethod
    def _migrate_new_cols(cls, existcolist=[]):
        colist = []
        dtype = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Char) or isinstance(field, Integer) or \
            isinstance(field, Float) or isinstance(field, Datetime) or \
            isinstance(field, Date):
                if name not in tuple(list(existcolist)[0]):
                    colist.append(name)
                    dtype.append(field.data_type)
            elif isinstance(field, ForeignKey):
                if name not in tuple(list(existcolist)[0]):
                    colist.append(name + "_id")
                    dtype.append("INTEGER")
        if colist and dtype:
            return sql.add_new_cols(tbname=cls._get_name(), colist=colist, dtypels=dtype)
        return None
            

    @classmethod
    def _get_create_sql(cls):
        fields = [
            ("id", "SERIAL PRIMARY KEY")
        ]

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Char) or isinstance(field, Integer) or \
            isinstance(field, Float) or isinstance(field, Datetime) or \
            isinstance(field, Date):
                fields.append((name, field.data_type))
            elif isinstance(field, ForeignKey):
                fields.append((name + "_id", "INTEGER"))
        fields = [" ".join(x) for x in fields]
        return CREATE_TABLE_SQL.format(name=cls._get_name(), fields=", ".join(fields))

    @classmethod
    def _get_select_where_sql(cls, args=[]):
        '''
            search[('name', '=', 10)]
        '''
        fld_types = {}
        new_filter = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Char) or isinstance(field, Integer) or \
            isinstance(field, Float) or isinstance(field, Datetime) or \
            isinstance(field, Date):
                fld_types[name] = field.data_type
        for item in args:
            if type(item) == tuple:
                if fld_types.get(item[0]) == "INTEGER":
                    new_filter.append((item[0], item[1], int(item[2])))
                if fld_types.get(item[0]) == "VARCHAR":
                    new_filter.append((item[0], item[1], "'{x}'".format(x=str(item[2]))))
                if fld_types.get(item[0] == "BOOLEAN"):
                    new_filter.append((item[0], item[1], 'true' if item[2] else 'false'))
                if fld_types.get(item[0] in ["TIMESTAMP","DATE"]):
                    new_filter.append((item[0], item[1],  item[2]))
                if fld_types.get(item[0] == "DECIMAL"):
                    new_filter.append((item[0], item[1],  float(item[2])))
                if item[0] == 'id':   
                    new_filter.append((item[0], item[1], item[2]))
            else:
                new_filter.append(item)
        fld_types['id'] = "INTEGER"
        return sql._search_flds_where_(tbname=cls._get_name(), colist=fld_types.keys(), filters=new_filter)
            
    async def create(self, vals={}):
        cls = self.__class__
        newObj = cls.clspartum()
        newObj._fld_value_setter(vals=vals)
        fields, values = newObj._fld_value_casting(classmebers=inspect.getmembers(cls))
        sqlQ = sql._insert_sql_(tbname=cls._get_name(), colist=fields, valist=values)
        res = await clx.config.environ._execute(sqlQ, clx.config.envpool)
        return await newObj.browse(ids=[int(gtol.id_parseser(res))])
        
    
    async def write(self, vals={}):
        cls = self.__class__
        self._fld_value_setter(vals=vals)
        fields, values = self._fld_value_casting(classmebers=inspect.getmembers(cls))
        combin_l = []
        for index,fld in enumerate(fields):
            combin_l.append((fld, '=', values[index]))
        query = sql._update_sql(tbname=cls._get_name(), vals=combin_l, ids=self._id)
        res = await clx.config.environ._execute(query, clx.config.envpool)
        return True
    
    async def unlink(self):
        cls = self.__class__
        query = sql._delete_sql(tbname=cls._get_name(), ids=self._id)
        await clx.config.environ._execute(query, clx.config.envpool)
        

    async def browse(self, ids=[]):
        #tbclass 
        cls = self.__class__
        if type(ids) == list:
            tup = tuple(ids)
            if len(tup) > 1:
                query = self._get_select_where_sql(args=[('id', 'in', tup)])                                      
            else:
                query = self._get_select_where_sql(args=[('id', '=', tup[0])])
            res = await clx.config.environ._execute(query, clx.config.envpool)
            return ObjValsMapper(cls, res).tbobj_lx()
            
    async def search(self, args=[], limit=None):
        cls = self.__class__
        query = self._get_select_where_sql(args=args)
        res = await clx.config.environ._execute(query, clx.config.envpool)
        return ObjValsMapper(cls, res).tbobj_lx()
        
    async def createtb(self):
        return self._get_create_sql()
    
    def _fld_value_casting(self, classmebers=[]):
        ''' 
            Make the Column names related Values. If The Values Need to Cast that Also 
            Done in this Method
        '''
        col_l = []
        val_l = []
        for name, field in classmebers:
            if isinstance(field, Char):
                val = getattr(self, name)
                if not isinstance(val, Char):
                    col_l.append(name)
                    val_l.append("'{x}'".format(x=str(val)))
            
            if isinstance(field, Integer):
                val = getattr(self, name)
                if not isinstance(val, Integer):
                    col_l.append(name)
                    val_l.append(str(val))
                    
            if isinstance(field, Datetime):
                val = getattr(self, name)
                if not isinstance(val, Datetime):
                    col_l.append(name)
                    val_l.append("'{x}'".format(x=str(val)))
                
            if isinstance(field, Float):
                val = getattr(self, name)
                if not isinstance(val, Float):
                    col_l.append(name)
                    val_l.append(str(val))
                    
            if isinstance(field, Date):
                val = getattr(self, name)
                if not isinstance(val, Date):
                    col_l.append(name)
                    val_l.append("'{x}'".format(x=str(val)))
                
        return col_l,val_l
    
    def _fld_value_setter(self, vals={}):
        for fld, value in vals.items():
            setattr(self, fld, value)
            

class ObjValsMapper:
    def __init__(self, clsobj=None, result_l=[]):
        self.tbobj_l = []
        for res in result_l:
            tbobj = clsobj.clspartum()
            for fld, value in res.items():
                if fld == 'id':
                    setattr(tbobj, '_id', value)
                setattr(tbobj, fld, value)
            self.tbobj_l.append(tbobj)
        
    def tbobj_lx(self):
        return self.tbobj_l if len(self.tbobj_l) > 1 else self.tbobj_l[0] or False