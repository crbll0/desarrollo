# -*- coding: utf-8 -*-
{
    'name': "Modulo",

    'summary': """
        Formularios de vinculacion""",

    'description': """
        Long description of module's purpose
    """,

    'author': "GrowIT",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Extra Rights, Other Extra Rights, Administration,  Theme, After-Sales,Document Signatures,Website,Specific Industry Applications,Point of Sale,Payroll,Attendance
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'report_py3o', 'contacts'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/reports.xml',
        'views/formulario.xml'
    ],
}

