from odoo import fields, models, api, _

from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _get_default_picking_type(self):
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        return self.env['stock.picking.type'].search([
            ('code', '=', 'mrp_operation'),
            ('warehouse_id.company_id', '=', company_id),
        ], limit=1).id


    name = fields.Char()
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        domain="[('code', '=', 'mrp_operation'), ('company_id', '=', company_id)]",
        default=_get_default_picking_type, required=True, check_company=True,
        readonly=True, states={'draft': [('readonly', False)]})

    def _prepare_move_raw_items(self, product_id, product_uom_qty):
        bom = self.env['mrp.bom']._bom_find(product=product_id, picking_type=self.picking_type_id,
                                            company_id=self.company_id.id, bom_type='normal')
        vals = []
        for rec in bom.bom_line_ids:
            vals_raw_ids = {
                'name': _('New'),
                'location_id': rec.product_id.with_context(force_company=self.company_id.id).property_stock_production.id,
                'location_dest_id': rec.product_id.with_context(force_company=self.company_id.id).property_stock_production.id,
                'product_id': rec.product_id.id,
                'product_uom': rec.product_uom_id.id,
                'product_uom_qty': rec.product_qty * product_uom_qty,
            }
            vals.append(vals_raw_ids)

        return vals

    def action_create_manufacturing_order(self):
        sale_ids = self.browse(self.env.context['active_ids'])
        for sale_id in sale_ids:
            for order in sale_id.order_line:
                bom = self.env['mrp.bom']._bom_find(product=order.product_id, picking_type=self.picking_type_id,
                                                    company_id=self.company_id.id, bom_type='normal')

                if order.product_uom_qty < order.product_id.package_type.std_lot_size:
                    new_mo = self.env['mrp.production'].create({
                        'name': _('New'),
                        'product_id': order.product_id.id,
                        'origin': sale_id.name,
                        'product_qty': order.product_uom_qty,
                        'bom_id': bom.id,
                        'product_uom_id': order.product_uom.id,
                        'date_start_wo': self.date_order,
                        'move_raw_ids': [(0, 0, line) for line in
                                         self._prepare_move_raw_items(order.product_id, order.product_uom_qty)],
                        # 'company_id': line.name,
                    })

                    new_mo.action_confirm()
                    continue

                if order.product_id.package_type.std_lot_size < order.product_uom_qty < order.product_id.package_type.max_lot_size:
                    new_mo = self.env['mrp.production'].create({
                        'name': _('New'),
                        'product_id': order.product_id.id,
                        'origin': sale_id.name,
                        'product_qty': order.product_uom_qty,
                        'bom_id': bom.id,
                        'product_uom_id': order.product_uom.id,
                        'date_start_wo': self.date_order,
                        'move_raw_ids': [(0, 0, line) for line in
                                         self._prepare_move_raw_items(order.product_id, order.product_uom_qty)],
                        # 'company_id': line.name,
                    })

                    new_mo.action_confirm()
                else:
                    try:
                        count_ref = order.product_uom_qty // order.product_id.package_type.std_lot_size

                    except ZeroDivisionError:
                        raise(_("No Standard Lot size set for {}").format(order.product_id))

                    count = 0.0
                    while count < count_ref:
                        new_mo = self.env['mrp.production'].create({
                            'name': _('New'),
                            'product_id': order.product_id.id,
                            'origin': sale_id.name,
                            'product_qty': order.product_id.package_type.std_lot_size,
                            'bom_id': bom.id,
                            'product_uom_id': order.product_uom.id,
                            'date_start_wo': self.date_order,
                            'move_raw_ids': [(0, 0, line) for line in
                                             self._prepare_move_raw_items(order.product_id, order.product_uom_qty)],
                        })
                        count += 1
                        new_mo.action_confirm()

                    else:
                        qty = order.product_uom_qty % order.product_id.package_type.std_lot_size
                        new_mo = self.env['mrp.production'].create({
                            'name': _('New'),
                            'product_id': order.product_id.id,
                            'origin': sale_id.name,
                            'product_qty': qty,
                            'bom_id': bom.id,
                            'product_uom_id': order.product_uom.id,
                            'date_start_wo': self.date_order,
                            'move_raw_ids': [(0, 0, line) for line in
                                             self._prepare_move_raw_items(order.product_id, order.product_uom_qty)],
                            # 'company_id': line.name,
                        })
                        new_mo.action_confirm()

    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: {}').format(', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'date_order': fields.Datetime.now()
        })

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        # self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True