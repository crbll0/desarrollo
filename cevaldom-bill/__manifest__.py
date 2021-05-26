# -*- coding: utf-8 -*-
{
    'name': "CoreSystem - CEVALDOM",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "GrowIT",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
#         'views/res_config.xml',
        'views/res_partner.xml',
        'views/product.xml',
        'views/account_move.xml',
        'views/views.xml'
    ],
}
