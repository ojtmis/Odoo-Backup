from odoo import api, models, _


class ProfitAndLoss(models.AbstractModel):
    _name = 'report.team_accounting_profit_and_loss.pnl_container_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('tesesttttt')
        if self.env.context.get('pnl_report'):
            if data.get('report_data'):
                data.update({
                             'company': self.env.company,
                             'report_lines': data.get('report_data')['bs_lines'],
                             })
        return data
