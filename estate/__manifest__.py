# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Module Learning Le Vrai',
    'depends' : [
        'base_setup'
    ],
    'data' : [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
        
        'wizards/estate_property_wizard_views.xml',

        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_views.xml',
        'views/estate_menus.xml',

        #"demo/demo_data.xml"
    ],
    # "demo" : [
    #     "demo/demo_data.xml"
    # ],
    'category': 'Real Estate/Brokerage',
    'application': True
}
