from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    # Add new column to res.partner model, by default partners are not
    instructor = fields.Boolean('Instructor', default=False)

    session_ids = fields.Many2many('openacademy.session', string='Attended Sessions', readonly='True')
