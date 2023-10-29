from odoo import models, fields, api
from datetime import date, time


class HmsPatient(models.Model):
    _name = 'hms.patient'

    first_name = fields.Char(string="First name")
    last_name = fields.Char(string="Last name")
    birth_date = fields.Date()
    history = fields.Html(string="History")
    blood_type = fields.Selection([('a', 'A'),('-o','-O'),('+o', '+o')], string="Blood Type")
    pcr = fields.Boolean(string="PCR")
    cr_ratio = fields.Float(string="CR Ratio")
    image = fields.Image(string="Image")
    address = fields.Text(string="Address")
    age = fields.Integer("Age", default=None)
    department_id = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related='department_id.capacity')
    doctor_ids = fields.Many2many('hms.doctor')
    patient_state = fields.Selection([('u','Undetermined'),('g','Good'),('f','Fair'),('s','Serious')])
    log_ids = fields.One2many('log.history','create_id')

    @api.onchange('patient_state')
    def _on_change_state(self):
        if not self.patient_state:
            return {}
        return {
            'warning': {'title':'Patient', 'message':'State changed to NEW_STATE'}
        }

    @api.onchange('age')
    def _on_change_age(self):
        if self.age == 0:
            return {}
        if self.age < 30:
            self.pcr = True
        else:
            self.pcr = False

        return {
            'warning' : {'title': 'pcr', 'message' :'pcr has been checked'}
        }


class LogHistory(models.Model):
    _name = 'log.history'

    description = fields.Text()
    create_id = fields.Many2one('hms.patient')
    name = fields.Char()
    date = fields.Date(default=date.today())
