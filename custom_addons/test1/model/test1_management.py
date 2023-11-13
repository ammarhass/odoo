from odoo import models, fields


class Test1(models.Model):
    _name = 'test1.test1'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")

    test_id = fields.Many2one('test2.test2',string='Many_to_one')
    employee_id = fields.Many2one('res.users', 'employee')
    price = fields.Monetary(currency_field='currency_id', string="price")
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id')
    company_id = fields.Many2one('res.company', string='Company', related='employee_id.company_id')
