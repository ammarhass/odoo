from odoo import models, fields, api, Command
from datetime import date, datetime


class HmsPatient(models.Model):
    _name = 'hms.patient'

    first_name = fields.Char(string="First name")
    last_name = fields.Char(string="Last name")
    email = fields.Char(string="Email")
    birth_date = fields.Date()
    history = fields.Html(string="History")
    blood_type = fields.Selection([('a', 'A'), ('-o', '-O'), ('+o', '+O')], string="Blood Type")
    pcr = fields.Boolean(string="PCR")
    cr_ratio = fields.Float(string="CR Ratio")
    image = fields.Image(string="Image")
    address = fields.Text(string="Address")
    age = fields.Integer("Age", default=None, compute='calc_age')
    department_id = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related='department_id.capacity')
    doctor_ids = fields.Many2many('hms.doctor')
    state = fields.Selection([('u', 'Undetermined'), ('g', 'Good'), ('f', 'Fair'), ('s', 'Serious')], default='u')
    log_ids = fields.One2many('log.history', 'create_id')

    _sql_constraints = [('email_uniq', 'unique(email)', "Email you entered already exist")]

    def change_blood(self):
        self.blood_type = 'a'

    def update_log(self, value):
        if value == 'u':
            self.state ='g'
            self.log_ids = [Command.create({'description': "patient state changed to Good"})]
        elif value == 'g':
            self.state = 'f'
            self.log_ids = [Command.create({'description': "patient state changed to Fair"})]
        elif value == 'f':
            self.state = 's'
            self.log_ids = [Command.create({'description': "patient state changed to Serious"})]
        elif value == 's':
            self.state = 'u'
            self.log_ids = [Command.create({'description': "patient state changed to Undetermined"})]

    def change_state(self):
        if self.state == 'u':
            self.update_log(self.state)
        elif self.state == 'g':
            self.update_log(self.state)
        elif self.state == 'f':
            self.update_log(self.state)
        elif self.state == 's':
            self.update_log(self.state)




    @api.model
    def create(self, vals_list):
        name_split = vals_list['first_name'].split()
        vals_list['email'] = f"{name_split[0][0]}{vals_list['last_name']}@gmail.com"
        return super().create(vals_list)

    def write(self, vals):

        # res = super().write(vals)
        if 'first_name' in vals and 'last_name' in vals :
            name_split = vals['first_name'].split()
            vals['email'] = f"{name_split[0][0]}{vals['last_name']}@gmail.com"

        elif 'first_name' in vals and self.last_name:
            name_split = vals['first_name'].split()
            print("name_split[0]", name_split[0])
            print(name_split[0][0])
            vals['email'] = f"{name_split[0][0]}{self.last_name}@gmail.com"

        elif 'last_name' in vals and self.first_name:
            name_split = self.first_name.split()
            print("name_split[0]", name_split[0])
            print(name_split[0][0])
            vals['email'] = f"{name_split[0][0]}{vals['last_name']}@gmail.com"

        return super().write(vals)

    @api.onchange('patient_state')
    def _on_change_state(self):
        if not self.patient_state:
            return {}
        return {
            'warning': {'title': 'Patient', 'message': 'State changed to NEW_STATE'}
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
            'warning': {'title': 'pcr', 'message': 'pcr has been checked'}
        }

    @api.depends('birth_date')
    def calc_age(self):
        for rec in self:
            current_year = date.today()
            if rec.birth_date:
                rec.age = current_year.year - rec.birth_date.year
            else:
                rec.age = None


class LogHistory(models.Model):
    _name = 'log.history'

    description = fields.Text()
    create_id = fields.Many2one('hms.patient')
