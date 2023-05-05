from odoo import fields, models


class MainCategory(models.Model):
    _name = 'main.category'
    _description = 'Main Category'
    _rec_name = 'is_main'

    is_main = fields.Char(string='Main Category')


class SettingCategory(models.Model):
    _name = 'setting.category'
    _description = 'Description'
    _rec_name = 'is_category'

    # code = fields.Char(string='Code Sequence', required=True, default='00001')
    is_pnl_or_bs = fields.Selection([
        ('pnl', 'Profit and loss',),
        ('bs', 'Balance Sheet')], string='Profit and Loss or Balance Sheet', required=True)
    is_category = fields.Char(string='Category', required=True, default='####')


class SettingSubcategory(models.Model):
    _name = 'setting.subcategory'
    _description = 'Subcategory'
    _rec_name = 'is_sub_category'

    is_sub_category = fields.Char(string='Sub Category', default='####')
