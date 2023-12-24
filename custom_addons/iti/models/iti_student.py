from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, datetime


class ItiStudent(models.Model):
    _name = "iti.student"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(tracking=True)
    birthdate = fields.Date()
    tax = fields.Float(compute="calc_tax", store=False)
    salary = fields.Float()
    net_salary = fields.Float(compute="clac_tax")
    address = fields.Text()
    email = fields.Char(readonly=True)
    gender = fields.Selection([('m', "Male"), ('f', "Female")], default=None)
    accepted = fields.Boolean()
    level = fields.Integer()
    image = fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()
    track_id = fields.Many2one('iti.track')
    skills_ids = fields.Many2many('iti.skill', widget='many2many')
    grade_ids = fields.One2many('iti.grades', 'student_id')
    track_capacity = fields.Integer(related='track_id.capacity')
    state = fields.Selection([
        ('applied', 'Applied'),
        ('first', 'First Interview'),
        ('second', 'Second Interview'),
        ('passed', 'Passed'),
        ('rejected', 'Rejected')
    ], default='applied', Tracking=True)

    family_ids = fields.One2many('student.family','student_id','Family')
    # family_ids = fields.Many2many('student.family', string='Family')
    email_sent = fields.Boolean("Email Sent", default=False)
    student_seq = fields.Char("Student Code", readonly=1)


    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         "the name you entered already exist"),
        ('email_uniq', 'unique (email)', "the email you entered already exist")
    ]
    # def _action_send_email(self):
    #     students_ids = self.env['iti.student'].search([('email_sent', '=', False)])
    #     for student in students_ids:
    #         if student.mail_sent is False:




    @api.constrains("salary")
    def check_salary(self):
        if self.salary > 10000:
            raise UserError("salary is higher than 10000")

    @api.constrains("track_id")
    def checK_track_capacity(self):
        track_count = len(self.track_id.students_ids)
        track_capacity = self.track_id.capacity
        if track_count > track_capacity:
            raise UserError("Track is full")

    @api.model
    def create(self, vals_list):
        vals_list['student_seq'] = self.env['ir.sequence'].next_by_code("iti.student")
        name_split = vals_list['name'].split()
        vals_list['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        search_students = self.search([('email', '=', vals_list['email'])])
        track = self.env['iti.track'].browse(vals_list['track_id'])
        if track.is_open is False:
            raise UserError("Selected track is closed")
        if search_students:
            raise UserError("Email already exist")
        return super().create(vals_list)

    def write(self, vals):
        print("Entering write function")
        print(self.salary)

        if 'name' in vals:
            name_split = vals['name'].split()
            vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"

        if 'salary' in vals:
            x = vals['salary']
            print(x)
            vals['salary'] = x
            print(vals['salary'])
        print(self.level)
        return super().write(vals)

    # def unlink(self):
    #     for record in self:
    #         if record.state in ['passed', 'rejected']:
    #             raise UserError("You can't delete passed/rejected students")
    #         super().unlink()

    @api.depends('salary')
    def calc_tax(self):
        for rec in self:
            rec.tax = rec.salary * 0.20
            rec.net_salary = rec.salary - rec.tax

    def change_state(self):
        if self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':
            self.state = 'second'
        elif self.state in ['passed', 'rejected']:
            self.state = 'applied'
        self.message_post(body="user changed the state of {}".format(self.name))

        print(self.env.ref("iti.student_tree_view").read()[0])


    def set_passed(self):
        self.state = 'passed'

    def set_rejected(self):
        self.state = 'rejected'

    @api.onchange('gender')
    def _on_change_gender(self):
        domain = {'track_id': []}
        if not self.gender:
            # self.gender = 'm'
            return {}
        if self.gender == 'm':
            domain = {'track_id': [('is_open', '=', True)]}
            self.salary = 10000
        else:
            self.salary = 5000
        return {
            'warning': {
                'title': 'Hello',
                'message': 'you have changed the gender'
            },
            'domain': domain
        }

    # def any_pyfunction(self):
    #     vals = {
    #         'subject': 'Testing odoo',
    #         'body_html': "hello",
    #         'email_to': 'ammar.hass94@gmail.com',
    #         'auto_delete': False,
    #     }
    #     print("hi")
    #     mail = self.env['mail.mail'].sudo().create(vals)
    #     mail.sudo().send()

    def student_report(self):
        data = {
            'model_id': self.id,
            'date': self.admin_date,
            'student': self.name,
            'image': self.image,
            'class': self.class_id
            }

    def server_action_fun(self):
        print("server action function")
        # # for rec in self:
        # print("entering for loop")
        print(self.env['iti.student'].browse(self._context.get("active_ids")))
        self.env['iti.student'].browse(self._context.get("active_ids")).write({'salary': 400.0})

        # print("after updatin salary")
        # # self.write(
        # #             {
        # #                 "name": 'mamdouh ahmed'
        # #             }
        # #         )

    def wiz_open(self):

        return self.env['ir.actions.act_window']._for_xml_id("iti.student_wizard_actions")

        # return {'type': 'ir.actions.act_window',
        #         'res_model': 'student.update.wizard',
        #         'view_mode': 'form',
        #         'target': 'new'
        #          }

class StudentGrades(models.Model):
    _name = 'iti.grades'

    grade = fields.Selection([('vg', 'very good'), ('g', 'good')])
    student_id = fields.Many2one('iti.student')
    skills_id = fields.Many2many('iti.skill')


class FamilyClass(models.Model):
    _name = 'student.family'

    name = fields.Char()
    relative_id = fields.Many2one("family.type")
    student_id = fields.Many2one('iti.student')


class FamilyType(models.Model):
    _name = 'family.type'

    name = fields.Char()