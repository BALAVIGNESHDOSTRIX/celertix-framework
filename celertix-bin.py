'''
        DEVELOPER NAME: M.BALAVIGNESH
        
        START DATE: 16/08/2020

'''
from pathlib import Path
from celertix.models.celertix_orm import Database, Model
from celertix.configs.celertix_dbconfig import DB_CONFIG as dbcon
from celertix.configs.celertix_module_config import root_path 
from celertix.tools.celertix_global import clx,Clxauth,clxuniv
from celertix.models.celertix_class_registry import ClassRegistry as clsreg
from celertix.tools.celertix_tools import CelertixTools as tools 

async def create_new_tables(tblist=[]):
    newtables = clsreg.NewTablesParser(tblist=list(tblist), tbobjdict=clxuniv.env)
    for tbl in newtables:
        tbclass = clxuniv.env.get(tbl)
        if tbclass._migrate:
            query = await tbclass.createtb()
            await clxuniv.environ._execute(query)
            
async def update_new_columns(tblist=[]):
    for tbls in tblist:
        cols = await clxuniv.environ.get_all_cols(tbls[0])
        colsl = tools.parse_same_key_list(cols)
        sqlq = clxuniv.env[str(tbls[0]).replace('_', '.')]._migrate_new_cols(existcolist=colsl.values())
        if sqlq:
            await clxuniv.environ._execute(sqlq)
            

@clx.listener('before_server_start')
async def register_db(clx, loop): 
    moduels = clsreg.Module_Loader(package_dir = Path(__file__).resolve().parent)
    clxuniv['environ'] = Database(dbuser=dbcon.get('dbuser'),userpass=dbcon.get('dbpass'),dbname=dbcon.get('dbname'), dbhost=dbcon.get('dbhost'), dbport=dbcon.get('dbport'), maxquery=4000, maxinclife=5000)
    clxuniv['envpool'] = await clxuniv.environ.register_db
    clxuniv['env'] = clsreg.InstanceEnviron(tbclass_l=moduels)
    tables = await clxuniv.environ.tables()
    tblist = tools.parse_same_key_list(keylist=tables)
    tblist = tblist.values() if tables else []
    await create_new_tables(tblist=tblist)
    await update_new_columns(tblist=tblist)
    
# @clx.listener('before_server_stop')
# async def deregister_db(clx, loop):
#     await clxuniv.environ.unregister_db()
    

if __name__ == "__main__":
    import os
    os.path.dirname(os.path.realpath('celertix-bin.py'))
    clx.run(host="0.0.0.0", port=8000, debug=True)
