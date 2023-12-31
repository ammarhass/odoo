from odoo import models, fields, api


class HmsDepartment(models.Model):
    _name = 'hms.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many('hms.patient','department_id')