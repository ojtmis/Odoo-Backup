from odoo import fields, models, api, _


class ProductCategory(models.Model):
    _inherit = "product.category"

    accrual_transaction = fields.Many2one('account.account', company_dependent=True,
                                                      string="Accrual Input Account")
    debit_note_acc = fields.Many2one('account.account', company_dependent=True,
                                                      string="Debit Note Account")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_product_accounts(self):
        return {
            'income': self.property_account_income_id or self.categ_id.property_account_income_categ_id,
            'expense': self.property_account_expense_id or self.categ_id.property_account_expense_categ_id,
            'receivable': self.categ_id.debit_note_acc
        }

    package_type = fields.Many2one('package.type')
