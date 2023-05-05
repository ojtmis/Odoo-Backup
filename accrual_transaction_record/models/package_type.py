from odoo import fields, models, api, _


class PackageType(models.Model):
    _name = "package.type"

    name = fields.Char(required=True)
    complete_name = fields.Char(compute='_compute_complete_name',
        store=True)
    parent_id = fields.Many2one('package.type', 'Parent Pacakge Type', index=True, ondelete='cascade')
    std_lot_size = fields.Integer(string='Standard Lot Size', required=True)
    max_lot_size = fields.Integer(string='Maximum Lot Size', required=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for package in self:
            if package.parent_id:
                package.complete_name = '{} / {}'.format(package.parent_id.complete_name, package.name)
            else:
                package.complete_name = package.name