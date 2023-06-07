from odoo import fields, models, api, tools


class GetDataHere(models.Model):
    _name = 'get.data.here'
    _description = 'Description'
    _auto = False
    # _inherit = 'profit.and.loss'
    # _order = 'root asc'

    root = fields.Char(string='Name')
    sub_category = fields.Many2one('sub.categ', string='Sub Category')
    # category = fields.Many2one('sub.categ', string='Sub Category')
    # pnl_connection = fields.Many2one('profit.and.loss', string='Category')
    account_id = fields.Many2one('account.account', string='Chart of Accounts')
    main_category = fields.Many2one('category', string='Category')
    date = fields.Char(string='Date')
    monthly = fields.Char(string='Monthly')
    yearly = fields.Char(string='Yearly')
    balance = fields.Monetary(string='Balance')
    grouped_analytic_account = fields.Char(string='Analytic Account (Grouped)')
    # debit = fields.Monetary(string='Debit')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    profit_and_loss_root = fields.Char(string='Code')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'get_data_here')  ## <-- This code is for query view
        self._cr.execute("""
                            CREATE or REPLACE view get_data_here as 
                            (
                    SELECT  row_number() over() as id, 
                                CONCAT(AML.pnl_id,' ',AML.root) as profit_and_loss_root,
                                AML.pnl_id AS profit_and_loss_id,
                                AML.root AS root,
                                AML.main_category as main_category,
                                AML.sub_category as sub_category,
                                AML.account_id as account_id,
                                AML.analytic_account_id as analytic_account_id,
                                AML.is_pnl_or_bs,
                                AML.balance as balance,
                                CASE 
                                    WHEN AAA.name like '%8310%' THEN 'PLASIC - SOT'
                                    WHEN AAA.name like '%8300%' THEN 'PLASIC - TOs'
                                    WHEN AAA.name like '%8110%' THEN 'ASPM MODULES'
                                    WHEN AAA.name like '%8100%' THEN 'HERMETICS'
                                    WHEN AAA.name like '%8120%' THEN 'DIE SALES' 
                                    ELSE 'SUPPORT' END AS grouped_analytic_account,
                                AML.date as date,
                                AML.monthly as monthly,
                                AML.yearly as yearly
                                    
                            FROM(
                            SELECT
								conn.pnl_id,
                                conn.is_pnl_or_bs,
                                conn.name as root,
                                conn.connection_categ as main_category,
                                conn.sub_category as sub_category,
                                aml.account_id as account_id,
                                aml.analytic_account_id as analytic_account_id,
                                ABS((SUM(aml.debit) - SUM(aml.credit))) as balance,
                                TO_CHAR(aml.date, 'YYYY-MM-DD') as date,
                                TO_CHAR(aml.date, 'MM-YYYY') as monthly,
                                TO_CHAR(aml.date,'YYYY') as yearly
                                    FROM(
                                        SELECT
										x.pnl_id,
                                        x.is_pnl_or_bs,
                                        x.name,
                                        x.connection_categ as connection_categ,
                                        x.sub_category as sub_category,
                                        y.account_id as account_id
                                        FROM
                                            public.profit_and_loss x,
                                            public.profit_and_loss_line y
                                        WHERE x.id = y.pnl_connection
                                    )AS conn,
                                public.account_move_line as aml
                                WHERE aml.account_id = conn.account_id
                                GROUP BY
								conn.pnl_id,
                                conn.is_pnl_or_bs,
                                conn.connection_categ,
                                conn.name,
                                conn.sub_category,
                                aml.account_id,
                                aml.analytic_account_id,
                                aml.date,
                                aml.name
                            ) AS AML
                               LEFT JOIN 
                            public.account_analytic_account as AAA
                            ON
                            AML.analytic_account_id = AAA.id
                            WHERE AML.is_pnl_or_bs = 'pnl' 
                            GROUP BY
								profit_and_loss_root,
								AML.pnl_id,
                                AML.root,
                                AML.main_category,
                                AML.sub_category,
                                AML.account_id,
                                AML.analytic_account_id,
                                AML.balance,
                                AML.is_pnl_or_bs,
								AML.date,
                                AML.monthly,
                                AML.yearly,
                                grouped_analytic_account
	                               
                            )
                                            """)

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True, store=True, )
