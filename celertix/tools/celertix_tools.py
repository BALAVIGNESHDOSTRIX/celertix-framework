class CelertixxTools:
    @classmethod
    def parse_same_key_list(cls, keylist=[]):
        need_l = {}
        for v in keylist:
            for key,value in v.items():
                need_l.setdefault(key, []).append(value)
        return need_l if need_l else keylist
    
    @classmethod
    def cast_col_vals(cls, types=None, val_l=None):
        pass
    
    @classmethod
    def id_parseser(cls, id_dict=[]):
        return dict(id_dict[0])['id']
    
    