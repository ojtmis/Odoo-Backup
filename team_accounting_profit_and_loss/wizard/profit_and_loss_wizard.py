from odoo import fields, models, api


class ProfitAndLossWizard(models.TransientModel):
    _name = 'profit.loss.wizard'
    _inherit = 'account.common.report'
    _description = 'Profit and Loss Wizard'

    code = fields.Char(string='Code')
    debit = fields.Monetary(string='Debit')
    credit = fields.Monetary(string='Credit')
    balance = fields.Monetary(string='Balance')
    internal_group = fields.Monetary(string='Internal Group')
    account_id = fields.Monetary(string='Account ID')

    @api.model
    def view_report(self, option, tag):
        r = self.env['profit.loss.wizard'].search(
            [('id', '=', option[0])])
        data = {
            'code': r.code,
            'debit': r.debit,
            'credit': r.credit,
            'balance': r.balance,
            'internal_group': r.internal_group,
            'account_id': r.account_id,
        }
        records = self._get_report_values(data)
        print(records)

        return {
            'name': "Profit and Loss",
            'type': 'ir.actions.client',
            'tag': 'sale_cust',
            'report_lines': records['debit_total'],
            'sample': records['sample'],
        }

    def _get_report_values(self, data):
        is_debits = self.debit
        is_credits = self.credit
        sample = 'This is sample text for testing'

        return {
            'doc_ids': self.ids,
            'debit_total': is_debits,
            'credit_total': is_credits,
            'sample': sample,
        }

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True, store=True,
                                  compute_sudo=True)


