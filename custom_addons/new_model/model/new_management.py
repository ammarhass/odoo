from odoo import models, fields



class NewManagement(models.Model):
    _name = 'new'
    _description = 'new management'

    name = fields.Char(string="Name")
    new_field = fields.Char(string="new_field")