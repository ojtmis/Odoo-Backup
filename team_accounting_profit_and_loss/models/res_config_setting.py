from ast import literal_eval

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    analytic_ids = fields.Many2many('account.analytic.account', string='Analytic Account')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('team_accounting_profit_and_loss.analytic_ids', self.analytic_ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_val = self.env['ir.config_parameter'].sudo()
        analytic_var = get_val.get_param('team_accounting_profit_and_loss.analytic_ids')
        res.update(
            analytic_ids=[(6, 0, literal_eval(analytic_var))]
        )
        return res
