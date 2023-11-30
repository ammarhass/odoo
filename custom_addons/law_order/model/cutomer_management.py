from odoo import models, fields, api
from datetime import date, datetime

class Customer(models.Model):
    _name = "customer"
    _description = "adding a customer"

    name = fields.Char(string = "Name")
    title = fields.Char(string = "Title")
    date = fields.Date(strint ="Date field", default=date.today())
    time = fields.Datetime(string="Datetime field", default=datetime.now())
    age = fields.Integer(string="Age", compute='_compute_age')
    lawyer_id = fields.Many2one('lawyers')
    print(type(fields.Char()))
    nickname = fields.Char(string="Nickname", related='name', depends=['name'])

    @api.depends('date')
    def _compute_age(self):
        for rec in self:
            currentyear = date.today()
            if rec.date:
                rec.age = currentyear.year - rec.date.year
            else:
                rec.age = 1
