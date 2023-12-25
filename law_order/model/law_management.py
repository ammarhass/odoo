from odoo import models, fields



class NewManagement(models.Model):
    _name = 'lawyers'
    _description = 'law management'

    name = fields.Char(string="Name", required=True)
    new_field = fields.Char(string="new_field")
    customer_id = fields.Many2one('customer',string="Customers")
    customer_ids = fields.Many2many('customer', string="Customer many")
    customer2_ids = fields.One2many('customer', 'lawyer_id', string="onetomany")

    lawyer_id = fields.Many2one('res.users', string="Lawyer")
    price = fields.Monetary(currency_field='currency_id', string="price")
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id')
    company_id = fields.Many2one('res.company', string='Company', related='lawyer_id.company_id')
    reference = fields.Reference(selection=[('res.company', 'Company'), ('res.currency', 'Currency'),('lawyers.new_field', 'New_field')], string="Reference")

    field01 = fields.Text(string="text field")
    field02 = fields.Selection([('male','Male'),('female','Female')], string="selection field")
    field03 = fields.Boolean(string="boolean field")
    field04 = fields.Html(string="html field")
    field05 = fields.Integer(string="integer field")
    field06 = fields.Image(string="image field")
    field07 = fields.Binary(string="binary field")
