from odoo import fields, models, api


class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    _description = 'Team Accounting Account Analytic Account'

    compute_here = fields.Float(compute='fetch_data_from_function')
    ann_account_debit = fields.Float()
    ann_account_credit = fields.Float()
    ann_account_balance = fields.Float()

    """Getting Balance, Credit, Debit here because the main function for credit debit balance is in compute only and not stored """
    def fetch_data_from_function(self):
        self.compute_here = 0
        fetch_debit = 0
        fetch_credit = 0
        fetch_balance = 0
        for rec in self:
            print(rec.debit)
            print(rec.credit)
            print(rec.balance)
            fetch_debit = rec.debit
            fetch_credit = rec.credit
            fetch_balance = rec.balance
        self.ann_account_debit = fetch_debit
        self.ann_account_credit = fetch_credit
        self.ann_account_balance = fetch_balance
