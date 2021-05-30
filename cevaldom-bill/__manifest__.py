# -*- coding: utf-8 -*-
{
    'name': "CoreSystem - CEVALDOM",

    'summary': """
    Integracion de Odoo con el sistema core de CEVALDOM.
    """,

    'description': """
    """,

    'author': "GrowIT",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_config.xml',
        'views/res_partner.xml',
        'views/product.xml',
        'views/account_move.xml',
        'views/views.xml'
    ],
}
