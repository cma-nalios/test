from odoo import models, fields, api, _

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many("estate.property", "estate_property_type_id")
    expected_price = fields.Float()
    state = fields.Selection(string="State", selection=[("new","New"),("offer_received","Offer Received"),("offer_accepted","Offer Accepted"),("canceled","Canceled"),("sold","Sold")], required=True, copy=False, default="new")
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many("estate.property.offer","property_type_id")
    offer_count = fields.Integer(compute="_sum_total_offers")

    _sql_constraints = [
        ('unique_name_type', 'unique(name)', "Chaque nom doit être unique")
    ]

    @api.depends("offer_ids")
    def _sum_total_offers(self):
        for line in self:
            line.offer_count = len(line.offer_ids)
            

    def open_estate_offers(self):
        action = self.env['ir.actions.actions']._for_xml_id('estate.estate_property_offer_action')
        action.update({
            'domain': [('id', 'in', self.offer_ids.ids)],
        })
        return action