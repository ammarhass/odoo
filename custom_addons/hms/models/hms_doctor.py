from odoo import models, fields

class HmsDoctor(models.Model):
    _name = 'hms.doctor'

    name= fields.Char()
    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Image()
    patient_ids = fields.Many2many('hms.patient')