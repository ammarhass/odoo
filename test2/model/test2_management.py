from odoo import models, fields

class Test2(models.Model):
    _name = 'test2.test2'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")