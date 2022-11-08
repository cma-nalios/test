from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Estate Property Tag"
    _order="name"

    name=fields.Char("Name", required=True)
    color=fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_name', 'unique(name)', "Chaque tag doit être unique")
    ]