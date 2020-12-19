from celertix.models.celertix_orm import Model
from celertix.models.celertix_fields import *


class ResUers(Model):
    _name = 'res.user'
    _id = 0
    _migrate = True

    name = Char(string="Name")
    age = Integer(string="Age")
    department = Char(string="Department")
    blood_group = Char(string="BloodGroup")
    create_dt = Datetime(string="CreateDt")
    write_dt = Date(string="WriteDt")
    salary = Float(string="Salary")

