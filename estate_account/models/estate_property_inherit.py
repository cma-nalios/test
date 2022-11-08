from odoo import models, Command

class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        account_move = self.env['account.move'].sudo().create({
            'partner_id': self.buyer_id.id,
            'move_type' :'out_invoice',
            'name' : "Le Nom",
            'invoice_line_ids': [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit":self.selling_price*1.06+100
                })
            ]

        })
        return super().sold_action()