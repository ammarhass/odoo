from odoo import models, fields, api


class RealEstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Tag"
    _order = "name"
    name = fields.Char("Name")
    color = fields.Integer("Color Index")
    _sql_constraints = [('name_uniq', 'unique (name)', "the name must be unique")]