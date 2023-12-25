from odoo import fields, models, api


class EmployeeWizard(models.TransientModel):

    _name = 'employee.wizard.new'

    employees_ids = fields.Many2many('hr.employee')

    def update_employee(self):
        pass
