# -*- coding: utf-8 -*-
{
    'name': "approval_module_extension",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
     'depends': ['account', 'purchase', 'stock', 'purchase_stock', 'om_account_accountant', 'om_account_asset', 'om_account_budget',
                'team_accounting', 'accounting_pdf_reports', 'mrp', 'sale', 'purchase_requisition', 'approval_module'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_requisition_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
