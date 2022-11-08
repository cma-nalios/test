# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.addons.estate.models.estate_property import PROPERTY_STATES


class EstatePropertyWizard(models.TransientModel):
    _name = 'estate.property.wizard'

    state = fields.Selection(PROPERTY_STATES)

    def testWizard(self):
        properties = self.env['estate.property'].search([])
        return
