import sys, inspect, os, imp
from copy import deepcopy
from celertix.configs.celertix_module_config import root_path, models_path, route_path
from celertix.configs.celertix_module_config import root_entry
from celertix.safe_eval.celertix_module_wildcard import WCRDL
from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from .celertix_orm import Model
from .celertix_fields import *

dynamic_modules = dict()

class ClassRegistry: 
    
    @classmethod 
    def Module_Loader(cls, package_dir):
        tbclassess = []
        parent_root = str(package_dir) + str(root_entry) + str(root_path)
        for pkgs in os.listdir(parent_root):
            if pkgs not in WCRDL:
                inside_root = parent_root + str(root_entry) + str(pkgs)
                for inside in os.listdir(inside_root):
                    if inside not in WCRDL:
                        if inside == str(models_path):
                            model_ins_root = inside_root + str(root_entry) + str(models_path)
                            for minside in os.listdir(model_ins_root):
                                if minside not in WCRDL:
                                    module = import_module(root_path + "." + pkgs + "." + models_path + "." + str(minside[:minside.index('.')]), ".")
                                    for m in inspect.getmembers(module, inspect.isclass):
                                        if Model in m[1].__bases__:
                                            classobj = getattr(module, str(m[0]))
                                            tbclassess.append(classobj)
        return tbclassess
                            
    @classmethod 
    def InstanceEnviron(cls, tbclass_l=[]):
        environ_dict = {}
        for clsobj in tbclass_l:
            if clsobj._migrate:
                environ_dict[clsobj._name] = clsobj()
        return environ_dict
    
    @classmethod
    def DaemonCrDict(cls, tbclass_l=[]):
        daemoncr_dict = {}
        for clsobj in tbclass_l:
            daemoncr_dict[clsobj._name] = clsobj._name
        return daemoncr_dict
        
    @classmethod
    def NewTablesParser(cls, tblist=[], tbobjdict={}):
        if tblist:
            return [tb for tb in list(tbobjdict.keys()) if str(tb).replace(".", "_") not in tblist[0]]
        else:
            return [tb for tb in list(tbobjdict.keys())]