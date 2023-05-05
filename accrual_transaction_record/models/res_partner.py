from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    accrual_transaction = fields.Many2one('account.account', company_dependent=True,
                                                      string="Accrual Input Account")
    local = fields.Boolean()
    indent = fields.Boolean()
    contact_person = fields.Char()
