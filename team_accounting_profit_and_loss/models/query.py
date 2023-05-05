from odoo import models, fields, api


class SaleCustom(models.Model):
    _name = 'sale.custom'

    @api.model
    def get_sale_order(self):
        ret_list = []
        req = (
            """SELECT
                        aa.code as code,
                        aml.debit as debit,
                        aml.credit,
                        aml.balance,
                        aa.internal_group,
                        aml.account_id
                        FROM  
                        public.account_move_line aml,
                        public.account_account aa
                        WHERE aml.account_id = aa.id
                        AND	aa.internal_group in ('expense','income')
                        AND (aa.code like '4%'
                         or aa.code like '5%'
                         or aa.code like '6%'
                         or aa.code like '7%'
                         or aa.code like '8%')""")
        self.env.cr.execute(req)
        for rec in self.env.cr.dictfetchall():
            ret_list.append(rec)
        return ret_list

