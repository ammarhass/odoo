from odoo import models, fields



class NewClass(models.Model):
    _inherit = 'res.partner'
    new_field = fields.Binary()