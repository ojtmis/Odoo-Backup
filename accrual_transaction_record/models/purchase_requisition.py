from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.requisition"

    amount_total = fields.Float(compute='_compute_amount_total')

    @api.depends('line_ids.subtotal')
    def _compute_amount_total(self):
        self.amount_total = sum([line.subtotal for line in self.line_ids])


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    subtotal = fields.Float(compute="_compute_subtotal")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_qty = 1.0
            if self.requisition_id.vendor_id == [rec.seller_ids.name for rec in self.product_id][0]:
                self.price_unit = [rec.price for rec in self.product_id.seller_ids][0]
                # self.qty_ordered = [rec.seller_ids.min_qty for rec in self.product_id][0]
                self.product_uom_id = [rec.seller_ids.product_uom for rec in self.product_id][0]
            else:
                self.price_unit = self.product_id.standard_price
                self.product_uom_id = self.product_id.uom_po_id

        if not self.schedule_date:
            self.schedule_date = self.requisition_id.schedule_date

    @api.depends('price_unit', 'product_qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.product_qty * rec.price_unit


