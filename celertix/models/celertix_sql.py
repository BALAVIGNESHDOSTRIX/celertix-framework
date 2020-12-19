CONDITIONAL_OPRATORS = {
    '=' : '=',
    '&' : 'AND',
    '!=': '!=',
    '|' : 'OR',
    'in': 'IN',
    'not in': 'NOT IN',
    'like': 'LIKE'
}


class CelertixSql:
    
    ''' 
        POSTGRESQL SCHEMA AND INFORMATION RELATED QURIES
    '''
    @classmethod
    def get_all_tables(cls):
        return "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"
    
    @classmethod
    def select_all_columns(cls, tbname=None):
        return "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'public' AND table_name = '{x}';".format(x=tbname)
    
    @classmethod
    def add_new_cols(cls, tbname=None, colist=None, dtypels=None):
        finstr = nrl = None 
        alc = "ALTER TABLE {tb} ".format(tb=tbname)
        if len(colist) == len(dtypels):
            for index,col in enumerate(colist):
                colstr = 'ADD COLUMN {coln} {dtype}'.format(coln=col, dtype=dtypels[index])
                nrl = nrl + ',' + colstr if nrl else colstr
        finstr = alc + nrl + ';'
        return finstr
    
    @classmethod
    def _insert_sql_(cls,tbname=None,colist=[],valist=[]):
        query = 'INSERT INTO {tbname} ({colist}) VALUES ({valist}) RETURNING ID;'.format(tbname=tbname, 
                                                                                  colist=", ".join(colist),
                                                                                  valist=", ".join(valist))
        return query
    
    @classmethod
    def _search_flds_where_(cls, tbname=None, colist=[], filters=[]):
        init_q = "SELECT {fields} FROM {tbname} WHERE {conditon}".format(fields=", ".join(colist), tbname=tbname, conditon="{condition}")
        cond_q = " {filter} {operator} {param} "
        fin_q = ""
        for filt in filters:
            if type(filt) == tuple:
                fin_q = fin_q + cond_q.format(filter=filt[0], operator=filt[1], param=filt[2])
            else:
                fin_q = fin_q + CONDITIONAL_OPRATORS.get(filt)
        return init_q.format(condition=fin_q)
    
    @classmethod
    def _update_sql(cls, tbname=None, vals=None, ids=None):
        valsx = ""
        if len(vals) > 1:
            for x in vals:
                valsx += x[0] + x[1] + str(x[2]) + ","
        return "UPDATE {tb_name} SET {vals} WHERE id = {_id};".format(tb_name=tbname, vals=valsx[:-1], _id=ids)
    
    @classmethod
    def _delete_sql(cls, tbname=None, ids=None):
        return "DELETE FROM {tbname} WHERE id = {ids};".format(tbname=tbname, ids=ids)