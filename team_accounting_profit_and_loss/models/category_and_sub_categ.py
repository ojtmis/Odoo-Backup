from odoo import models, fields


class Category(models.Model):
    _name = 'category'
    _description = 'Category and Sub Category'
    _rec_name = 'is_category'

    is_category = fields.Many2one('setting.category', string='Category', required=True)
    is_pnl_or_bs = fields.Selection([
        ('pnl', 'Profit and loss',),
        ('bs', 'Balance Sheet')], string='Profit and Loss or Balance Sheet', related='is_category.is_pnl_or_bs',
        store=True)
    connecton_sub_categ = fields.One2many('sub.categ', 'connection_categ', string='Connection', store=True)

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         result.append((rec.id, '%s - %s' % (rec.code, rec.is_category.is_category)))
    #     return result


class SubCategory(models.Model):
    _name = 'sub.categ'
    _rec_name = 'sub_category'

    connection_categ = fields.Many2one('category', string='Connection', default='-')
    sub_category = fields.Many2one('setting.subcategory', string='Sub Category')




