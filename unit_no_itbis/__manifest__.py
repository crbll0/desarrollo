# -*- coding: utf-8 -*-
{
    'name': "unit_no_itbis",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/account.xml'
#         'views/templates.xml',
    ],
}
