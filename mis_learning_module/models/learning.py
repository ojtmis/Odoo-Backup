from odoo import fields, models

class LearningMIS(models.Model):
    _name = 'mis.learning'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'MIS Learning Table'

    title = fields.Char(string='Title', required=True)
    overview = fields.Text(string='Overview', required=True)
    difficulty = fields.Selection([
        ('very_easy', 'Very Easy'),
        ('easy', 'Easy'),
        ('normal', 'Normal'),
        ('hard', 'Hard'),
        ('very_hard', 'Very Hard')
    ], required=True)
    image = fields.Binary(string='Image')

