from odoo import fields, models, api, _


class ProfitAndLoss(models.Model):
    _name = 'team.profit.loss'
    _description = 'Team Profit and Loss'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Profit and Loss", readonly=True, copy=False, default='New')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string="Status", tracking=True)

    profit_and_loss_date_start = fields.Datetime('Date Start')
    profit_and_loss_date_end = fields.Datetime('Date End')
    connection = fields.One2many('team.profit.loss.line', 'team_and_l')
    fetch_analytic_line_data = fields.Float()
    view_count = fields.Integer(compute='fetch_analytic_line_count', string='Counting in Form')
    view_count_data = fields.Integer(string='Passed Data from View Count')
    notes = fields.Char('Notes')

    def fetch_analytic_line_count(self):
        self.view_count = 0
        counting = self.env['team.analytic.line'].search_count([('team_profit_loss_conn', '=', self.id)])
        self.view_count_data = counting

    def action_view_lines(self):
        print('tangina')
        self.ensure_one()
        return {
            'name': _('Analytic Account Line'),
            'view_mode': 'tree,form',
            'res_model': 'team.analytic.line',
            # 'view_id': self.env.ref('team_accounting_profit_and_loss.analytic_acc_line_view_tree_new').id,
            'type': 'ir.actions.act_window',
            'context': {
            },
            'domain': [('team_profit_loss_conn', '=', self.id)],
            'target': 'current',
        }

    def counting_self_name(self):
        for rec in self:
            print('sample')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'team.profit.loss') or 'New'
        result = super(ProfitAndLoss, self).create(vals)
        return result

    def print_here(self):
        print('Print')

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'


class TeamProfitLossLine(models.Model):
    _name = 'team.profit.loss.line'
    _description = 'Team Profit and Loss Move Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    team_and_l = fields.Many2one('team.profit.loss')
    connection = fields.Many2one('team.analytic.line')
    analytic_acc = fields.Many2one('account.analytic.account', 'Analytic Account', required=True)
    debit_line_team = fields.Float('Debit', related='analytic_acc.ann_account_debit', stored=True)
    credit_line_team = fields.Float('Credit', related='analytic_acc.ann_account_credit', stored=True)
    balance_line_team = fields.Float('Balance', related='analytic_acc.ann_account_balance', stored=True)

    name = fields.Char('Name')
    date_data = fields.Datetime('Date')
    amount = fields.Float('Amount')
    unit_amm = fields.Float('Unit Amount')
    acc_id = fields.Integer('Account Id')

    @api.onchange('analytic_acc')
    def _onchange_fetch_analytic_acc_line(self):
        for rec in self:
            get_id = rec.analytic_acc.line_ids
            get_connection_data = rec.team_and_l._origin.id  # """<--- In Here you can use ._origin.id to get the id if you have encounter <NewId origin=1> """
            print(get_connection_data)
            for pass_data in get_id:
                pass_value = self.connection
                pass_value.create({
                    'team_profit_loss_conn': get_connection_data,
                    'connection_id': rec.analytic_acc.id,
                    'analytic_id': pass_data.id,
                    'name': pass_data.name,
                    'date': pass_data.date,
                    'amount': pass_data.amount,
                    'unit_amount': pass_data.unit_amount,
                })
                return pass_value


class AnalyticLine(models.Model):
    _name = 'team.analytic.line'
    _description = 'Team Pacific Corp Analytic Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    team_profit_loss_conn = fields.Many2one('team.profit.loss')
    connection_id = fields.Many2one('account.analytic.account')
    analytic_id = fields.Integer()

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    name = fields.Char('Description')
    date = fields.Date('Date', index=True, default=fields.Date.context_today)
    amount = fields.Monetary('Amount', default=0.0)
    unit_amount = fields.Float('Quantity', default=0.0)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure',
                                     domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_uom_id.category_id', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    user_id = fields.Many2one('res.users', string='User', default=_default_user)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True, store=True,
                                  compute_sudo=True)
