from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import datetime
from odoo.exceptions import UserError

class RealEstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "real estate offers"
    _order = 'price desc'
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]

    price = fields.Float(required=True)
    state = fields.Selection(selection=[('a', 'Accepted'),('r', 'Refused')], default=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date("Deadline", compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", string="Property Type", store=True
    )
    @api.depends("validity")
    def _compute_deadline(self):
        for rec in self:
            date = rec.create_date.date() if rec.create_date else fields.Date.today()
            rec.date_deadline = date + relativedelta(days=rec.validity)

    def _inverse_deadline(self):
        for rec in self:
            date = rec.create_date.date() if rec.create_date else fields.Date.today()
            rec.validity = (rec.date_deadline - date).days

    def accept_state(self):
        if "a" in self.mapped("property_id.offer_ids.state"):
        # if self.state == 'a':
            raise UserError("An offer as already been accepted.")
        # self.state = 'a'
        # self.property_id.selling_price = self.price
        # self.property_id.buyer_id = self.partner_id
        self.write(
            {
                "state": "a",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "oa",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id
            }
        )

    def cancel_state(self):
        self.write(
            {
                "state": "r"
            }
        )
        # if "a" not in self.mapped("property_id.offer_ids.state"):
        #     self.mapped("property_id").write(
        #         {
        #             "state": "n",
        #             # "selling_price" : 0.0
        #         }
        #     )
        # self.state = 'r'
