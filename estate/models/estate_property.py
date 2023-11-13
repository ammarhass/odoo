from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = 'id desc'
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]
    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    # def _default_date(self):
    #     return fields.Date.to_date('2002-10-02')

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda self: self._default_date_availability())
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[("N", "North"),
                                                     ("S", "South"),
                                                     ("E", "East"),
                                                     ("W", "West")],
                                          string="Garden Orientation")
    state = fields.Selection(string="status", selection=[
        ('n', 'New'),
        ('or', 'Offer Received'),
        ('oa', 'Offer Accepted'),
        ('s', 'Sold'),
        ('c', 'Canceled')
    ], default='n', required=True, copy=False)
    active = fields.Boolean(default=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float("Total Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float("Best Offer", compute='_compute_best_price')
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    nickname = fields.Char(
        related='buyer_id.name', store=True,
        depends=['buyer_id'])
    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for rec in self:
            if (
                    not float_is_zero(rec.selling_price, precision_rounding=0.01)
                    and float_compare(rec.selling_price, rec.expected_price * 90.0 / 100.0,
                                      precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            # best_prices = rec.offer_ids.mapped('price')
            # if len(best_prices):
            #     rec.best_offer = max(best_prices)
            # else:
            #     rec.best_offer = 0.0
            rec.best_offer = max(rec.offer_ids.mapped("price")) if rec.offer_ids else 0.0

    def sold_set(self):
        if self.state == 'c':
            raise UserError("Canceled properties cannot be sold.")
        else:
            self.state = 's'

    def canceled_set(self):
        if self.state == 's':
            raise UserError("Sold properties cannot be canceled.")
        else:
            self.state = 'c'
