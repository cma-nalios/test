from odoo import models, fields, api
from datetime import timedelta, date
class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Estate Property Offer"
    _order="price desc"

    price = fields.Float("Price")
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused","Refused")], copy = False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity")
    date_deadline = fields.Date("Date Deadline", compute="_compute_date_deadline", inverse="_inverse_compute_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    



    @api.depends("validity")
    def _compute_date_deadline(self):
        for line in self:
            if line.create_date is False:
                line.create_date=date.today()
            line.date_deadline=line.create_date+timedelta(days=line.validity)

    def _inverse_compute_date_deadline(self):
        for line in self:
            line.validity=(line.date_deadline-line.create_date.date()).days

    def accept_action(self):
        self.status="accepted"
        self.property_id.selling_price=self.price
        self.property_id.buyer_id=self.partner_id


    def refuse_action(self):
        self.status="refused"
        

    def total_offers_action(self):
        for line in self:
            line.property_type_id.offer_count=len(line.mapped("property_type_id.offer_ids"))

    
    @api.model
    def create(self,vals):
        theobject = self.env['estate.property'].browse(vals['property_id'])
        for line in theobject:
            line.state="offer_received"
        return super().create(vals)
