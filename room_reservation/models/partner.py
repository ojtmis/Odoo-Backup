from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    # Add new column to res.partner model, by default reserver are not
    reserver = fields.Boolean('Reserver', default=False)

    session_ids = fields.Many2many('reservation.session', string='Attended Sessions', readonly='True')

