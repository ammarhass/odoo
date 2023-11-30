from odoo import models, fields, api


class StudentUpataWizard(models.TransientModel):

    _name = 'student.update.wizard'
    total_salary = fields.Float(string="Total Salary")

    def update_student_salary(self):
        print("Successfully click the button on wizard")
        self.env['iti.student'].browse(self._context.get("active_ids")).write({'salary': self.total_salary})
        self.env['iti.student'].browse(self._context.get("active_ids")).write({'level': 4})
        print("Check if record exist")
        print(self.env['student.update.wizard'].browse([1]))
        return True

