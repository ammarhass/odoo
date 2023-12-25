from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence"
    # _sql_constraints = [('name_uniq', 'unique (name)', "the name must be unique")]

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=10)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer("Offer Counter", compute="_compute_offer")
    _sql_constraints = [('name_uniq', 'unique (name)', "the name must be unique")]

    def _compute_offer(self):
        # data = self.env["estate.property.offer"].read_group(
        #     [("property_id.state", "!=", "canceled"), ("property_type_id", "!=", False)],
        #     ["ids:array_agg(id)", "property_type_id"],
        #     ["property_type_id"],
        # )
        # mapped_count = {d["property_type_id"][0]: d["property_type_id_count"] for d in data}
        # mapped_ids = {d["property_type_id"][0]: d["ids"] for d in data}
        # for prop_type in self:
        #     prop_type.offer_count = mapped_count.get(prop_type.id, 0)
        #     prop_type.offer_ids = mapped_ids.get(prop_type.id, [])
        for rec in self:
                print(rec.mapped("name"))
                rec.offer_count = len(rec.mapped("offer_ids"))


    def action_view_offers(self):
        # print(self.env.ref("estate.estate_property_offer_action"))
        res = self.env.ref("estate.estate_property_offer_action").read()[0]
        print(self.env['estate.property.tag'].search([]))
        # res["domain"] = [("id", "in", self.offer_ids.ids)]
        # print(res)
        return res