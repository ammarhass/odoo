from odoo import models, fields, api
from odoo.exceptions import UserError



class Partner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        comodel_name='hms.patient',
        string=' Patient',
        required=False)


    api.model
    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise UserError("Customer can't be deleted, email already exist in hms_patient")
            super().unlink()


    @api.constrains('email')
    def check_email(self):
        search_result = self.env['hms.patient'].search([('email', '=', self.email)])
        # print('search_result', search_result)
        if search_result:
            raise UserError("Email already exist")