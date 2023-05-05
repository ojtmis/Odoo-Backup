from odoo import fields, models, api, _


class AccountAssetCategory(models.Model):
    _inherit = "account.asset.category"

    mui_cip_acc = fields.Many2one('account.account', company_dependent=True,
                                  string="MUI/CIP Account")
