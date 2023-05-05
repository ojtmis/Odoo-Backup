from odoo import fields, models, api, tools


class AccountPandL(models.Model):
    _name = 'account.p_and_l'
    # _inherit = 'account.move.line'
    _description = 'Description'

    # def init(self):
    #     tools.drop_view_if_exists(self._cr, 'account.p_and_l')
    #     self._cr.execute("""
    #               CREATE or REPLACE view get_data_here as (
    #               SELECT row_number() over() as id, line.partner_id,
    # line.quantity , line.price_unit FROM(
    # SELECT so.partner_id , sol.product_uom_qty as quantity,
    # sol.price_unit
    # FROM public.sale_order_line sol
    # LEFT JOIN public.sale_order so ON (so.id = sol.order_id)
    # ) line
    # )""")
