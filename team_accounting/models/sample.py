from odoo import models, fields, api
class SaleCustom(models.Model):
   _name = 'account.custom'
   @api.model
   def get_sale_order(self):
       ret_list = []
       req = (
            """SELECT 
                    a.id,
                    a.name,
					a.ann_account_debit,
					a.ann_account_credit,
					a.ann_account_balance,
                    b.name as name_b, 
                    b.account_id,
                    b.amount,
                    b.unit_amount
                    from 
                    account_analytic_account a 
                    left join 
                    account_analytic_line b
                    on 
                    a.id = b.account_id
                    WHERE a.name in ('8100 Hermetics','8120 Die Sales','8300 Plastics-TOs','8310 Plastics-SOT','8200 Others')""")
       self.env.cr.execute(req)
       for rec in self.env.cr.dictfetchall():
           ret_list.append(rec)
       return ret_list

   @api.model
   def fetch_new_data(self):
       fetch_list = []
       sql = ("""
            SELECT 
                        a.id,
                        b.name as name_b, 
                        b.account_id,
                        b.amount,
                        b.date,
                        b.unit_amount,
						b.product_id
                        from 
                        account_analytic_account a 
                        left join 
                        account_analytic_line b
                        on 
                        a.id = b.account_id
                        WHERE a.name in ('8310 Plastics-SOT')""")
       self.env.cr.execute(sql)
       for rec in self.env.cr.dictfetchall():
           fetch_list.append(rec)
       return fetch_list
