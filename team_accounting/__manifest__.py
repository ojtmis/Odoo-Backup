#John Raymark LLavanes
#MIS - 2k23
{
    'name': 'Team Pacific Corporation Accounting Module',
    'version': '0.1',
    'category': 'Accounting Extensions',
    'summary': 'Accounting Customization For Odoo 13',
    'sequence': '10',
    'author': 'John Raymark LLavanes - 10450',
    'company': 'Team Pacific Corporation',
    'maintainer': 'MIS - LOC 267',
    'support': 'mis@teamglac.com',
    'website': '',
    'depends': ['account'],
    'live_test_url': '',
    'demo': [],
    'data': [
        #Reports

        'reports/report_views.xml',
        'reports/debit_credit_report.xml',
        'reports/vendor_bills_report.xml',
        'reports/bills_report.xml',
        'reports/payment_voucher_signed.xml',
        'reports/payment_voucher_signed_whole.xml',
        'reports/report_payment_receipt_templates.xml',
        'reports/payment_voucher_signed_account_move.xml',
        'reports/payment_voucher_whole.xml',
        'reports/payment_voucher_template_journalentries.xml',
        'reports/check_voucher.xml',
        'reports/ap_voucher.xml',
        'reports/debit_credit_memo_v2.xml',
        'reports/general_ledger.xml',
        'reports/new_debit_credit_report.xml',
        'reports/new_debit_credit_report_v2.xml',
        'reports/report_purchase_request.xml',

        #Views

        'views/account_payment_views.xml',
        'views/account_p_and_l_view.xml',
        'views/account_move_views.xml',
        'views/templates.xml',
        'views/ir_actions_report.xml',
        'views/team_accounting_menu.xml',
        'views/analytic_account_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
        'static/src/xml/report_pdf_options.xml',
        'static/src/xml/general_ledger_view.xml',
        'static/src/xml/sample.xml'

    ],

}
