# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    purchase_line_id_new = fields.Many2one('purchase.order.line', ondelete='set null', index=True, readonly=True)
