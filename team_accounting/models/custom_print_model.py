from odoo import fields, models, api


class CustomModule(models.AbstractModel):
    _name = 'report.team_accounting.bill_report'
    _description = 'Custom Module for Print'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('report.team_accounting.bill_report')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return docargs
