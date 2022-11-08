from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property","salesman_id", attrs="{'invisible':[('name','=','available House')]}")
    vamos = fields.Char(name="Le caractère", string="Je sais pas")
    unboolean = fields.Boolean("Le boolean qui s'intègre partout", required=True)
