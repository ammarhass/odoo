from odoo import models, fields, api

class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    new_field = fields.Binary()



