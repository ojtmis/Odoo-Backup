from odoo import fields, models, api, tools


class ProfitAndLossQry(models.Model):
    _name = 'profit.and.loss.qry'
    _description = 'Profit and Loss Query'
    _auto = False

    sub_category = fields.Many2one('setting.subcategory', string='Sub Category')
    category = fields.Many2one('sub.categ', string='Sub Category')
    pnl_connection = fields.Many2one('profit.and.loss', string='Sub Category')
    account_id = fields.Many2one('account.account', string='Analytic Accounts')
    connection_categ = fields.Many2one('category', string='Connection')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'profit_and_loss_qry')
        self._cr.execute("""
                            CREATE or REPLACE view profit_and_loss_qry as (
                                    SELECT  
                                        row_number() over() as id,
                                        aml.account_id as account_id, 
                                        conn.sub_category as sub_category, 
                                        conn.connection_categ as connection_categ,
                                        conn.pnl_connection as pnl_connection
                                    FROM
                                    (
                                        SELECT 
                                            a.sub_category,
                                            a.connection_categ,
                                            b.pnl_connection,
                                            b.account_id
                                        FROM
                                            PUBLIC.profit_and_loss a,
                                            PUBLIC.profit_and_loss_line b
                                        WHERE 
                                            a.id = b.pnl_connection
                                        ORDER BY 
                                            a.id 
                                        ASC
                                    ) AS conn,
                                    public.account_move_line as aml 
                                    WHERE 
                                        aml.account_id = conn.account_id
                                    ORDER BY 
                                        aml.account_id 
                                    DESC
                            )""")

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True, store=True, )
